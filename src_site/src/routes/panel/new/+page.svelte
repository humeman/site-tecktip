<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { page } from '$app/stores';
    import { goto } from "$app/navigation"
    import { refresh } from "$lib/tecktip";
    import { onMount } from "svelte";
    import { check_key } from "$lib/auth";
    import { create_tip, format_timestamp } from "$lib/admin";

    let key;
    let error;

    let new_tip;
    let new_by;

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
    });

    async function save() {
        try {
            await create_tip(
                key,
                {
                    "tip": new_tip,
                    "by": new_by
                }
            );
        } catch (e) {
            error = `error: ${e}`;
            return;
        }
        goto("/panel");
    }
</script>

<TeckPage>
    <Container slot="static" title={ "create tip" }>
        <div class="flex w-full flex-col lg:flex-row items-center">
            <input bind:value={new_tip} id="tip" placeholder="tip" class="grow pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl text-xl rounded-full border-2 border-white/50 bg-white/75 text-slate-950 backdrop-blur-lg drop-shadow-xl">
            <p class="inline text-lg sm:text-xl md:text-2xl text-slate-100 px-3 md:px-5 lg:px-7 py-2">by</p>
            <input bind:value={new_by} id="by" placeholder="by" class="pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl text-xl rounded-full border-2 border-white/50 bg-white/75 text-slate-950 backdrop-blur-lg drop-shadow-xl">
        </div>

        <div class="flex flex-row flex-wrap gap-3 md:gap-4 lg:gap-6 w-full items-center justify-center">
            <button on:click={save} class="transition-all ease-in-out rounded-full bg-green-600/75 text-blue-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-green-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-green-600">create</button>
            <button on:click={() => {goto("/panel");}} class="transition-all ease-in-out rounded-full bg-red-600/75 text-red-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-red-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-red-500">cancel</button>
        </div>

        {#if error != null}
        <p class="text-lg sm:text-xl md:text-2xl text-red-500">{error}</p>
        {/if}
    </Container>
</TeckPage>