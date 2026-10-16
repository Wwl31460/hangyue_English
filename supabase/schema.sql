-- =========================================================
-- 航悦英语 · 账号与进度 数据库（Supabase / PostgreSQL）
-- 在 Supabase 控制台 → SQL Editor 中“新建查询”→ 粘贴本文件 → 点“运行”一次即可。
--
-- 说明（给老师/管理员看，不用懂技术）：
--   1) 账号本身由 Supabase 自带的“认证”功能管理，不需要在这里建表；
--   2) 我们只要一张表 user_progress，把每个学生的【全部学习进度】存成一个整体；
--   3) 数据安全靠 RLS（行级安全）：每个学生只能读写自己的那一行的数据。
--
-- 学生账号怎么建：见本文件最底部“建账号步骤”，不去碰这张表。
-- =========================================================

-- 进度表：一个学生一行，data 里是完整的进度（星星/积分/已学单词/单元错词本/当前单元等）
create table if not exists public.user_progress (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  display_name text,                 -- 显示名（默认取用户名）
  current_grade text,                -- 当前年级，如 'g6s1'（用于首页“继续学习”）
  current_unit  int,                 -- 当前单元，如 1
  data         jsonb not null default '{}'::jsonb,  -- 完整进度（前端整份存取）
  updated_at   timestamptz not null default now()
);

-- 开启行级安全：不开的话任何人都能读全表，开了之后每条读写都会校验“是不是本人”
alter table public.user_progress enable row level security;

-- 本人可读
drop policy if exists "本人可读" on public.user_progress;
create policy "本人可读" on public.user_progress
  for select using (auth.uid() = user_id);

-- 本人可写（插入/更新都受此策略约束）
drop policy if exists "本人可写" on public.user_progress;
create policy "本人可写" on public.user_progress
  for insert with check (auth.uid() = user_id);
drop policy if exists "本人可改" on public.user_progress;
create policy "本人可改" on public.user_progress
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- 新账号建好后，自动在进度表里插一行空进度（这样前端首次读取不会报错）
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = public
as $$
begin
  insert into public.user_progress (user_id, display_name, data)
  values (
    new.id,
    coalesce(new.raw_user_meta_data->>'username', split_part(new.email, '@', 1)),
    '{}'::jsonb
  )
  on conflict (user_id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- =========================================================
-- 建学生账号（在 App 内完成，不用填邮箱）：
--   1) 老师打开 App → 「我的」页底部 → 「老师后台（添加学生账号）」→ 输入老师口令进入；
--   2) 填「用户名」（中文或英文都行，如 小明 / xiaoming）+「密码」（至少 6 位）+ 确认密码 → 点“添加学生”；
--   3) 系统自动生成底层账号并写入进度表，学生打开 App 用「用户名 + 密码」即可登录。
--   邮箱由系统按用户名自动生成（英文→用户名@hangyue.local；中文→编码后的合法邮箱），老师/学生都不用管。
--
-- 后台只需准备一次（老师不用碰）：
--   A) 本文件在 Supabase 控制台 SQL Editor 运行一次（建表 + 策略 + 触发器）；
--   B) Supabase 控制台 → Authentication → Providers → Email → 关闭 “Confirm email”
--      （这样学生账号添加后无需点验证邮件即可直接登录）。
-- =========================================================
