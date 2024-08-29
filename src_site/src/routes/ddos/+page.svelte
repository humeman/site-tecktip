<script>
    import Footer from "$lib/Footer.svelte"
    import TeckPage from "$lib/TeckPage.svelte"
	import { get } from 'svelte/store';
    import { current_tip, refresh, refresh_no_fade } from "$lib/tecktip.js";
    import { browser } from "$app/environment";

    async function new_tip() {
        if (!browser) return;
        await refresh_no_fade(true);
        window.setTimeout(new_tip, 25);
    }

    new_tip();
</script>

<TeckPage>
    <div slot="fade" class="flex flex-col items-center justify-center justify-items-center grow">
        <h1 id="tip" class="text-transparent bg-clip-text bg-gradient-to-r from-slate-800 to-black drop-shadow-3xl lg:text-7xl md:text-6xl text-4xl font-semibold p-10 text-center break-words">
            {$current_tip.tip}
        </h1>
    </div>
</TeckPage>
