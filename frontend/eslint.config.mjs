import globals from "globals";
import pluginJs from "@eslint/js";
import tseslint from "typescript-eslint";
import pluginVue from "eslint-plugin-vue";


export default [
    {files: ["**/*.{js,mjs,cjs,ts,vue}"]},
    {languageOptions: { globals: globals.browser }},
    pluginJs.configs.recommended,
    ...tseslint.configs.recommended,
    ...pluginVue.configs["flat/essential"],
    {
        rules: {
            "indent": ["error", 4],
            "no-mixed-spaces-and-tabs": "error", // Prevent mixed spaces and tabs
        }
    },
    {
        files: ["**/*.vue"], languageOptions: {parserOptions: {parser: tseslint.parser}},
        rules: {
            // Enforce 4-space indentation
            "indent": ["error", 4],
            "vue/html-indent": ["error", 4],
            "vue/script-indent": ["error", 4, { baseIndent: 0, switchCase: 1 }],

            // Ensure automatic fixes
            "no-mixed-spaces-and-tabs": "error", // Prevent mixed spaces and tabs
        }
    },
];