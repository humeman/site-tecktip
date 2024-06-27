function submit_tip() {
    let tip = $("#tiptext").val();
    let by = $("#createdby").val();

    let error = $(".error");
    error.text("");

    if (by.length > 20 || by.length < 3) {
        error.text(`author name must be between 3 and 20 chars, not ${by.length}`);
        return;
    }

    if (tip.length > 128 || tip.length < 3) {
        error.text(`tip must be between 3 and 128 chars, not ${tip.length}`);
        return;
    }

    // post
    put(
        "https://tecktip.today:8325/pub/submit",
        {
            "tip": tip,
            "by": by
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                error.text(`error: ${data['reason']}`);
            } else {
                window.location.replace(`https://tecktip.today/success.html?event=create&uuid=${data['uuid']}`)
            }
        }
    )
}

function populate_message() {
    const params = getSearchParameters();

    let placeholder = messages[params["event"]];

    for (let param in params) {
        let val = params[param];

        placeholder = placeholder.replace(`%${param}%`, val);
    }

    $(".status").html(placeholder);
}

messages = {
    "create": "submission id '%uuid%' sent successfully. our curators will review it shortly. thank you for your contribution &#128077;"
}
