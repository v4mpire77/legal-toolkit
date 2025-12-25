-- Users table is handled by Supabase Auth (auth.users)
-- We need a public table for Cases that references the auth user.

create table public.cases (
  id uuid default gen_random_uuid() primary key,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  user_id uuid references auth.users not null,
  title text not null,
  case_type text not null, -- 'deadline', 'bundle', 'fee', etc.
  data jsonb not null, -- Stores the actual calculation data
  description text
);

-- Enable Row Level Security (RLS)
alter table public.cases enable row level security;

-- Create Policy: Users can only see their own cases
create policy "Users can view own cases" on public.cases
  for select using (auth.uid() = user_id);

-- Create Policy: Users can insert their own cases
create policy "Users can insert own cases" on public.cases
  for insert with check (auth.uid() = user_id);

-- Create Policy: Users can delete their own cases
create policy "Users can delete own cases" on public.cases
  for delete using (auth.uid() = user_id);
