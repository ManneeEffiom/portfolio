-- Tables are auto-created by SQLAlchemy (db.create_all) on first run.
-- This DDL is provided for reference / manual setup in Supabase.

create table if not exists public.projects (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  slug text unique not null,
  description text,
  stack text[],
  live_url text,
  repo_url text,
  doc_url text,
  published boolean default false,
  featured boolean default false,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
