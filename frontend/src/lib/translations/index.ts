import i18n from 'sveltekit-i18n';
import lang from './lang.json';

/** @type {import('sveltekit-i18n').Config} */
export const config = {
    translations: {
        en: { lang },
        pl: { lang }
    },
    loaders: [
        {
            locale: 'en',
            key: 'index',
            routes: ['/'],
            loader: async () => (await import('./en/index.json')).default
        },
        {
            locale: 'en',
            key: 'login',
            routes: ['/login'],
            loader: async () => (await import('./en/login.json')).default
        },
        {
            locale: 'en',
            key: 'register',
            routes: ['/register'],
            loader: async () => (await import('./en/register.json')).default
        },
        {
            locale: 'en',
            key: 'app/account',
            routes: ['/app/account'],
            loader: async () => (await import('./en/app/account.json')).default
        },
        {
            locale: 'en',
            key: 'app/index',
            routes: ['/app/index'],
            loader: async () => (await import('./en/app/index.json')).default
        },
        {
            locale: 'en',
            key: 'app.account',
            routes: ['/app/account'],
            loader: async () => (await import('./en/app/account.json')).default
        },
        {
            locale: 'en',
            key: 'app.index',
            routes: ['/app'],
            loader: async () => (await import('./en/app/index.json')).default
        },

        {
            locale: 'pl',
            key: 'index',
            routes: ['/'],
            loader: async () => (await import('./pl/index.json')).default
        },
        {
            locale: 'pl',
            key: 'login',
            routes: ['/login'],
            loader: async () => (await import('./pl/login.json')).default
        },
        {
            locale: 'pl',
            key: 'register',
            routes: ['/register'],
            loader: async () => (await import('./pl/register.json')).default
        },
        {
            locale: 'pl',
            key: 'app.account',
            routes: ['/app/account'],
            loader: async () => (await import('./pl/app/account.json')).default
        },
        {
            locale: 'pl',
            key: 'app.index',
            routes: ['/app'],
            loader: async () => (await import('./pl/app/index.json')).default
        }
    ]
};

export const { t: _, loading, locales, locale, loadTranslations } = new i18n(config);

loading.subscribe(($loading) => $loading && console.log('Loading translations...'));
