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

export async function delete_tip(api_key, id) {
    return;

    res = await fetch(
        `${uri}/tips?id=${id}`,
        {
            method: "DELETE",
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

export async function list_images_and_run(api_key, callback) {
    await callback({
        "id": "0c796b9e-a994-4247-bb2c-2c1003bfd8bc",
        "url": "https://tecktip.today/images/0c796b9e-a994-4247-bb2c-2c1003bfd8bc.jpg"
    });
    await callback({
        "id": "f4f4c4d0-7589-418b-b239-75e1a3c4e132",
        "url": "https://tecktip.today/images/f4f4c4d0-7589-418b-b239-75e1a3c4e132.jpg"
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

export async function delete_image(api_key, id) {
    return;

    res = await fetch(
        `${uri}/images?id=${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function upload_image(api_key, file) {
    return {
        "id": "f4f4c4d0-7589-418b-b239-75e1a3c4e132",
        "url": "https://tecktip.today/images/f4f4c4d0-7589-418b-b239-75e1a3c4e132.jpg"
    };

    let data = new FormData();
    data.append("file", file);

    res = await fetch(
        `${uri}/images`,
        {
            method: "POST",
            body: data,
            headers: {
                "Authorization": api_key
            }
        }
    );

    return await res.json();
}

export async function list_audit_log_and_run(api_key, callback) {
    await callback({
        "id": "abc",
        "user_id": "def",
        "user_alias": "the teck man",
        "created": 1724885557,
        "action": "tip deleted\nby: abc\ncontent: this is a teck tip\non: Jul 18, 2024"
    });
    await callback({
        "id": "abc1",
        "user_id": "def1",
        "user_alias": "the teck man",
        "created": 1524885557,
        "action": "tip deleted\nby: abcd\ncontent: this is another teck tip\non: Jul 18, 2014"
    });

    return;

    res = await fetch(
        `${uri}/audit`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );

    return res.ok;
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