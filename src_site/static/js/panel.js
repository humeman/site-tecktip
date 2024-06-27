function get_tips() {
    $(".tips").empty()

    get(
        "https://tecktip.today:8325/list",
        {
            "key": localStorage.getItem("api-key")
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                console.log("error: " + data["reason"]);
                return;
            }

            // Sort uuids by created date
            sorted = Object.keys(data["tips"]).sort((a, b) => {
                return data["tips"][a]["created"] - data["tips"][b]["created"]
            })

            for (let i in sorted) {
                let uid = sorted[i]
                // Get tip value
                let info = data["tips"][uid]

                // Create a tip div
                var tip = $(
                    `
                    <div class="tecktip" id="${uid}">
                        <p class="tip">${escapeHtml(info['tip'])}</p>
                        <div class="info">
                            <p class="info" id="uuid">${info['uuid'].split('-')[0]}</p>
                            <p class="info" id="user">${escapeHtml(info['by'])}</p>
                            <p class="info" id="time">${info['created']}</p>
                            <button class="smallbutton" id="edit" onclick="window.location.replace('https://tecktip.today/panel/edit.html?uuid=${info['uuid']}')">edit</button>
                            <button class="smallbutton" id="kill" onclick="delete_tip('${info['uuid']}')">kill</button>
                        </div>
                    </div>
                    `
                )

                $(".tips").append(tip);
            }

            let params = getSearchParameters();
            // Check for jump arg
            if (params["current"]) {
                window.location.replace(`#${params['current']}`)
            }
        }
    )
}

function delete_tip(tip) {
    put(
        "https://tecktip.today:8325/kill",
        {
            "key": localStorage.getItem("api-key"),
            "uuid": tip
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                console.log(data["reason"]);
                return;
            }

            $("#status").text(`tip ${tip} deleted.`)

            get_tips();
        }
    )
}

function save_tip() {
    let by = $("#createdby").val();
    let tip = $("#tiptext").val();

    let error = $(".error");
    error.text("");

    if (by.length > 20 || by.length < 3) {
        error.text(`by must be between 3 and 20 chars, not ${by.length}`);
        return;
    }
    if (tip.length > 128 || tip.length < 3) {
        error.text(`tip must be between 3 and 128 chars, not ${tip.length}`);
        return;
    }

    // post
    put(
        "https://tecktip.today:8325/new",
        {
            "key": localStorage.getItem("api-key"),
            "tip": tip,
            "by": by
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                error.text(`error: ${data['reason']}`);
            } else {
                window.location.replace(`https://tecktip.today/panel?current=${data['uuid']}`)
            }
        }
    )
}

function populate_edit() {
    let params = getSearchParameters();

    let uuid = params["uuid"];

    if (!uuid) {
        $(".error").text("error: no uuid specified");
        return;
    }

    $("#uuid").val(uuid);

    // get tip info
    get(
        "https://tecktip.today:8325/get",
        {
            "key": localStorage.getItem("api-key"),
            "uuid": uuid
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                $(".error").text(`error: ${data['reason']}`);
                return;
            }

            $("#createdby").val(data["tip"]["by"]);
            $("#tiptext").val(data["tip"]["tip"]);
        }
    )
}

function save_edit() {
    let uuid = $("#uuid").val();
    let by = $("#createdby").val();
    let tip = $("#tiptext").val();

    let error = $(".error");
    error.text("");

    if (by.length > 20 || by.length < 3) {
        error.text(`by must be between 3 and 20 chars, not ${by.length}`);
        return;
    }
    if (tip.length > 128 || tip.length < 8) {
        error.text(`tip must be between 8 and 128 chars, not ${tip.length}`);
        return;
    }

    // post
    put(
        "https://tecktip.today:8325/edit",
        {
            "key": localStorage.getItem("api-key"),
            "uuid": uuid,
            "tip": tip,
            "by": by
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                error.text(`error: ${data['reason']}`);
            } else {
                window.location.replace(`https://tecktip.today/panel?current=${data['uuid']}`)
            }
        }
    )
}

