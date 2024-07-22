<script>
    import Footer from "$lib/Footer.svelte"
    import TeckPage from "$lib/TeckPage.svelte"
	import { get_tip } from "$lib/TeckTip.svelte";
    import { do_update } from "$lib/TeckTip.svelte";
	import { onDestroy } from 'svelte';

    export let tecktip = "";
    export let creator = null;

    export function set_tip() {
        tecktip = "";
        get_tip().then(tip => {
            tecktip = tip.tip;
            creator = tip.by;
        })
    }

    const unsubscribe = do_update.subscribe(value => {
        if (value) {
            do_update.set(false);
            set_tip();
        }
	});

    onDestroy(unsubscribe);
</script>

<TeckPage>
    <div slot="fade" class="flex flex-col items-center justify-center grow">
        <h1 id="tip" class="text-transparent bg-clip-text bg-gradient-to-r from-slate-800 to-black h-full align-middle drop-shadow-3xl lg:text-7xl md:text-6xl text-5xl font-semibold p-10 text-center break-words">
            {tecktip}
        </h1>
    </div>
    <Footer slot="static" submission={creator}/>
</TeckPage>
