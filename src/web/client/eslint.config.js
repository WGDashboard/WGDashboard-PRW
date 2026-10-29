import js from "@eslint/js";
import globals from "globals";
import vue from "eslint-plugin-vue";

export default [
  {
    ignores: ["dist/**", "node_modules/**"],
  },
  js.configs.recommended,
  ...vue.configs["flat/recommended"],
  {
    files: ["**/*.{js,vue}"],
    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    rules: {
      // Prettier owns template layout, so style rules should not duplicate its checks.
      "vue/attribute-hyphenation": "off",
      "vue/attributes-order": "off",
      "vue/component-definition-name-casing": "off",
      "vue/first-attribute-linebreak": "off",
      "vue/html-closing-bracket-newline": "off",
      "vue/html-closing-bracket-spacing": "off",
      "vue/html-indent": "off",
      "vue/html-self-closing": "off",
      "vue/max-attributes-per-line": "off",
      "vue/mustache-interpolation-spacing": "off",
      "vue/multiline-html-element-content-newline": "off",
      "vue/no-multi-spaces": "off",
      "vue/order-in-components": "off",
      "vue/singleline-html-element-content-newline": "off",
      "vue/this-in-template": "off",
      "vue/v-on-event-hyphenation": "off",
      // Report existing legacy UI violations without blocking its first lint rollout.
      "no-unused-vars": "warn",
      complexity: ["warn", 10],
      "max-depth": ["warn", 3],
      "max-lines": [
        "warn",
        { max: 250, skipBlankLines: true, skipComments: true },
      ],
      "vue/multi-word-component-names": "warn",
      "vue/no-mutating-props": "warn",
      "vue/no-ref-as-operand": "warn",
      "vue/require-v-for-key": "warn",
      "vue/valid-v-for": "warn",
    },
  },
];
