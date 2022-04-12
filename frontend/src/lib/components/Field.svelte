<script>
    export let field;
    export let type;
    export let label = '';
    export let required = false;
    let random = Math.floor(Math.random() * (99999 - 10000) + 10000).toString();
    function setType(node, type) {
        node.type = type;
    }
    function focusOut() {
        field.validate();
    }
</script>

<div
    class="
        flex 
        flex-col 
        bg-inherit
        "
>
    <div
        class="
            text-md 
            relative 
            rounded-md 
            bg-inherit
            p-2
            text-left 
            shadow-md  
            outline
            outline-1 
            outline-slate-400
            focus-within:outline-2
            focus-within:outline-palette-1-250
            hover:outline-slate-200
            focus-within:hover:outline-palette-1-250
            "
        class:outline-red-400={$field.invalid}
    >
        <div class="relative bg-inherit">
            <input
                on:focusout={focusOut}
                class="
                    text-md 
                    w-full
                    border-0 
                    bg-inherit 
                    p-0 
                    text-white 
                    transition-autofill
                    delay-[86400000ms]
                    ease-in-out  
                    focus:border-0 
                    focus:ring-0
                    "
                id={random}
                name={$field.name}
                bind:value={$field.value}
                use:setType={type}
                on:input
                {required}
                placeholder=" "
            />

            <label class="absolute left-0  bg-inherit text-white duration-300" for={random}>
                {label}
            </label>
        </div>
    </div>
    <div class="text-red-400">
        <slot />
    </div>
</div>

<style lang="postcss">
    input:focus ~ label,
    input:not(:placeholder-shown) ~ label {
        @apply left-0 origin-top-left -translate-y-5 scale-90 transform px-2;
    }
</style>
