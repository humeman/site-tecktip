<script>
    import { browser } from "$app/environment";

    export let code;
    export let anim = [];
    export let title;
    export let lastitem;
    let processed = [];
    let line = 0;
    let col = 0;
    let in_progress = false;

    $: code, update_processed();

    $: add_last_item(lastitem);
    
    function add_last_item(lastitem_) {
        if (lastitem == null) { return; }
        code = [...code, lastitem]
        processed = [];
        anim = [];
        update_processed();
    }

    function do_animation() {
        if (!in_progress) return;

        // Don't animate HTML tags
        if (processed[line][col] == '<') {
            while (processed[line][col] != '>') col++;
        }

        // Skip over icons too
        if (processed[line][col] == '%') {
            while (processed[line][col] != '%') col++;
        }

        col++;
        if (col >= processed[line].length) {
            anim[line] = processed[line];
            line++;
            col = 0;
        }
        else {
            anim[line] = `${processed[line].substring(0, col + 1)}<span class="text-gray-700 dark:text-gray-200">█</span>`
        }

        if (line >= processed.length) in_progress = false;

        if (browser) {
            window.setTimeout(() => { do_animation() }, 10);
        }
    }

    function start_animation() {
        in_progress = true;
        line = 0;
        col = 0;
        do_animation();
    }

    function update_processed() {
        code.forEach((line, i) => {
            if (line.length > 0) {
                processed[i] = `<span class='text-gray-600 dark:text-gray-800'>></span> ${line}`;
            }
            else {
                processed[i] = "<span class='invisible'>.</span>";
            }
        })

        processed.forEach(() => {
            anim.push("<span class='invisible'>.</span>");
        })
        start_animation();
    }
</script>

<div class="flex flex-col bg-gradient-to-bl from-slate-300 to-slate-400 dark:from-slate-900 dark:to-black rounded-3xl w-[90%] md:w-[80%] lg:w-[70%] drop-shadow-3xl">
    <div class="flex flex-row items-center w-full bg-gradient-to-bl from-slate-900 to-black dark:from-slate-300 dark:to-slate-400 overflow-hidden rounded-t-3xl p-2 pl-4">
        <p class="text-gray-50 dark:text-gray-800 grow font-bold">{@html title}</p>
        <div class="rounded-full bg-green-500 w-4 h-4 ml-2"><span class="invisible text-black hover:visible">.</span></div>
        <div class="rounded-full bg-yellow-400 w-4 h-4 ml-2"><span class="invisible text-black hover:visible">-</span></div>
        <div class="rounded-full bg-red-500 w-4 h-4 ml-2 mr-2"><span class="invisible text-black hover:visible">x</span></div>
    </div>

    <div class="m-6">
        {#each anim as line}
            <p class="text-gray-700 dark:text-gray-200 font-mono font-medium lg:text-xl md:text-lg sm:text-md">{@html line}</p>
        {/each}
    </div>
</div> 