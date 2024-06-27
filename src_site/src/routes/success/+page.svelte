<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";

    import { page } from "$app/stores"
    import { browser } from "$app/environment"
    import { goto } from "$app/navigation"

    let messages = {
        "create": "submission id '%uuid%' sent successfully. our curators will review it shortly. lingules thanks you 👍"
    }

    let message = "";

    function update_params() {
        if (!browser) return;

        let params = {}
        console.log("running")
        for (const [key, value] of $page.url.searchParams.entries()) {
            params[key] = value;
        }

        let placeholder = messages[params["event"]];

        for (let param in params) {
            let val = params[param];

            placeholder = placeholder.replace(`%${param}%`, val);
        }

        message = placeholder;
    }

    $: $page.url.searchParams, update_params();

    function goto_home() {
        if (browser) {
            goto("/")
        }
    }
</script>

<TeckPage>
    <Container slot="static" title={ "success"}>
        <p class="text-lg sm:text-xl md:text-2xl text-slate-100 p-2 mb-10 text-center">
            {message}
        </p>

        <button on:click={goto_home} class="transition-all ease-in-out rounded-full bg-slate-600/75 text-slate-100  pl-8 pr-8 md:pl-10 md:pr-10 lg:pl-12 lg:pr-12 pt-4 pb-4 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">home</button>
    </Container>
</TeckPage>