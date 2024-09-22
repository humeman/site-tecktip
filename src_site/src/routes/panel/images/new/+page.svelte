<script>
    import Container from "$lib/Container.svelte";
    import TeckPage from "$lib/TeckPage.svelte";
    import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

    import { page } from '$app/stores';
    import { goto } from "$app/navigation"
    import { browser } from "$app/environment"
    import { refresh } from "$lib/tecktip";
    import { onMount, tick } from "svelte";
    import { redirect } from "@sveltejs/kit";
    import { check_key } from "$lib/auth";
    import { upload_image, format_timestamp } from "$lib/admin";

    let key;
    let error;
    let files;

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

    async function upload(file) {
        try {
            await upload_image(key, files[0]);
        } catch (e) {
            console.error(e);
            error = e;
            return;
        }
        goto("/panel/images");
    }

    $: if (files) {
        upload(files[0]);
    }
</script>

<TeckPage>
    <Container slot="static" title={ "new image" }>
        <label for="image" class="cursor-pointer transition-all ease-in-out rounded-full bg-cyan-600/75 text-cyan-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-cyan-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-cyan-500">pick an image</label>
        <input accept="image/png, image/jpeg" bind:files id="image" name="image" type="file" class="hidden" />
        <button on:click={() => {goto("/panel/images");}} class="transition-all ease-in-out rounded-full bg-red-600/75 text-red-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-red-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-red-500">cancel</button>

        {#if error != null}
        <p class="text-lg sm:text-xl md:text-2xl text-red-500">{error}</p>
        {/if}
    </Container>
</TeckPage>