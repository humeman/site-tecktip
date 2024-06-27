<script>
    import "../app.css";

    import { browser } from "$app/environment";
    import { get } from "svelte/store";

    import TeckTip from "$lib/TeckTip.svelte";
    import { bg_style } from "$lib/TeckTip.svelte";
</script>

<main style={$bg_style}>
    <div class="min-h-[90%] flex flex-col items-center justify-center">
        <slot name="fade" class="flex h-[100%] w-full"></slot>
    </div>
</main> 
<main class="pt-10 w-full transition-all duration-1000 ease-in-out">
    <div class="flex flex-col items-center justify-center min-h-[100%] ">
        <slot name="static" class="flex h-[100%] w-full"></slot>
    </div>
</main>