
module.exports = {
  plugins: [
    // Tailwind のコアプラグインを require で読み込む
    require('tailwindcss'),
    // autoprefixer を使うなら入れる（不要なら削除可）
    require('autoprefixer'),
    // postcss-simple-vars, postcss-nested はお好みで
    require('postcss-simple-vars'),
    require('postcss-nested'),
  ]
};
