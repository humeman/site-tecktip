<script>
    import { page } from "$app/stores";

    import AnimCodeBlock from "$lib/AnimCodeBlock.svelte";
	import { get_tip } from "$lib/tecktip.js";
    import TeckPage from "$lib/TeckPage.svelte"

    let tips = {
        404: "quick bit!!!!!!! this page is not real. you mayhaps have imapgined it.",
        500: "teck!!! whonnock server is broken  .    what have you done to my    data ?"
    }
    let default_tip = "teck!! tip!!!  ido not know why thuis  happened"
    let errormsg = "none";

    if ($page.error !== null) {
        errormsg = $page.error.message;
    }
    export let tecktip = null;

    export let err_text = [
        `<span class='text-red-500 font-bold'>teck tip tomorrow!</span> the teck man is not working.`,
        tips[$page.status] || default_tip,
        "",
        `<span class='font-bold'>technical details:</span>`,
        `<span class='text-red-500 font-bold'>error.code</span>: <span class='font-bold'>${$page.status}</span>`,
        `<span class='text-red-500 font-bold'>error.msg</span>: <span class='font-bold'>${errormsg}</span>`
    ]

    export function load({ params }) {
        get_tip().then(text => {
            tecktip = `<span class='text-red-500 font-bold'>teck.tip</span>: <span class='font-bold'>${text.tip}</span>`
        })
    }
</script>

<TeckPage>
    <AnimCodeBlock slot="static" code={ err_text } lastitem={ tecktip } />
</TeckPage>