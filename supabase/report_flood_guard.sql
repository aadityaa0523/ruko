-- Ruko: server-side flood guard for number reports.
-- Run once in Supabase Dashboard > SQL Editor (project izxqlbipvrtnsvpwekaw).
-- The reporter is a salted hash of the sender's IP; the raw IP is never stored.
alter table public.number_reports add column if not exists reporter text;
create index if not exists number_reports_number_idx on public.number_reports (number, created_at);
create index if not exists number_reports_reporter_idx on public.number_reports (reporter, created_at);

create or replace function public.number_reports_guard() returns trigger
language plpgsql security definer set search_path to '' as $$
declare
  h json := coalesce(nullif(current_setting('request.headers', true), '')::json, '{}'::json);
  ip text := coalesce(h->>'cf-connecting-ip', split_part(h->>'x-forwarded-for', ',', 1), 'unknown');
begin
  new.reporter := encode(sha256(convert_to('ruko-report:' || trim(ip), 'UTF8')), 'hex');
  new.created_at := now();
  if exists (select 1 from public.number_reports r where r.number = new.number
             and r.reporter = new.reporter and r.created_at > now() - interval '30 days') then
    raise exception 'already_reported' using errcode = 'P0001';
  end if;
  if (select count(*) from public.number_reports r where r.reporter = new.reporter
      and r.created_at > now() - interval '1 hour') >= 10 then
    raise exception 'too_many_reports' using errcode = 'P0001';
  end if;
  if (select count(*) from public.number_reports r where r.number = new.number
      and r.created_at > now() - interval '1 hour') >= 30 then
    raise exception 'number_flooded' using errcode = 'P0001';
  end if;
  return new;
end $$;
revoke all on function public.number_reports_guard() from public, anon, authenticated;
drop trigger if exists number_reports_guard on public.number_reports;
create trigger number_reports_guard before insert on public.number_reports
  for each row execute function public.number_reports_guard();

-- Lookups count different reporters, not raw rows.
create or replace function public.number_lookup(p_number text)
returns table(reports bigint, reports_7d bigint, last_reported timestamptz, top_category text)
language sql stable security definer set search_path to '' as $$
  select count(distinct coalesce(r.reporter, r.id::text)),
         count(distinct coalesce(r.reporter, r.id::text)) filter (where r.created_at > now() - interval '7 days'),
         max(r.created_at),
         (select r2.category from public.number_reports r2 where r2.number = p_number
            group by r2.category order by count(distinct coalesce(r2.reporter, r2.id::text)) desc limit 1)
  from public.number_reports r where r.number = p_number;
$$;
