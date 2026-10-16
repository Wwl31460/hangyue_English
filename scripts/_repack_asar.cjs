// 重打包 app.asar（项目内工具脚本）
// 用法：node scripts/_repack_asar.cjs <源目录> <输出.asar>
const asar = require('@electron/asar');

const src = process.argv[2];
const dst = process.argv[3];
if (!src || !dst) {
  console.error('用法: node scripts/_repack_asar.cjs <源目录> <输出.asar>');
  process.exit(2);
}

asar
  .createPackageWithOptions(src, dst, {})
  .then(() => {
    const st = require('fs').statSync(dst);
    console.log('OK ' + dst + ' bytes=' + st.size);
  })
  .catch((e) => {
    console.error('FAIL ' + e.message);
    process.exit(1);
  });
