/* eslint-env node */
module.exports = {
  env: { browser: true, es2021: true },
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './tsconfig.json',
    tsconfigRootDir: __dirname,
  },
  parser: '@typescript-eslint/parser',
  extends: [
    'airbnb',
    'prettier',
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
    'plugin:react-hooks/recommended',
    'plugin:prettier/recommended',
  ],
  plugins: ['react', '@typescript-eslint', 'import', 'jsx-a11y', 'react-hooks'],
  rules: {
    'prettier/prettier': 0,
    'no-console': ['off'],
    'no-alert': ['off'],
    'import/no-unresolved': ['off'],
    'import/extensions': ['off'],
    'import/prefer-default-export': ['off'],
    'import/no-extraneous-dependencies': ['off'],
    'react/jsx-filename-extension': [1, { extensions: ['.js', '.jsx', '.tsx'] }],
    'react/function-component-definition': [0, { namedcomponents: 'arrow-function' }],
    'react/require-default-props': ['off'],
    'react/jsx-props-no-spreading': ['off'],
    'react/no-array-index-key': ['off'],
    'react-hooks/exhaustive-deps': ['off'],
    'jsx-a11y/control-has-associated-label': ['off'],
    'jsx-a11y/click-events-have-key-events': ['off'],
    'jsx-a11y/no-noninteractive-element-interactions': ['off'],
    'jsx-a11y/no-static-element-interactions': ['off'],
    'jsx-a11y/media-has-caption': ['off'],
    camelcase: ['off'],
    '@typescript-eslint/no-non-null-assertion': ['off'],
    '@typescript-eslint/no-non-null-asserted-optional-chain': ['off'],
  },
}
