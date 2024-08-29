<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { goto } from "$app/navigation"
    import { browser } from "$app/environment"
    import { get_tip, refresh } from "$lib/tecktip.js";
    import { onMount } from "svelte";

    let tip;
    let by;
    let error = ""

    async function submit_tip() {
        if (tip == null || by == null) {
            error = "fill out both fields before continuing";
            return;
        }

        if (by.length > 20 || by.length < 3) {
            error = `author name must be between 3 and 20 chars, not ${by.length}`;
            return;
        }

        if (tip.length > 128 || tip.length < 3) {
            error = `tip must be between 3 and 128 chars, not ${tip.length}`;
            return;
        }

        try {
            let res = await fetch(
                `https://${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}/submit`,
                {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(
                        {
                            tip: tip,
                            name: by
                        }
                    )
                });
            let data = await res.json();
            if (!data["success"]) {
                error = `error: ${data['reason']}`;
            } else {
                window.location.replace(`/success?event=create&uuid=${data['uuid']}`)
            }
        } catch (e) {
            error = "failed to send submission to API. try again later"
        }
    }

    function goto_home() {
        if (browser) {
            goto("/")
        }
    }

    onMount(async () => {
        await refresh(false);
    })
</script>

<TeckPage>
    <Container slot="static" title={ "submit a tip" }>
        <p class="text-lg sm:text-xl md:text-2xl text-slate-100 p-2 mb-5 md:mb-7 lg:mb-10 text-center">
            enter your tip below for our curators to review.
        </p>
        
        <input bind:value={tip} id="tip" placeholder="tip" class="w-[90%] text-xl rounded-3xl border-2 border-gray-400 bg-slate-100/75 text-black backdrop-blur-lg drop-shadow-xl ml-2 mr-2 p-3 md:p-4 lg:p-5">
        <input bind:value={by} id="createdby" placeholder="created by" class="w-[90%] text-xl rounded-3xl border-2 border-gray-400 bg-slate-100/75 text-black backdrop-blur-lg drop-shadow-xl ml-2 mr-2 p-3 md:p-4 lg:p-5">

        <div class="flex-row">
            <button on:click={submit_tip} class="mr-2 md:mr-4 lg:mr-5 mt-10 transition-all ease-in-out rounded-full bg-slate-600/75 text-slate-100  pl-8 pr-8 md:pl-10 md:pr-10 lg:pl-12 lg:pr-12 pt-4 pb-4 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">submit</button>
            <button on:click={goto_home} class="mr-2 md:mr-4 lg:ml-5 transition-all ease-in-out rounded-full bg-red-800/75 text-slate-100  pl-8 pr-8 md:pl-10 md:pr-10 lg:pl-12 lg:pr-12 pt-4 pb-4 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">cancel</button>
        </div>
        
        <p class="text-red-800 text-lg">{@html error}</p>
    </Container>
</TeckPage>