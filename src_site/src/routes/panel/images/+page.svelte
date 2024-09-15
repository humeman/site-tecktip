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
    import { list_images_and_run, delete_image, confirm_submission_with_edits, delete_submission, format_timestamp } from "$lib/admin";
    import Fa from 'svelte-fa'
    import { faPencil, faCheck, faTrash } from '@fortawesome/free-solid-svg-icons'

    let key;
    let images = [];
    let pending_deletion = [];

    async function load_images() {
        await list_images_and_run(key, async (image) => {
            images = [...images, image];
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

        await load_images();
    });

    async function remove(image) {
        if (!pending_deletion.includes(image.id)) {
            pending_deletion = [...pending_deletion, image.id];
            return;
        }

        await delete_image(key, image.id);
        pending_deletion = pending_deletion.filter(id => id != image.id);
        await load_images();
    }
</script>

<TeckPage>
    <Container slot="static" title={ "images" }>
        <div class="flex 2xl:flex-row flex-col gap-3 md:gap-4 lg:gap-6 w-full items-center justify-center">
            <button on:click={() => {goto("/panel/images/new")}} class="transition-all ease-in-out rounded-full bg-slate-500/75 text-slate-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">new</button>
            <button on:click={() => {goto("/panel")}} class="transition-all ease-in-out rounded-full bg-cyan-600/75 text-blue-100 pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-cyan-600 drop-shadow-xl dark:drop-shadow-xl border-2 border-cyan-600">back</button>
        </div>

        <div class="mt-10 flex flex-col gap-3 md:gap-4 lg:gap-6 w-full">
            {#each images as image}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <div class="w-full px-3 py-2 md:px-5 md:py-3 lg:px-6 lg:py-4 drop-shadow-xl dark:drop-shadow-xl rounded-3xl border-2 bg-slate-300/50 border-slate-300 ease-in-out transition-all">
                <div class="flex flex-row items-center justify-center">
                    <div class="grow max-w-[80vh] p-10">
                        <img src={image.url} alt="teck image {image.id}" class="w-full rounded-3xl">
                    </div>
                    <div class="p-0 m-2 lg:m-3" on:click={() => {remove(image)}}>
                        <Fa icon={faTrash} size="2vw" class="p-0 m-0 {pending_deletion.includes(image.id) ? "text-red-600" : "text-slate-800"} hover:text-red-700 hover:cursor-pointer ease-in-out transition-all"></Fa>
                    </div>
                </div>
            </div>
            {/each}
        </div>
    </Container>
</TeckPage>