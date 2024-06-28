<script context="module">
    import { browser } from "$app/environment"
    import { writable } from 'svelte/store';
    import { autotip } from "$lib/Footer.svelte";
	import { get } from 'svelte/store';
    import { SITE_HOST, API_PORT } from '$env/static/public'

    export const bg_style = writable("");
    export const do_update = writable(false);

    let autotip_state = false;

    export let opacity = 100;

    export let current_image = null;
    let uri = `https://${SITE_HOST}:${API_PORT}`;

    export async function get_tip(err_counter = 0) {
        return fetch(uri)
            .then( response => response.text())
            .then( text => {
                return text
            })
            .catch( err => {
                err_counter++;

                if (err_counter > 10) {
                    return null;
                }
                return get_tip(err_counter);
            })
    }

    export function get_img(err_counter = 0) {
        return fetch(`${uri}/img`)
            .then( response => response.text())
            .then( text => {
                return text
            })
            .catch( err => {
                err_counter++;

                if (err_counter > 10) {
                    return null;
                }
                return get_img(err_counter);
            })
    }

    export function set_img() {
        do_update.set(true);

        get_img().then(img => {
            current_image = `/images/${img}`;
            update_bg_style();

            if (browser) {
                // Animate upwards
                window.setTimeout(animate_fade(5, 500), 500/5);


                if (get(autotip)) {  
                    window.setTimeout(() => {new_img(true)}, 5000);
                }
            }
        })
    }

    export function new_img(is_autotip = false) {
        if (is_autotip) {
            if (!get(autotip)) return;
        }

        if (browser) {
            window.setTimeout(animate_fade(-1, 500), 5);
            window.setTimeout(set_img, 500);
        }
    }

    function animate_fade(step, time) {
        // Calculate a new opacity
        opacity += step;

        // And using that, compile a new bg_style
        update_bg_style();

        if (browser) {
            let new_step = step;
            if (new_step < 0) {new_step *- 1}

            if (opacity > 0 && opacity < 100) {
                window.setTimeout(() => {animate_fade(step, time)}, time * (new_step / 100));
            }
        }
    }

    function update_bg_style() {
        if (current_image == null) {
            bg_style.set(`background-image: none; opacity: ${opacity}%`)
        }

        else {
            bg_style.set(`background-image: url("${current_image}"); opacity: ${opacity}%`)
        }
    }

    new_img();
</script>