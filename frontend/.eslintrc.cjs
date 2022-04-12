module.exports = {
    root: true,
    parser: '@typescript-eslint/parser',
    extends: [
        'prettier',
        'eslint:recommended',
        'plugin:tailwindcss/recommended',
        'plugin:@typescript-eslint/recommended'
    ],
    plugins: ['svelte3', '@typescript-eslint', 'tailwindcss'],
    ignorePatterns: ['*.cjs'],
    overrides: [{ files: ['*.svelte'], processor: 'svelte3/svelte3' }],
    settings: {
        tailwindcss: {
            config: 'tailwind.config.cjs'
        },
        'svelte3/typescript': () => require('typescript')
    },
    parserOptions: {
        sourceType: 'module',
        ecmaVersion: 2020
    },
    env: {
        browser: true,
        es2017: true,
        node: true
    }
};
