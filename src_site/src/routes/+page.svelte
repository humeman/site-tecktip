<script>
    import Footer from "$lib/Footer.svelte"
    import TeckPage from "$lib/TeckPage.svelte"
	import { get } from 'svelte/store';
    import { current_tip } from "$lib/tecktip.js";
</script>

<TeckPage>
    <div slot="fade" class="flex flex-col items-center justify-center justify-items-center grow">
        <h1 id="tip" class="text-transparent bg-clip-text bg-gradient-to-r from-slate-800 to-black drop-shadow-3xl lg:text-7xl md:text-6xl text-4xl font-semibold p-10 text-center break-words">
            {$current_tip.tip}
        </h1>
    </div>
    <Footer slot="static" submission={$current_tip.by}/>
</TeckPage>
