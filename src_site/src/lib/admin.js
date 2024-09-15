import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

let uri = `https://${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}`;

export async function list_tips_and_run(api_key, callback) {
    await callback({
        "tip": "test tip 1",
        "created": 1724885557,
        "by": "teck man 1",
        "id": "real-uuid-1"
    });
    await callback({
        "tip": "test tip 2",
        "created": 1624885557,
        "by": "teck man 2",
        "id": "real-uuid-2"
    });
    await callback({
        "tip": "test tip 3",
        "created": 1524885557,
        "by": "teck man 3",
        "id": "real-uuid-3"
    });

    return;

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

export async function get_tip(api_key, id) {
    return {
        "tip": "test tip 3",
        "created": 1524885557,
        "by": "teck man 3",
        "id": "real-uuid-3"
    }

    res = await fetch(
        `${uri}/tips?id=${id}`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function update_tip(api_key, tip) {
    return;

    res = await fetch(
        `${uri}/tips`,
        {
            method: "PUT",
            body: JSON.stringify(tip),
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function create_tip(api_key, tip) {
    return;

    res = await fetch(
        `${uri}/tips`,
        {
            method: "POST",
            body: JSON.stringify(tip),
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function list_submissions_and_run(api_key, callback) {
    await callback({
        "tip": "test submission 1",
        "created": 1724885557,
        "by": "teck man 1",
        "id": "real-uuid-1",
        "ip": "1.2.3.4"
    });
    await callback({
        "tip": "test submission 2",
        "created": 1624885557,
        "by": "teck man 2",
        "id": "real-uuid-2",
        "ip": "2.3.4.5"
    });

    return;

    res = await fetch(
        `${uri}/tips`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );

    return res.ok;
}

export async function get_submission(api_key, id) {
    return {
        "tip": "test submission 1",
        "created": 1524885557,
        "by": "teck man 1",
        "id": "real-uuid-1",
        "ip": "1.2.3.4"
    }

    res = await fetch(
        `${uri}/submissions?id=${id}`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function confirm_submission(api_key, id) {
    return;

    res = await fetch(
        `${uri}/submissions/confirm`,
        {
            method: "POST",
            body: JSON.stringify(
                {
                    "id": id
                }
            ),
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function confirm_submission_with_edits(api_key, id, tip, by) {
    return;

    res = await fetch(
        `${uri}/submissions/confirm`,
        {
            method: "POST",
            body: JSON.stringify(
                {
                    "id": id,
                    "edits": {
                        "tip": tip,
                        "by": by
                    }
                }
            ),
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function delete_submission(api_key, id) {
    return;

    res = await fetch(
        `${uri}/submissions?id=${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]

export function format_timestamp(timestamp) {
    const date = new Date(timestamp * 1000);

    return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`
}