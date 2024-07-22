<script context="module">
    export const autotip = writable(false);
</script>

<script>
    import { browser } from "$app/environment"
    import { goto } from "$app/navigation"
    import { writable } from "svelte/store"
    import { new_img } from "$lib/TeckTip.svelte"

    export var submission = null;

    function toggle_autotip() {
        autotip.set(!$autotip); 

        if ($autotip) { 
            new_img(); 
        }
    }

    function goto_submit() {
        if (browser) {
            goto("submit")
        }
    }
</script>

<div class="grow"></div>

<div id="footer" class="flex mt-auto flex-col md:flex-row justify-center items-center rounded-t-3xl bg-gradient-to-r from-gray-800/75 to-gray-900/75 backdrop-blur-lg w-[95%] p-3 md:p-5 lg:p-10 gap-3 md:gap-5 lg:gap-10">
    <div class="flex flex-col gap-4 grow">
        <h1 class="text-transparent grow bg-clip-text h-full align-middle bg-gradient-to-r from-slate-100 to-blue-300 drop-shadow-xl lg:text-2xl md:text-xl text-md">
            site by <a href="https://humeman.com" class="underline hover:text-blue-400 transition-all ease-in-out font-semibold">humeman</a>
        </h1>
        {#if submission != null}
        <h1 class="text-transparent grow bg-clip-text h-full align-middle bg-gradient-to-r from-slate-100 to-blue-300 drop-shadow-xl lg:text-xl md:text-md text-sm">
            tip submitted by <strong>{submission}</strong>
        </h1>
        {/if}
    </div>
    <div class="flex flex-row gap-3 md:gap-4 lg:gap-6">
        <button on:click={goto_submit} class="transition-all ease-in-out rounded-full bg-slate-600/75 text-slate-100  pl-6 pr-6 md:pl-8 md:pr-8 lg:pl-12 lg:pr-12 pt-2 pb-2 md:pt-3 md:pb-3 lg:pt-3 lg:pb-3 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">submit</button>
        <button on:click={() => {new_img(false)}} class="transition-all ease-in-out rounded-full bg-slate-600/75 text-slate-100  pl-4 pr-4 md:pl-6 md:pr-6 lg:pl-10 lg:pr-10 pt-2 pb-2 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">new</button>
        <button on:click={toggle_autotip} class="{$autotip ? 'bg-green-600/60' : 'bg-slate-600/75'} transition-all ease-in-out rounded-full text-slate-100 pl-4 pr-4 md:pl-6 md:pr-6 lg:pl-10 lg:pr-10 pt-2 pb-2 lg:text-xl md:text-lg text-md font-bold hover:bg-slate-500 drop-shadow-xl dark:drop-shadow-xl border-2 border-slate-500">auto</button>
    </div>
</div>