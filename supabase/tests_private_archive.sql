-- Run with psql against a disposable LOCAL Supabase database after migrations.
-- Uses administrator privileges only for fixtures/SET ROLE, then tests real
-- Postgres permissions and RLS as authenticated/anon. Entire test rolls back.
-- This is NOT the live two-account JWT/API test or required screenshot.
begin;
select set_config('rr_test.a', gen_random_uuid()::text, true);
select set_config('rr_test.b', gen_random_uuid()::text, true);
select set_config('rr_test.ca', gen_random_uuid()::text, true);
select set_config('rr_test.cb', gen_random_uuid()::text, true);
select set_config('rr_test.pa', gen_random_uuid()::text, true);
select set_config('rr_test.pb', gen_random_uuid()::text, true);
select set_config('rr_test.ra', gen_random_uuid()::text, true);
insert into auth.users(id) values (current_setting('rr_test.a')::uuid), (current_setting('rr_test.b')::uuid);
insert into public.rr_classes(id, owner_id, name) values
  (current_setting('rr_test.ca')::uuid, current_setting('rr_test.a')::uuid, 'Synthetic A'),
  (current_setting('rr_test.cb')::uuid, current_setting('rr_test.b')::uuid, 'Synthetic B');
insert into public.rr_projects(id, owner_id, class_id, name, instructions) values
  (current_setting('rr_test.pa')::uuid, current_setting('rr_test.a')::uuid, current_setting('rr_test.ca')::uuid, 'Synthetic A', 'Synthetic instructions'),
  (current_setting('rr_test.pb')::uuid, current_setting('rr_test.b')::uuid, current_setting('rr_test.cb')::uuid, 'Synthetic B', 'Synthetic instructions');
insert into public.rr_reviews(id, owner_id, project_id, save_token, snapshot) values
  (current_setting('rr_test.ra')::uuid, current_setting('rr_test.a')::uuid, current_setting('rr_test.pa')::uuid,
   gen_random_uuid(), '{"schema_version":1}');

select set_config('request.jwt.claim.sub', current_setting('rr_test.b'), true);
select set_config('request.jwt.claims', json_build_object('sub', current_setting('rr_test.b'), 'role', 'authenticated')::text, true);
set local role authenticated;
do $$
declare n integer;
begin
  if auth.uid() <> current_setting('rr_test.b')::uuid then raise exception 'Wrong test identity'; end if;
  if (select count(*) from public.rr_classes) <> 1 then raise exception 'B class visibility incorrect'; end if;
  if (select count(*) from public.rr_projects) <> 1 then raise exception 'B project visibility incorrect'; end if;
  if exists(select 1 from public.rr_reviews) then raise exception 'A review leaked to B'; end if;
  update public.rr_projects set name = 'Unauthorized' where id = current_setting('rr_test.pa')::uuid;
  get diagnostics n = row_count;
  if n <> 0 then raise exception 'B changed A project'; end if;
  delete from public.rr_reviews where id = current_setting('rr_test.ra')::uuid;
  get diagnostics n = row_count;
  if n <> 0 then raise exception 'B deleted A review'; end if;
  delete from public.rr_projects where id = current_setting('rr_test.pa')::uuid;
  get diagnostics n = row_count;
  if n <> 0 then raise exception 'B deleted A project'; end if;
  delete from public.rr_classes where id = current_setting('rr_test.ca')::uuid;
  get diagnostics n = row_count;
  if n <> 0 then raise exception 'B deleted A class'; end if;
  begin
    insert into public.rr_classes(owner_id, name) values (current_setting('rr_test.a')::uuid, 'Forged owner');
    raise exception 'Forged owner insert allowed';
  exception when insufficient_privilege then null; end;
  begin
    insert into public.rr_projects(owner_id, class_id, name, instructions) values
      (auth.uid(), current_setting('rr_test.ca')::uuid, 'Cross-parent', 'Synthetic');
    raise exception 'Cross-owner project insert allowed';
  exception when foreign_key_violation then null; end;
  begin
    update public.rr_projects set class_id = current_setting('rr_test.ca')::uuid where id = current_setting('rr_test.pb')::uuid;
    raise exception 'Cross-owner reparent allowed';
  exception when foreign_key_violation then null; end;
  begin
    insert into public.rr_reviews(owner_id, project_id, save_token, snapshot) values
      (auth.uid(), current_setting('rr_test.pa')::uuid, gen_random_uuid(), '{"schema_version":1}');
    raise exception 'Cross-owner review insert allowed';
  exception when foreign_key_violation then null; end;
  begin
    update public.rr_classes set owner_id = current_setting('rr_test.a')::uuid where id = current_setting('rr_test.cb')::uuid;
    raise exception 'Owner reassignment allowed';
  exception when insufficient_privilege then null; end;
  if public.rr_deletion_counts('classes', current_setting('rr_test.ca')::uuid)
       <> '{"classes":0,"projects":0,"reviews":0}'::jsonb then raise exception 'Counts leaked A data'; end if;
  update public.rr_projects set name = 'B updated own project' where id = current_setting('rr_test.pb')::uuid;
  get diagnostics n = row_count;
  if n <> 1 then raise exception 'B own update failed'; end if;
