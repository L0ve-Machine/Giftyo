// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // プロジェクト直下 templates をスキャン
    "../../templates/**/*.html",

    // Django built-in 認証テンプレート（registration）をスキャン
    "../../templates/registration/**/*.html",

    // influencer アプリのテンプレートをスキャン
    "../../influencer/templates/**/*.html",

    // fan アプリがあればスキャン（存在しない場合は不要）
    "../../fan/templates/**/*.html",

    // JavaScript ファイルを動的に使っているなら .js もスキャン
    "../../**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#F28C8C',       // お好きなプライマリカラーに変更OK
        'primary-dark': '#E17575',// ホバー時などに使う少し濃い色
      },
    },
  },
  plugins: [
    require('@tailwindcss/line-clamp'), // line-clamp が不要であればこの行は削除可
  ],
};
