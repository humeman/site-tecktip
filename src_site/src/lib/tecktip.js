
import { browser } from "$app/environment"
import { readable, writable } from 'svelte/store';
import { autotip } from "$lib/Footer.svelte";
import { fade_with, fade_style } from "$lib/TeckPage.svelte";
import { get } from 'svelte/store';
import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

export const current_tip = writable({tip: "", by: null});

let uri = `https://${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}`;

export async function refresh(with_tip) {
    await fade_with(
        async () => {
            if (with_tip) {
                let tip = await get_tip();
                current_tip.set(tip);
            }

            let img = await get_img();
            fade_style.set(`background-image: url("/images/${img}");`);
        }
    )
}

export async function refresh_no_fade(with_tip) {
    if (with_tip) {
        let tip = await get_tip();
        current_tip.set(tip);
    }

    let img = await get_img();
    fade_style.set(`background-image: url("/images/${img}");`);
}

export async function get_tip(err_counter = 0) {
    let res;
    try {
        res = await fetch(uri, 
            {
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );
    } catch (e) {
        console.error(e)
        err_counter++;

        if (err_counter > 3) {
            return "error: the teck man is broken :(";
        }
        await new Promise(r => setTimeout(r, 500));
        return await get_tip(err_counter = err_counter);
    }
    if (res.status != 200) {
        return "error: the teck man is broken :(";
    }
    return await res.json();
}

export async function get_img(err_counter = 0) {
    let res;
    try {
        res = await fetch(`${uri}/img`);
    } catch (e) {
        console.error(e)
        err_counter++;

        if (err_counter > 3) {
            return null;
        }
        await new Promise(r => setTimeout(r, 500));
        return await get_tip(err_counter);
    }
    if (res.status != 200) {
        return null;
    }
    return await res.text();
}