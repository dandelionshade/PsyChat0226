import globals from "globals";
import pluginJs from "@eslint/js";
import pluginVue from "eslint-plugin-vue";


/** @type {import('eslint').Linter.Config[]} */
export default [
  {files: ["**/*.{js,mjs,cjs,vue}"]},
  {files: ["**/*.js"], languageOptions: {sourceType: "commonjs"}},
  {languageOptions: { globals: globals.browser }},
  pluginJs.configs.recommended,
  ...pluginVue.configs["flat/essential"],
];

//下面的代码需要考虑清楚并明确好要求后再使用：
module.exports = {
  env: {
      browser: true,
      es2021: true,
      node: true, // 如果你的代码需要在 Node.js 环境运行，则添加此项
  },
  extends: [
      'eslint:recommended', // Eslint 推荐规则
      'plugin:vue/vue3-essential', // Vue 3 基本规则
      'airbnb-base', // Airbnb 风格指南
      'plugin:prettier/recommended', // 整合 Prettier
  ],
  parserOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
  },
  plugins: [
      'vue',
      'prettier', // 启用 Prettier 插件
  ],
  rules: {
      // 自定义规则 (可以根据需要添加或修改)
      'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off', // 生产环境禁用 console
      'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off', // 生产环境禁用 debugger
      'prettier/prettier': 'error', // Prettier 错误提示
      'vue/multi-word-component-names': 'off', // 关闭 Vue 组件命名警告
      'import/extensions': 'off', // 允许省略导入文件的扩展名
      'import/no-extraneous-dependencies': 'off', // 允许使用未在 package.json 中声明的依赖
      'import/prefer-default-export': 'off', // 允许不使用默认导出
      'no-param-reassign': 'off',  //允许函数参数重新赋值
      'consistent-return': 'off',   //允许函数返回值类型不一致
      'no-unused-vars': 'warn'    // 未使用变量警告
  },
};
/*
########.eslintrc.js

env: 指定代码运行环境。
extends: 继承的规则集。
eslint:recommended: Eslint 推荐规则。
plugin:vue/vue3-essential: Vue 3 基本规则。
airbnb-base: Airbnb 风格指南 (也可以选择其他风格指南)。
plugin:prettier/recommended: 整合 Prettier，将 Prettier 的规则作为 Eslint 的规则来使用。
parserOptions: 指定 JavaScript 语法版本和模块类型。
plugins: 使用的插件。
vue: Vue.js 插件。
prettier: Prettier 插件。
rules: 自定义规则。
no-console: 生产环境禁用 console.log 等语句。
no-debugger: 生产环境禁用 debugger 语句。
prettier/prettier: 将 Prettier 的规则作为 Eslint 的规则来使用，如果代码不符合 Prettier 的格式，则会报错。
vue/multi-word-component-names: 关闭 Vue 组件命名警告。
import/extensions: 允许省略导入文件的扩展名。
import/no-extraneous-dependencies: 允许使用未在 package.json 中声明的依赖。
import/prefer-default-export: 允许不使用默认导出。
*/