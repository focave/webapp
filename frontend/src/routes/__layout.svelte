<script context="module">
    import { locale, loadTranslations } from '$lib/translations';
    /** @type {import('@sveltejs/kit').Load} */
    export const load = async ({ url }) => {
        const { pathname } = url;
        const defaultLocale = 'pl';
        const initLocale = locale.get() || defaultLocale;
        await loadTranslations(initLocale, pathname);
        return {};
    };
</script>

<script>
    import '../app.css';
    import { onMount } from 'svelte';
    import { browser } from '$app/env';
    import { user } from '$lib/stores';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';
    import updateCount from '$lib/utils/update_count';
    import request from '$lib/utils/request';

    let count = updateCount();

    onMount(async () => {
        if ($user != null) {
            await request('POST', '/token/verify/')
                .then(async (response) => {
                    if (response.status == 200) {
                        return;
                    }
                    if (response.status == 403 || response.status == 400) {
                        user.set(null);
                        if (
                            browser &&
                            $page.url.pathname != '/login' &&
                            $page.url.pathname != '/register'
                        ) {
                            goto('/login');
                        }
                    }
                })
                .catch((error) => {
                    console.error(error);
                });
        }
    });

    if ($count == 0) {
        setInterval(async () => {
            if ($user != null) {
                await request('POST', '/token/refresh/').then(async (response) => {
                    if (response.status == 200) {
                        console.log('/token/refresh: ', response.status);
                    }
                });
            }
        }, 1000 * 60 * 5);
    }
</script>

<slot />
