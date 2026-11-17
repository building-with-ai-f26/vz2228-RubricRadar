# Create your Supabase account and project

For the builder · November 17, 2026. You create the account/project yourself;
we will connect it after the security checks. The local sample works without it.

1. Open [Supabase Dashboard](https://supabase.com/dashboard), create an account
   or sign in with GitHub, and complete any verification yourself.
2. Create/select your own organization and select the **Free** plan for this prototype.
   Supabase currently lists a free tier; check the displayed plan before proceeding.
   No paid upgrade is needed for this setup step. See [official pricing](https://supabase.com/pricing).
3. Create a **New project**, named **Rubric Radar**. Choose a nearby US region
   (East US if offered for your account). Set a strong database password and keep
   it in your password manager. This database password is separate from students'
   future Rubric Radar passwords; do not paste it into chat or the app.
4. Wait until the project dashboard is ready. Tell the agent **“My Supabase project
   is ready.”** Account/project creation alone does not configure the app's tables
   or prove security. Do not add real coursework yet.

Next, together: review/apply the repository's migration in the intended test project,
run the rollback-only security script and direct two-account API checks, configure
Auth email confirmation/recovery, then connect the app and verify live behavior.
See [technical setup](./supabase.md) and [security register](../../SECURITY.md).
The agent has not created an account, applied a migration or changed any cloud settings.

When configuring locally, find the Project URL in **Connect** and the **publishable**
key (starts `sb_publishable_`) in Connect or **Settings → API Keys**. Put those fields
in the ignored local `.env`, using `.env.example` as a reference. Keep
`RUBRIC_RADAR_ARCHIVE_ENABLED=false` until actual database isolation is verified.
Do not send database passwords, secret/service-role keys or auth tokens in chat.

Sources: [official project creation guide](https://supabase.com/docs/guides/getting-started/quickstarts/flask),
[official API key guide](https://supabase.com/docs/guides/getting-started/api-keys).
The public-read sample-table policy in the generic quickstart is not our private
archive policy; use the repository's reviewed migration for Rubric Radar.
