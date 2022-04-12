<script>
    import { _ } from '$lib/translations';
    import { goto } from '$app/navigation';
</script>

<div class="flex h-screen w-screen flex-col bg-login-image bg-center ">
    <div class="flex flex-1 items-center justify-center">
        <div
            class="min-w-120 grid w-120 grid-cols-1 gap-6 rounded-xl bg-white p-14 shadow-xl dark:bg-slate-900 dark:text-white"
        >
            <div class="justify-self-center">{$_('index.title')}</div>
            <div class="flex">
                <button
                    class="m-2 flex-1 rounded-md bg-palette-1-150 py-2 px-4 shadow-md duration-300 ease-in-out  hover:bg-palette-1-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-inner  disabled:hover:bg-palette-1-150 dark:bg-palette-1-350 dark:text-white dark:hover:bg-palette-1-400 dark:disabled:hover:bg-palette-1-350"
                    on:click={() => goto('/login')}
                >
                    {$_('index.login')}
                </button>
                <button
                    class="m-2 flex-1 rounded-md bg-palette-1-150 py-2 px-4 shadow-md duration-300 ease-in-out  hover:bg-palette-1-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-inner  disabled:hover:bg-palette-1-150 dark:bg-palette-1-350 dark:text-white dark:hover:bg-palette-1-400 dark:disabled:hover:bg-palette-1-350"
                    on:click={() => goto('/register')}
                >
                    {$_('index.register')}
                </button>
            </div>
        </div>
    </div>
</div>
