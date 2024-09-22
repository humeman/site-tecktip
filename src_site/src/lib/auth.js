import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

let uri = `${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}`;

export async function check_key(api_key) {
    let res = await fetch(
        `${uri}/admin/auth`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );
    
    if (!res.ok) return false;
    let data = await res.json();
    return data.success;
}