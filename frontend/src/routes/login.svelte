<script lang="ts">
    import * as svelteForms from 'svelte-forms';
    import * as validators from 'svelte-forms/validators';
    import { user } from '$lib/stores';
    import { browser } from '$app/env';
    import Field from '$lib/components/Field.svelte';
    import { goto } from '$app/navigation';
    import request from '$lib/utils/request';
    import { _ } from '$lib/translations';

    $: if (browser && $user != null) {
        goto('/app/account');
    }

    const email = svelteForms.field('email', '', [validators.required(), validators.email()], {
        validateOnChange: false
    });
    const password = svelteForms.field('password', '', [validators.required()], {
        validateOnChange: false
    });

    const form = svelteForms.form(email, password);

    let loginErrors = Promise.resolve([]);
    async function login() {
        let errors = [];
        await request('POST', '/token/', {
            email: $email.value,
            password: $password.value
        })
            .then(async (response) => {
                await response.json().then((data) => {
                    if (response.status == 200) {
                        user.set({ email: $email.value });
                    } else if (response.status == 400) {
                        if (data.email && data.email.includes('This field may not be blank.')) {
                            errors.push('Email may not be blank');
                        }
                        if (
                            data.password &&
                            data.password.includes('This field may not be blank.')
                        ) {
                            errors.push('Password may not be blank');
                        }
                    } else if (response.status == 401) {
                        errors.push('Invalid email or password');
                    } else {
                        errors.push(`Unexpected response ${response.status}`);
                    }
                });
            })
            .catch((error) => {
                console.error(error);
                errors.push('Unexpected error happened');
            });
        return errors;
    }
</script>

<div class="flex  h-screen w-screen flex-col bg-login-image bg-center">
    <div class="flex w-full items-center justify-end p-4">
        <div class="mr-4 h-fit">{$_('login.have-account')}</div>
        <div>
            <a href="/register">
                <button
                    class=" rounded-md bg-white py-2 px-4 drop-shadow-xl duration-150 ease-in-out hover:scale-110 dark:bg-slate-900 dark:text-white"
                >
                    {$_('login.register')}
                </button>
            </a>
        </div>
    </div>
    <div class="flex flex-1 items-center justify-center">
        <div
            class="min-w-120 grid w-120 grid-cols-1 gap-6 rounded-xl bg-white p-14 shadow-xl dark:bg-slate-900 dark:text-white"
        >
            <div class="justify-self-center">{$_('login.title')}</div>
            <Field field={email} label={$_('login.email')} type="email">
                {#if $form.hasError('email.required')}
                    {$_('login.email-required')}
                {:else if $form.hasError('email.not_an_email')}
                    {$_('login.email-invalid')}
                {/if}
            </Field>

            <Field field={password} label={$_('login.password')} type="password">
                {#if $form.hasError('password.required')}
                    {$_('login.password-required')}
                {/if}
            </Field>

            {#await loginErrors then errors}
                {#if errors.length > 0}
                    <div class="text-red-400">
                        {#each errors as error}
                            {error}<br />
                        {/each}
                    </div>
                {/if}
            {/await}
            <button
                disabled={!$form.valid}
                on:click|preventDefault={() => {
                    loginErrors = login();
                }}
                class="rounded-md bg-palette-1-150 py-2 px-4 shadow-md duration-300 ease-in-out  hover:bg-palette-1-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-inner  disabled:hover:bg-palette-1-150 dark:bg-palette-1-350 dark:text-white dark:hover:bg-palette-1-400 dark:disabled:hover:bg-palette-1-350"
            >
                {$_('login.login')}
            </button>
        </div>
    </div>
</div>
