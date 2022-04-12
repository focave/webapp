<!-- Current URL: {$page.url.pathname} -->
<script>
    import { user } from '$lib/stores';
    import request from '$lib/utils/request';
    import { _ } from '$lib/translations';

    async function logout() {
        await request('POST', '/token/delete/')
            .then(async (response) => {
                if (response.status == 200) {
                    user.set(null);
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    async function deleteToken() {
        await request('DELETE', '/users/me/')
            .then(async (response) => {
                if (response.status == 204) {
                    user.set(null);
                }
            })
            .catch((error) => {
                console.error(error);
            });
    }

    const fields = ['text'];
</script>

<div class="flex h-screen w-screen flex-col bg-login-image bg-center">
    <div class="flex flex-1 items-center justify-center">
        <div
            class="min-w-120 grid w-120 grid-cols-1 gap-6 rounded-xl bg-white p-14 shadow-xl dark:bg-slate-900 dark:text-white"
        >
            <div class="justify-self-center">{$_('app.account.title')}</div>

            {#each fields as field}
                {field}
            {/each}

            <button
                on:click|preventDefault={logout}
                class="rounded-md bg-palette-1-150 py-2 px-4 duration-300 ease-in-out hover:bg-palette-1-200 dark:bg-palette-1-350 dark:hover:bg-palette-1-400 dark:disabled:hover:bg-palette-1-350"
            >
                {$_('app.account.logout')}
            </button>
            <button
                on:click|preventDefault={deleteToken}
                class="rounded-md bg-[#AB6C5B] py-2 px-4 duration-300 ease-in-out hover:bg-[#B76355]"
            >
                {$_('app.account.delete')}
            </button>
        </div>
    </div>
</div>
