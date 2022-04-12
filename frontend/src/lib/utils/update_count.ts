import { writable } from 'svelte/store';
import { afterUpdate } from 'svelte';

export default function updateCount() {
    const count = writable(0);
    afterUpdate(() => {
        count.update((c) => c + 1);
    });
    return count;
}
