<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { goto } from "$app/navigation"
    import { browser } from "$app/environment"
    import { refresh } from "$lib/tecktip";
    import { onMount, tick } from "svelte";
    import { redirect } from "@sveltejs/kit";
    import { check_key } from "$lib/auth";
    import { list_tips_and_run, format_timestamp } from "$lib/admin";

    let key;
    let tips = [];
    let filter;

    async function load_tips() {
        await list_tips_and_run(key, async (tip) => {
            console.log(tip);
            tips = [...tips, tip];
        })
    }

    onMount(async () => {
        refresh(false);
        key = localStorage.getItem("api_key");

        if (key == null) {
            goto("panel/login");
            return;
        }

        else {
            let valid;
            try {
                valid = await check_key(key);
            } catch (e) {
                console.error(e);
                valid = false;
            }
            if (!valid) {
                goto("panel/login");
                return;
            }
        }

        await load_tips();
    });

    function filter_tips() {
        if (!filter) return tips;

        let filter_adj = filter.toLowerCase().trim();
        if (filter_adj.length == 0) return tips;

        let filtered = [];
        for (let tip of tips) {
            if (
                tip.tip.toLowerCase().includes(filter_adj) 
                || tip.by.toLowerCase().includes(filter_adj) 
                || format_timestamp(tip.created).toLowerCase().includes(filter_adj)
                || tip.id.toLowerCase().includes(filter_adj)
            )
                filtered.push(tip);
        }

        return filtered;
    }

    let filtered_tips = [];
    $: filter, tips, filtered_tips = filter_tips();
</script>

<TeckPage>
    <Container slot="static" title={ "teckpanel&trade; 2.0" }>
        <div class="flex 2xl:flex-row flex-col gap-3 md:gap-4 lg:gap-6 w-full items-center justify-center">
            <button on:click={() => {goto("/panel/new")}} class="transition-all ease-in-out rounded-full bg-slate-500/75 text-slate-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">new</button>
            <button on:click={() => {goto("/panel/submissions")}} class="transition-all ease-in-out rounded-full bg-slate-500/75 text-slate-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">submissions</button>
            <button on:click={() => {goto("/panel/images")}} class="transition-all ease-in-out rounded-full bg-slate-500/75 text-slate-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">images</button>
            <button on:click={() => {goto("/")}} class="transition-all ease-in-out rounded-full bg-cyan-600/75 text-blue-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-cyan-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-cyan-600">return to tipworld</button>
            <button on:click={() => {localStorage.removeItem("api_key"); goto("/panel/login");}} class="transition-all ease-in-out rounded-full bg-red-600/75 text-red-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-red-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-red-500">log out</button>
        </div>

        <div class="mt-10 flex flex-col gap-3 md:gap-4 lg:gap-6 w-full">
            <input bind:value={filter} id="filter" placeholder="filter" class="min-w-[30%] pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl text-xl rounded-full border-2 border-white/50 bg-white/75 text-slate-950 backdrop-blur-lg drop-shadow-xl">
            {#each filtered_tips as tip}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div on:click={goto(`/panel/edit?id=${tip.id}`)} class="w-full px-3 py-2 md:px-5 md:py-3 lg:px-6 lg:py-4 drop-shadow-xl dark:drop-shadow-xl rounded-3xl border-2 bg-slate-300/50 border-slate-300 hover:bg-slate-400/50 hover:border-slate-400 hover:cursor-pointer ease-in-out transition-all">
                <p class="text-slate-800 lg:text-3xl md:text-2xl text-lg py-1 md:py-2 drop-shadow-xl font-bold">{tip.tip}</p>
                <p class="text-slate-950 lg:text-xl md:text-lg text-md drop-shadow-xl">by <span class="font-bold text-cyan-800">{tip.by}</span> on <span class="font-bold text-cyan-800">{format_timestamp(tip.created)}</span></p>
                <p class="text-slate-600 lg:text-md md:text-sm text-xs drop-shadow-xl">{tip.id}</p>
            </div>
            {/each}
        </div>
    </Container>
</TeckPage>