end $$;

reset role;
select set_config('request.jwt.claim.sub', current_setting('rr_test.a'), true);
select set_config('request.jwt.claims', json_build_object('sub', current_setting('rr_test.a'), 'role', 'authenticated')::text, true);
set local role authenticated;
do $$
declare c uuid; p uuid; token uuid := gen_random_uuid(); n integer;
begin
  if (select name from public.rr_projects where id = current_setting('rr_test.pa')::uuid) <> 'Synthetic A'
    then raise exception 'A project was changed'; end if;
  if not exists(select 1 from public.rr_reviews where id = current_setting('rr_test.ra')::uuid)
    then raise exception 'A review missing'; end if;
  insert into public.rr_classes(name) values ('Cascade fixture') returning id into c;
  insert into public.rr_projects(class_id, name, instructions) values (c, 'Cascade fixture', 'Synthetic') returning id into p;
  insert into public.rr_reviews(project_id, save_token, snapshot) values (p, token, '{"schema_version":1}');
  -- Same operation used by the HTTP save path; no UPDATE privilege required.
  insert into public.rr_reviews(owner_id, project_id, save_token, snapshot)
    values (auth.uid(), p, token, '{"schema_version":1}') on conflict (owner_id, save_token) do nothing;
  if (select count(*) from public.rr_reviews where save_token = token) <> 1 then raise exception 'Duplicate save'; end if;
  begin
    update public.rr_reviews set snapshot = '{"schema_version":1}' where project_id = p;
    raise exception 'Saved snapshot was mutable';
  exception when insufficient_privilege then null; end;
  if public.rr_deletion_counts('classes', c) <> '{"classes":1,"projects":1,"reviews":1}'::jsonb
    then raise exception 'Cascade counts incorrect'; end if;
  delete from public.rr_classes where id = c;
  if exists(select 1 from public.rr_projects where id = p) or exists(select 1 from public.rr_reviews where project_id = p)
    then raise exception 'Cascade did not remove descendants'; end if;
end $$;

reset role;
select set_config('request.jwt.claim.sub', '', true);
select set_config('request.jwt.claims', '{}', true);
set local role anon;
do $$ begin
  begin perform * from public.rr_classes; raise exception 'Anonymous class read allowed';
    exception when insufficient_privilege then null; end;
  begin perform * from public.rr_projects; raise exception 'Anonymous project read allowed';
    exception when insufficient_privilege then null; end;
  begin perform * from public.rr_reviews; raise exception 'Anonymous review read allowed';
    exception when insufficient_privilege then null; end;
  begin perform public.rr_deletion_counts('classes', current_setting('rr_test.ca')::uuid); raise exception 'Anonymous RPC allowed';
    exception when insufficient_privilege then null; end;
end $$;
reset role;
rollback;
