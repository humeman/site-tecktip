function get_submissions() {
    $(".tips").empty()

    get(
        "https://tecktip.today:8325/pending",
        {
            "key": localStorage.getItem("api-key")
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                console.log("error: " + data["reason"]);
                return;
            }

            // Sort uuids by created date
            sorted = Object.keys(data["pending"]).sort((a, b) => {
                return data["pending"][a]["created"] - data["pending"][b]["created"]
            })

            for (let i in sorted) {
                let uid = sorted[i]
                // Get tip value
                let info = data["pending"][uid]

                // Create a tip div
                var tip = $(
                    `
                    <div class="tecktip" id="${uid}">
                        <p class="tip">${escapeHtml(info['tip'])}</p>
                        <div class="info">
                            <p class="info" id="uuid">${info['uuid'].split('-')[0]}</p>
                            <p class="info" id="user">${escapeHtml(info['by'])}</p>
                            <p class="info" id="time">${info['at']}</p>
                            <p class="info" id="ip">${info['ip']}</p>
                            <button class="smallbutton" id="accept" onclick="accept_submission('${info['uuid']}')">add</button>
                            <button class="smallbutton" id="edit" onclick="edit_submission('${info['uuid']}')">edit</button>
                            <button class="smallbutton" id="kill" onclick="kill_submission('${info['uuid']}')">kill</button>
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

function accept_submission(uuid, callback) {
    // Get pending submission
    let container = $(`#${uuid}`);

    let tip = container.children(".tip").eq(0).text();
    let user = container.children(".info").eq(0).children("#user").eq(0).text();

    put(
        "https://tecktip.today:8325/new",
        {
            "key": localStorage.getItem("api-key"),
            "tip": tip,
            "by": user
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                $("#status").text(`error: ${data['reason']}`);
                return;
            }

            $("status").text(`created tip ${data["uuid"]}`);

            // Delete suggestion
            put(
                "https://tecktip.today:8325/del_pending",
                {
                    "key": localStorage.getItem("api-key"),
                    "uuid": uuid
                },
                (data_, status, xhr) => {
                    if (!data_["success"]) {
                        $("#status").text(`error: ${data_['reason']}`);
                        return;
                    }

                    // Reload page
                    get_submissions()

                    if (callback) {
                        callback(data["uuid"]);
                    }
                }
            )
        }
    )
}

function edit_submission(uuid) {
    // Accept the submission
    accept_submission(
        uuid,
        (new_uuid) => {
            // Go to edit page
            window.location.replace(`https://tecktip.today/panel/edit.html?uuid=${new_uuid}`)
        }
    )
}

function kill_submission(uuid) {
    put(
        "https://tecktip.today:8325/del_pending",
        {
            "key": localStorage.getItem("api-key"),
            "uuid": uuid
        },
        (data_, status, xhr) => {
            if (!data_["success"]) {
                $("#status").text(`error: ${data_['reason']}`);
                return;
            }

            $("#status").text(`submission ${uuid} killed.`)

            // Reload page
            get_submissions()
        }
    )
}