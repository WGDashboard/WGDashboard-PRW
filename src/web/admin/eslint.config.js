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
      parserOptions: {
        parser: "@typescript-eslint/parser",
      },
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
      "no-empty": "warn",
      "no-redeclare": "warn",
      "no-undef": "warn",
      "no-unexpected-multiline": "warn",
      "no-unused-vars": "warn",
      "no-useless-assignment": "warn",
      complexity: ["warn", 10],
      "max-depth": ["warn", 3],
      "max-lines": [
        "warn",
        { max: 250, skipBlankLines: true, skipComments: true },
      ],
      "vue/multi-word-component-names": "warn",
      "vue/no-dupe-keys": "warn",
      "vue/no-duplicate-attributes": "warn",
      "vue/no-mutating-props": "warn",
      "vue/no-parsing-error": "warn",
      "vue/no-ref-as-operand": "warn",
      "vue/no-reserved-component-names": "warn",
      "vue/no-unused-components": "warn",
      "vue/no-unused-vars": "warn",
      "vue/no-use-v-if-with-v-for": "warn",
      "vue/require-prop-type-constructor": "warn",
      "vue/require-v-for-key": "warn",
      "vue/return-in-computed-property": "warn",
      "vue/valid-template-root": "warn",
      "vue/valid-v-else": "warn",
      "vue/valid-v-for": "warn",
      "vue/valid-v-if": "warn",
    },
  },
];
