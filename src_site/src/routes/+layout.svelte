<svelte:head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Chivo+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&family=Secular+One&display=swap');
    </style>

    <script>
        import { browser } from "$app/environment";


        if (browser) {
            // Set initial dark mode setting
            if (localStorage.getItem("dark_mode") === "true") {
                document.documentElement.classList.add('dark');
            }
        }
    </script>
</svelte:head>

<slot />