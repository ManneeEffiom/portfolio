# Supabase SQL: run in Supabase SQL editor

create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  slug text unique,
  description text,
  stack text[],                -- e.g. ['Python','Flask','MySQL']
  live_url text,
  repo_url text,
  doc_url text,
  published boolean default false,
  featured boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table public.projects enable row level security;

-- Public read access for published projects
create policy "public read published"
  on public.projects for select
  using (published = true);

-- Note: admin writes go through the service-role key on the backend (bypasses RLS).
