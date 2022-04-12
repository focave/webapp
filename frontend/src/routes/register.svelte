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
    const password = svelteForms.field(
        'password',
        '',
        [
            validators.required(),
            (() => (value: string) => ({ valid: value.toString().length >= 8, name: 'length' }))(),
            validators.not(validators.pattern(/^[0-9]*$/))
        ],
        {
            validateOnChange: true
        }
    );
    const password2 = svelteForms.field(
        'password2',
        '',
        [validators.required(), validators.matchField(password)],
        {
            validateOnChange: false
        }
    );

    const form = svelteForms.form(email, password, password2);

    let registerErrors = Promise.resolve([]);

    async function register() {
        let errors = [];
        await request('POST', '/users/', {
            email: $email.value,
            password: $password.value
        })
            .then(async (response) => {
                await response.json().then((data) => {
                    console.log(response.status);
                    console.log(data);

                    if (response.status == 201) {
                        if (browser) {
                            goto('/login');
                        }
                    } else if (response.status == 400) {
                        if (data.email && data.email.includes('This field may not be blank.')) {
                            errors.push('Email may not be blank');
                        }
                        if (data.email && data.email.includes('Enter a valid email address.')) {
                            errors.push('Email may not be blank');
                        }
                        if (
                            data.password &&
                            data.password.includes('This field may not be blank.')
                        ) {
                            errors.push('Password may not be blank');
                        }
                        if (
                            data.password &&
                            data.password.includes('This password is too common.')
                        ) {
                            errors.push('This password is too common.');
                        }
                        if (
                            data.password &&
                            data.password.includes('This password is entirely numeric.')
                        ) {
                            errors.push('This password is entirely numeric.');
                        }
                        if (
                            data.password &&
                            data.password.includes(
                                'This password is too short. It must contain at least 8 characters.'
                            )
                        ) {
                            errors.push(
                                'This password is too short. It must contain at least 8 characters.'
                            );
                        }
                        if (data.password) {
                            let match = data.password.find((value) =>
                                /^The password is too similar to the/.test(value)
                            );
                            if (match) {
                                errors.push(match);
                            }
                        }
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
        <div class="mr-4 h-fit">{$_('register.have-account')}</div>
        <div>
            <a href="/login">
                <button
                    class=" rounded-md  bg-slate-900 py-2 px-4 text-white drop-shadow-xl duration-150 ease-in-out hover:scale-110"
                >
                    {$_('register.login')}
                </button>
            </a>
        </div>
    </div>
    <div class="flex flex-1 items-center justify-center">
        <div
            class="min-w-120 grid w-120 grid-cols-1 gap-6 rounded-xl bg-white p-14 shadow-xl dark:bg-slate-900 dark:text-white "
        >
            <div class="justify-self-center">{$_('register.title')}</div>
            <Field field={email} label={$_('register.email')} type="email">
                {#if $form.hasError('email.required')}
                    {$_('register.email-required')}
                {:else if $form.hasError('email.not_an_email')}
                    {$_('register.email-invalid')}
                {/if}
            </Field>

            <Field field={password} label={$_('register.password')} type="password" on:input={() => password2.validate()}>
                {#if $form.hasError('password.required')}
                    {$_('register.password-required')}<br />
                {:else}
                    {#if $form.hasError('password.min')}
                        {$_('register.password-too-short')}<br />
                    {/if}
                    {#if $form.hasError('password.pattern')}
                        {$_('register.password-numeric')}
                    {/if}
                {/if}
            </Field>

            <Field field={password2} label={$_('register.password-repeat')} type="password">
                {#if $form.hasError('password2.match_field')}
                    {$_('register.passwords-diffrent')}
                {/if}
            </Field>

            {#await registerErrors then errors}
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
                    registerErrors = register();
                }}
                class="rounded-md bg-palette-1-150 py-2 px-4 shadow-md duration-300 ease-in-out  hover:bg-palette-1-200 disabled:cursor-not-allowed disabled:opacity-50 disabled:shadow-inner  disabled:hover:bg-palette-1-150 dark:bg-palette-1-350 dark:text-white dark:hover:bg-palette-1-400 dark:disabled:hover:bg-palette-1-350"
            >
                {$_('register.register')}
            </button>
        </div>
    </div>
</div>
