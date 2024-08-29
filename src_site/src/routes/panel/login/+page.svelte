<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { goto } from "$app/navigation"
    import { browser } from "$app/environment"
    import { refresh } from "$lib/tecktip";
    import { onMount } from "svelte";
    import { redirect } from "@sveltejs/kit";
    import { check_key } from "$lib/auth";

    let api_key;
    let error = null;

    let legacy = [
        "abc",
        "def",
        "ghi"
    ]


    async function sign_in() {
        if (legacy.includes(api_key)) {
            goto("panel/oldkey");
            return;
        }

        let valid;
        try {
            valid = await check_key(api_key);
        } catch (e) {
            error = `error: ${e}`;
            return;
        }

        if (!valid) {
            error = "invalid key";
            return;
        }

        localStorage.setItem("api_key", api_key);
        goto("/panel");
    }

    onMount(() => {
        refresh(false);
    });
</script>

<TeckPage>
    <Container slot="static" title={ "teckpanel&trade; 2.0 login" }>
        <input bind:value={api_key} id="api_key" placeholder="api key" type="password" class="w-[90%] text-xl rounded-3xl border-2 border-gray-400 bg-slate-100/75 text-black backdrop-blur-lg drop-shadow-xl ml-2 mr-2 p-3 md:p-4 lg:p-5">

        <div class="flex-row">
            <button on:click={sign_in} class="mt-10 transition-all ease-in-out rounded-full bg-slate-600/75 text-slate-100  pl-8 pr-8 md:pl-10 md:pr-10 lg:pl-12 lg:pr-12 pt-4 pb-4 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">sign in</button>
        </div>

        {#if error != null}
        <p class="text-lg sm:text-xl md:text-2xl text-red-500">{error}</p>
        {/if}
    </Container>
</TeckPage>