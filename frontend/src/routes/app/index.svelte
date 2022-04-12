<script>
    import { goto } from '$app/navigation';
    import { _ } from '$lib/translations';
</script>

<div class="flex w-full items-center justify-end p-4">
    <div class="mr-4 h-fit">{$_('app.index.have-account')}</div>
    <div>
        <button
            on:click|preventDefault={() => {
                goto('/app/account');
            }}
            class=" rounded-md bg-white py-2 px-4 drop-shadow-xl duration-150 ease-in-out hover:scale-110 dark:bg-slate-900 dark:text-white"
        >
            {$_('app.index.button')}
        </button>
    </div>
</div>
