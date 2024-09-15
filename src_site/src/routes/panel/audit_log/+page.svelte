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
    import { list_audit_log_and_run, format_timestamp } from "$lib/admin";
    import Fa from 'svelte-fa'
    import { faPencil, faCheck, faTrash } from '@fortawesome/free-solid-svg-icons'

    let key;
    let logs = [];
    let filter;

    async function load_log() {
        await list_audit_log_and_run(key, async (log) => {
            logs = [...logs, log];
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

        await load_log();
    });

    function filter_logs() {
        if (!filter) return logs;

        let filter_adj = filter.toLowerCase().trim();
        if (filter_adj.length == 0) return logs;

        let filtered = [];
        for (let log of logs) {
            if (
                log.user_alias.toLowerCase().includes(filter_adj) 
                || log.user_id.toLowerCase().includes(filter_adj) 
                || format_timestamp(log.created).toLowerCase().includes(filter_adj)
                || log.id.toLowerCase().includes(filter_adj)
                || log.action.toLowerCase().includes(filter_adj)
            )
                filtered.push(log);
        }

        return filtered;
    }

    let filtered_logs = [];
    $: filter, logs, filtered_logs = filter_logs();
</script>

<TeckPage>
    <Container slot="static" title={ "audit log" }>
        <div class="flex 2xl:flex-row flex-col gap-3 md:gap-4 lg:gap-6 w-full items-center justify-center">
            <button on:click={() => {goto("/panel")}} class="transition-all ease-in-out rounded-full bg-cyan-600/75 text-blue-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-cyan-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-cyan-600">back</button>
        </div>

        <div class="mt-10 flex flex-col gap-3 md:gap-4 lg:gap-6 w-full">
            <input bind:value={filter} id="filter" placeholder="filter" class="min-w-[30%] pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl text-xl rounded-full border-2 border-white/50 bg-white/75 text-slate-950 backdrop-blur-lg drop-shadow-xl">
            {#each filtered_logs as log}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="w-full px-3 py-2 md:px-5 md:py-3 lg:px-6 lg:py-4 drop-shadow-xl dark:drop-shadow-xl rounded-3xl border-2 bg-slate-300/50 border-slate-300 ease-in-out transition-all">
                <div class="flex flex-row items-center">
                    <div class="grow m-0 p-0">
                        <p class="text-slate-800 lg:text-3xl md:text-2xl text-lg py-1 md:py-2 drop-shadow-xl font-bold whitespace-pre-line">{log.action}</p>
                        <p class="text-slate-950 lg:text-xl md:text-lg text-md drop-shadow-xl"><span class="font-bold text-cyan-800">{log.user_alias}</span> on <span class="font-bold text-cyan-800">{format_timestamp(log.created)}</span></p>
                        <p class="text-slate-600 lg:text-md md:text-sm text-xs drop-shadow-xl">log {log.id}, user {log.user_id}</p>
                    </div>
                </div>
            </div>
            {/each}
        </div>
    </Container>
</TeckPage>