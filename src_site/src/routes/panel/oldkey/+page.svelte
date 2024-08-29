<script>
    import { page } from "$app/stores";

    import AnimCodeBlock from "$lib/AnimCodeBlock.svelte";
	import { get_tip, refresh } from "$lib/tecktip.js";
    import TeckPage from "$lib/TeckPage.svelte"
    import { onMount } from "svelte";
    
    export let tecktip = null;

    export let err_text = [
        `<span class='text-red-500 font-bold'>teck tip tomorrow!</span> your api key is outdated.`,
        "",
        `i may or may not have leaked them on github. please send me a message for your new key.`,
        ""
    ]

    onMount(() => {
        refresh(false)
        get_tip().then(text => {
            tecktip = `<span class='font-bold'>teck tip for the trouble</span>: ${text.tip}`
        })
    });
</script>

<TeckPage>
    <AnimCodeBlock slot="static" code={ err_text } lastitem={ tecktip } />
</TeckPage>