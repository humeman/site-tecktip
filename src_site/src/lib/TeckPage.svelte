<script context="module">
    import "../app.css";
    import { browser } from "$app/environment";
    import { get, writable } from "svelte/store";
    import { tick } from "svelte";

    let fade_in_progress = false;

    export const fade_style = writable("");
    export const fade_out = writable(false);
    export const fade_in = writable(false);
        
    export async function fade_with(blank_function) {
        if (!browser) return;

        if (fade_in_progress) {
            throw new Error("Attempted fade while one was already in progress!");
        }

        fade_in_progress = true;
        fade_out.set(true);
        await new Promise(resolve => window.setTimeout(resolve, 500));
        try {
            await blank_function();
        } catch (e) {
            console.error("Fade function failed with: " + e + ". Will not fade back in.");
            fade_in_progress = false;
            return;
        }
        fade_out.set(false);
        fade_in.set(true);
        await new Promise(resolve => window.setTimeout(resolve, 500));
        fade_in.set(false);
        fade_in_progress = false;
    }
</script>

<div class="{$fade_in ? "fade-in " : ""}{$fade_out ? "fade-out " : ""}bg-stretch fixed inset-0 flex flex-col items-center justify-center" style={$fade_style}>
    <slot name="fade" class="flex h-[100%] w-full"></slot>
</div> 
<div class="relative w-full transition-all duration-1000 ease-in-out flex flex-col align-middle items-center justify-center min-h-[100%] z-10">
    <slot name="static" class="flex h-[100%] w-full"></slot>
</div>