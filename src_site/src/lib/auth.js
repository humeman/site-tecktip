import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

let uri = `https://${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}`;

export async function check_key(api_key) {
    return true;

    res = await fetch(
        `${uri}/auth`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );

    return res.ok;
}