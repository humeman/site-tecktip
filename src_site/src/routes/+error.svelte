<script>
    import { page } from "$app/stores";

    import AnimCodeBlock from "$lib/AnimCodeBlock.svelte";
	import { get_tip } from "$lib/TeckTip.svelte";
    import TeckPage from "$lib/TeckPage.svelte"

    let tips = {
        404: "the page requested couldn't be found - check your spelling and try again.",
        500: "the error happened on my end - feel free to report this to me!"
    }
    let default_tip = "please try again soon, or report the issue to me if it persists."
    let errormsg = "none";

    if ($page.error !== null) {
        errormsg = $page.error.message;
    }
    export let tecktip = null;

    get_tip().then(text => {
        tecktip = `<span class='text-red-500 font-bold'>teck.tip</span>: <span class='font-bold'>${text}</span>`
    })

    export let err_text = [
        "<span class='text-green-500 font-bold'>visitor@tecktip</span>:<span class='text-blue-500'>~</span>$ ./error",
        "",
        `<span class='text-red-500 font-bold'>oops!</span> something went wrong while processing that request.`,
        tips[$page.status] || default_tip,
        "",
        `<span class='font-bold'>technical details:</span>`,
        `<span class='text-red-500 font-bold'>error.code</span>: <span class='font-bold'>${$page.status}</span>`,
        `<span class='text-red-500 font-bold'>error.msg</span>: <span class='font-bold'>${errormsg}</span>`
    ]
</script>

<TeckPage>
    <AnimCodeBlock slot="static" code={ err_text } title={ "visitor@tecktip:~$ error" } lastitem={ tecktip } />
</TeckPage>