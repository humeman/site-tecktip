<script>
    export let title;
</script>

<div id="container" class="flex flex-col w-[90%] md:w-[80%] sm:w-[75%] justify-center items-center content-center rounded-3xl my-3 md:my-5 lg:my-10 p-3 md:p-5 lg:p-10 shadow-2xl bg-gradient-to-r from-gray-800/75 to-gray-900/75 backdrop-blur-lg gap-5">
    <h1 class="text-transparent bg-clip-text bg-gradient-to-r from-slate-100 to-blue-300 drop-shadow-3xl dark:drop-shadow-dark3xl lg:text-6xl md:text-5xl text-5xl font-black m-5 text-center">
        {@html title}
    </h1>
    
    <slot></slot>
</div>