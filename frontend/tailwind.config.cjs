//const { fontFamily } = require('tailwindcss/defaultTheme'); //kill me

const plugin = require('tailwindcss/plugin');
const flatten = require('flatten-tailwindcss-theme');

module.exports = {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        extend: {
            colors: {
                celeste: {
                    500: '#80FFF4',
                    400: '#99FFF7',
                    300: '#B3FFF9',
                    200: '#CCFFFB',
                    100: '#E5FFFD'
                },
                palette: {
                    1: {
                        50: '#99E2B4',
                        100: '#88D4AB',
                        150: '#78C6A3',
                        200: '#67B99A',
                        250: '#56AB91',
                        300: '#469D89',
                        350: '#358F80',
                        400: '#248277',
                        450: '#14746F',
                        500: '#036666'
                    }
                }
            },
            spacing: {
                100: '25rem',
                108: '27rem',
                120: '30rem'
            },
            backgroundImage: {
                'login-image': "url('/img/login-image.jpg')"
            },
            fontFamily: {
                sans: ['Exo\\ 2', 'sans-serif']
            },
            transitionProperty: {
                autofill: 'background-color, color, font-size, font-family'
            }
        }
    },
    variants: {
        extends: {
            shadowFill: ['autofill', 'dark'],
            textFill: ['autofill', 'dark']
        }
    },
    plugins: [
        require('@tailwindcss/forms'),
        plugin(
            ({ addUtilities, variants, theme, e }) => {
                const colors = flatten(theme('colors'));
                const utils = Object.entries(colors).reduce(
                    (res, [key, value]) =>
                        Object.assign(res, {
                            [`.${e(`text-fill-${key}`)}`]: {
                                '-webkit-text-fill-color': value
                            }
                        }),
                    {}
                );
                addUtilities(utils, variants('textFill'));
            },
            { variants: { textFill: [] } }
        ),
        plugin(
            ({ addUtilities, variants, theme, e }) => {
                const colors = flatten(theme('colors'));
                const utils = Object.entries(colors).reduce(
                    (res, [key, value]) =>
                        Object.assign(res, {
                            [`.${e(`shadow-fill-${key}`)}`]: {
                                '--tw-shadow': `0 0 0 9999px ${value} inset`,
                                boxShadow:
                                    'var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow)'
                            }
                        }),
                    {}
                );
                addUtilities(utils, variants('shadowFill'));
            },
            { variants: { shadowFill: [] } }
        )
    ]
};
