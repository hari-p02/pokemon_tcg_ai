import { fixupPluginRules } from '@eslint/compat';
import eslint from '@eslint/js';
import react from 'eslint-plugin-react';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import tseslint from 'typescript-eslint';
import reactRefresh from 'eslint-plugin-react-refresh';
import eslintPluginReactHooks from 'eslint-plugin-react-hooks';
import pluginImport from 'eslint-plugin-import';

export default tseslint.config(
  eslint.configs.recommended,
  eslintPluginPrettierRecommended,
  ...tseslint.configs.recommendedTypeChecked,
  {
    ignores: ['eslint.config.mjs'],
    plugins: {
      'react-refresh': reactRefresh,
      'react-hooks': fixupPluginRules(eslintPluginReactHooks),
      import: pluginImport,
      react,
    },
    languageOptions: {
      parserOptions: {
        project: [
          './*/tsconfig.json',
          './tsconfig.json',
          './tsconfig.vite.json',
        ],
      },
    },
    rules: {
      ...eslintPluginReactHooks.configs.recommended.rules,
      'prettier/prettier': [
        'warn',
        { endOfLine: 'auto' },
      ],
      'react-hooks/exhaustive-deps': 'off',
      '@typescript-eslint/switch-exhaustiveness-check': 'error',
      '@typescript-eslint/restrict-template-expressions': 'off',
      '@typescript-eslint/no-misused-promises': 'off',
      '@typescript-eslint/no-unsafe-enum-comparison': 'off',
      '@typescript-eslint/no-floating-promises': [
        'error',
        {
          ignoreVoid: false,
        },
      ],
      'react-refresh/only-export-components': 'warn',
      '@typescript-eslint/no-unused-vars': [
        'warn',
        {
          vars: 'local',
          argsIgnorePattern: '^_',
          varsIgnorePattern: '^_',
        },
      ],
    },
  },
);
