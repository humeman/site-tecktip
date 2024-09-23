import { PUBLIC_SITE_HOST, PUBLIC_API_PORT } from '$env/static/public'

let uri = `${PUBLIC_SITE_HOST}:${PUBLIC_API_PORT}`;

async function get_data(res) {
    let data;
    try {
        data = await res.json()
    } catch (e) {
        console.error("Errored request:")
        console.error(e);
        console.error(res);
        if (res.status != 200) {
            throw Error(`api error (unexpected content): ${res.status}`)
        }
        else {
            throw Error(`api error (unexpected content)`)
        }
        throw e;
    }
    if (!data.success) {
        throw Error(`api error: ${res.status} / ${data.reason}`)
    }

    return data.data;
}

export async function list_tips_and_run(api_key, callback) {
    let count = 1
    let page = 0;

    while (count != 0) {
        let res = await fetch(
            `${uri}/admin/tips?page=${page}`,
            {
                headers: {
                    "Authorization": api_key
                }
            }
        );
        let data = await get_data(res);
        for (let tip of data.tips) {
            await callback(tip)
        }

        count = data.tips.length;
        page++;
    }
}

export async function get_tip(api_key, id) {
    let res = await fetch(
        `${uri}/admin/tips/${id}`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
}

export async function delete_tip(api_key, id) {
    let res = await fetch(
        `${uri}/admin/tips/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
}

export async function update_tip(api_key, id, changes) {
    let res = await fetch(
        `${uri}/admin/tips/${id}`,
        {
            method: "PUT",
            body: JSON.stringify(changes),
            headers: {
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
}

export async function create_tip(api_key, tip) {
    let res = await fetch(
        `${uri}/admin/tips`,
        {
            method: "POST",
            body: JSON.stringify(tip),
            headers: {
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
}

export async function list_submissions_and_run(api_key, callback) {
    let count = 1
    let page = 0;

    while (count != 0) {
        let res = await fetch(
            `${uri}/admin/submissions?page=${page}`,
            {
                headers: {
                    "Authorization": api_key
                }
            }
        );
        let data = await get_data(res);
        for (let submission of data.submissions) {
            await callback(submission)
        }

        count = data.submissions.length;
        page++;
    }
}

export async function get_submission(api_key, id) {
    let res = await fetch(
        `${uri}/admin/submissions/${id}`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.submission;
}

export async function confirm_submission(api_key, id, changes) {
    let res = await fetch(
        `${uri}/admin/submissions/${id}`,
        {
            method: "PUT",
            body: JSON.stringify(changes),
            headers: {
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
}

export async function delete_submission(api_key, id) {
    let res = await fetch(
        `${uri}/admin/submissions/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.submission;
}

export async function list_images_and_run(api_key, callback) {
    let count = 1
    let page = 0;

    while (count != 0) {
        let res = await fetch(
            `${uri}/admin/images?page=${page}`,
            {
                headers: {
                    "Authorization": api_key
                }
            }
        );
        let data = await get_data(res);
        for (let image of data.images) {
            await callback(image)
        }

        count = data.images.length;
        page++;
    }
}

export async function delete_image(api_key, id) {
    let res = await fetch(
        `${uri}/admin/images/${id}`,
        {
            method: "DELETE",
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.image;
}

export async function upload_image(api_key, file) {
    let fdata = new FormData();
    fdata.append("file", file);

    let res = await fetch(
        `${uri}/admin/images`,
        {
            method: "POST",
            body: fdata,
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.image;
}

export async function list_audit_log_and_run(api_key, callback) {
    let count = 1
    let page = 0;

    while (count != 0) {
        let res = await fetch(
            `${uri}/admin/audit?page=${page}`,
            {
                headers: {
                    "Authorization": api_key
                }
            }
        );
        let data = await get_data(res);
        for (let audit of data.audits) {
            await callback(audit)
        }

        count = data.audits.length;
        page++;
    }
}

export async function get_teckgpt(api_key) {
    let res = await fetch(
        `${uri}/admin/teckgpt`,
        {
            headers: {
                "Authorization": api_key
            }
        }
    );
    let data = await get_data(res);

    return await data.tip;
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