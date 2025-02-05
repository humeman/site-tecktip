<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { page } from '$app/stores';
    import { goto } from "$app/navigation"
    import { refresh } from "$lib/tecktip";
    import { onMount } from "svelte";
    import { check_key } from "$lib/auth";
    import { create_tip, get_teckgpt, format_timestamp } from "$lib/admin";

    let key;
    let error;
    let limited = false;
    let prompt = null;
    let tip = null;

    onMount(async () => {
        refresh(false);
        key = localStorage.getItem("api_key");

        if (key == null) {
            goto("/panel/login");
            return;
        }
        let valid;
        try {
            valid = await check_key(key);
        } catch (e) {
            console.error(e);
            valid = false;
        }
        if (!valid) {
            goto("/panel/login");
            return;
        }

        await get();
    });
    
    async function get() {
        if (limited) return;
        tip = null;
        error = null;
        limited = true;
        if (prompt != null && prompt.trim().length == 0) prompt = null;
        try {
            tip = await get_teckgpt(key, prompt);
            window.setTimeout(() => limited = false, 5000);
        } catch (e) {
            error = `error: ${e}`;
            window.setTimeout(() => limited = false, 1000);
            tip = null;
            return;
        }
    }

    async function save() {
        if (tip == null) return;
        try {
            let new_tip = await create_tip(
                key,
                {
                    "tip": tip,
                    "by": "teckgpt"
                }
            );
            goto(`/panel/edit?id=${new_tip.id}`)
        } catch (e) {
            error = `error: ${e}`;
            return;
        }
    }
</script>

<TeckPage>
    <Container slot="static" title={ "teckgpt" }>
        <input bind:value={prompt} id="prompt" placeholder="custom prompt (optional)" class="w-full text-center pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl text-xl rounded-full border-2 border-white/50 bg-white/75 text-slate-950 backdrop-blur-lg drop-shadow-xl">

        <p class="text-center text-lg sm:text-xl md:text-2xl text-slate-100">{tip != null ? tip : "thinking..."}</p>

        {#if error != null}
        <p class="text-center text-lg sm:text-xl md:text-2xl text-red-500">{error}</p>
        {/if}

        <div class="flex flex-row flex-wrap gap-3 md:gap-4 lg:gap-6 w-full items-center justify-center">
            <button on:click={save} class="transition-all ease-in-out rounded-full {tip == null ? "bg-green-600/5 text-green-100/15 border-green-600/25" : "bg-green-600/75 text-green-100 hover:bg-green-600 border-green-600"} pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-green-600 drop-shadow-xl dark:drop-shadow-xl border-2">create</button>
            <button on:click={get} class="transition-all ease-in-out rounded-full {limited ? "bg-cyan-600/5 text-cyan-100/15 border-cyan-600/25" : "bg-cyan-600/75 text-cyan-100 hover:bg-cyan-600 border-cyan-600"} pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold drop-shadow-xl dark:drop-shadow-xl border-2">refresh</button>
            <button on:click={() => {goto("/panel");}} class="transition-all ease-in-out rounded-full bg-slate-600/75 text-red-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">back</button>
        </div>
    </Container>
</TeckPage>