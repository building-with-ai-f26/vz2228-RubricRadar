-- Batch 2 foundation. Apply only to a reviewed empty/test Supabase project.
-- One transaction: no intermediate tables exposed without policies.
begin;

create table public.rr_classes (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  name text not null check (char_length(btrim(name)) between 1 and 200),
  professor text not null default '' check (char_length(professor) <= 200),
  semester text not null default '' check (char_length(semester) <= 200),
  created_at timestamptz not null default now(),
  unique (id, owner_id)
);
create table public.rr_projects (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  class_id uuid not null,
  name text not null check (char_length(btrim(name)) between 1 and 200),
  instructions text not null check (char_length(btrim(instructions)) between 1 and 12000),
  created_at timestamptz not null default now(),
  unique (id, owner_id),
  foreign key (class_id, owner_id) references public.rr_classes(id, owner_id) on delete cascade
);
create table public.rr_reviews (
  id uuid primary key default gen_random_uuid(),
  owner_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  project_id uuid not null,
  save_token uuid not null,
  snapshot jsonb not null check (
    jsonb_typeof(snapshot) = 'object' and snapshot ? 'schema_version'
    and snapshot->>'schema_version' = '1' and octet_length(snapshot::text) <= 1000000),
  created_at timestamptz not null default now(),
  unique (owner_id, save_token),
  foreign key (project_id, owner_id) references public.rr_projects(id, owner_id) on delete cascade
);
create index rr_classes_owner on public.rr_classes(owner_id);
create index rr_projects_owner_class on public.rr_projects(owner_id, class_id);
create index rr_reviews_owner_project on public.rr_reviews(owner_id, project_id);

alter table public.rr_classes enable row level security;
alter table public.rr_classes force row level security;
alter table public.rr_projects enable row level security;
alter table public.rr_projects force row level security;
alter table public.rr_reviews enable row level security;
alter table public.rr_reviews force row level security;

-- Clear automatic/default grants, then grant only necessary operations/columns.
revoke all on public.rr_classes, public.rr_projects, public.rr_reviews from public, anon, authenticated;
grant select, delete on public.rr_classes, public.rr_projects, public.rr_reviews to authenticated;
grant insert (owner_id, name, professor, semester) on public.rr_classes to authenticated;
grant update (name, professor, semester) on public.rr_classes to authenticated;
grant insert (owner_id, class_id, name, instructions) on public.rr_projects to authenticated;
grant update (class_id, name, instructions) on public.rr_projects to authenticated;
grant insert (owner_id, project_id, save_token, snapshot) on public.rr_reviews to authenticated;
-- No UPDATE privilege or policy on snapshots: reviews are append-only + deletable.

create policy rr_classes_select on public.rr_classes for select to authenticated using ((select auth.uid()) = owner_id);
create policy rr_classes_insert on public.rr_classes for insert to authenticated with check ((select auth.uid()) = owner_id);
create policy rr_classes_update on public.rr_classes for update to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
create policy rr_classes_delete on public.rr_classes for delete to authenticated using ((select auth.uid()) = owner_id);
create policy rr_projects_select on public.rr_projects for select to authenticated using ((select auth.uid()) = owner_id);
create policy rr_projects_insert on public.rr_projects for insert to authenticated with check ((select auth.uid()) = owner_id);
create policy rr_projects_update on public.rr_projects for update to authenticated using ((select auth.uid()) = owner_id) with check ((select auth.uid()) = owner_id);
create policy rr_projects_delete on public.rr_projects for delete to authenticated using ((select auth.uid()) = owner_id);
create policy rr_reviews_select on public.rr_reviews for select to authenticated using ((select auth.uid()) = owner_id);
create policy rr_reviews_insert on public.rr_reviews for insert to authenticated with check ((select auth.uid()) = owner_id);
create policy rr_reviews_delete on public.rr_reviews for delete to authenticated using ((select auth.uid()) = owner_id);

-- Invoker rights retain the caller's RLS. No SECURITY DEFINER or dynamic SQL.
create function public.rr_deletion_counts(item_kind text, item_id uuid)
returns jsonb language plpgsql stable security invoker set search_path = '' as $$
declare class_count bigint := 0; project_count bigint := 0; review_count bigint := 0;
begin
  if item_kind = 'classes' then
    select count(*) into class_count from public.rr_classes where id = item_id;
    select count(*) into project_count from public.rr_projects where class_id = item_id;
    select count(*) into review_count from public.rr_reviews r
      join public.rr_projects p on p.id = r.project_id and p.owner_id = r.owner_id where p.class_id = item_id;
  elsif item_kind = 'projects' then
    select count(*) into project_count from public.rr_projects where id = item_id;
    select count(*) into review_count from public.rr_reviews where project_id = item_id;
  elsif item_kind = 'reviews' then
    select count(*) into review_count from public.rr_reviews where id = item_id;
  else
    raise exception 'Unsupported archive item';
  end if;
  return jsonb_build_object('classes', class_count, 'projects', project_count, 'reviews', review_count);
end;
$$;
revoke all on function public.rr_deletion_counts(text, uuid) from public, anon, authenticated;
grant execute on function public.rr_deletion_counts(text, uuid) to authenticated;
commit;
