// 校验：把 src/lib/edgeTts.ts 里的 v2 令牌函数转译后，与官方 Python 的基准值比对。
// 仅用于开发期验证，不参与打包。
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { transform } from 'esbuild';

const src = readFileSync(new URL('../src/lib/edgeTts.ts', import.meta.url), 'utf8');
// 仅为测试把内部函数暴露出来（不改动源文件本身）
const patched = src.replace('function secMsGec(', 'export function secMsGec(');
const out = await transform(patched, { loader: 'ts', format: 'esm', target: 'node20' });
const dir = mkdtempSync(join(tmpdir(), 'gec-'));
const file = join(dir, 'edgeTts.mjs');
writeFileSync(file, out.code);
const { secMsGec } = await import('file://' + file);

const expected = {
  1700000000: '2CD23A2CA0B2595A-F3C846C370E05F9CC83ACC5F995C5F5D87A4D0F14CE8936A0F902E64099E38A2',
  1730000000: '50065ABF67B90F95-49BDAF24D28ECEB38DAEEC84DEAA71E91F92945EA8A47921C58FB4F8F79A4F5E',
  1800000000: '99E54519B490BE5C-E162DB0977FBDCB9B86DD8148BF1BCDC3C0303176CE39852A42B415935C20654',
};

let pass = 0;
for (const [ts, want] of Object.entries(expected)) {
  const got = secMsGec(Number(ts));
  const ok = got === want;
  if (ok) pass++;
  console.log(`${ok ? 'PASS' : 'FAIL'} t=${ts}\n  got=${got}\n  exp=${want}`);
}
console.log(pass === 3 ? '\n全部一致 ✅' : '\n存在不一致 ❌');
process.exit(pass === 3 ? 0 : 1);
