<script>
    import { browser } from '$app/env';
    import { user } from '$lib/stores';
    import { page } from '$app/stores';
    import { goto } from '$app/navigation';

    $: if (browser && $page.url.pathname != '/login' && $user == null) {
        goto('/login');
    }
</script>

<slot />
