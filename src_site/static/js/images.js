function populate_images() {
    $(".images").empty()

    get(
        "https://tecktip.today:8325/img/list",
        {
            "key": localStorage.getItem("api-key")
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                console.log("error: " + data["reason"]);
                return;
            }

            // Sort uuids by created date
            sorted = Object.keys(data["images"]).sort((a, b) => {
                return data["images"][a]["created"] - data["images"][b]["created"]
            })

            for (let i in sorted) {
                let uid = sorted[i]
                // Get tip value
                let info = data["images"][uid]

                // Create a tip div
                var tip = $(
                    `
                    <div class="img" id="${uid}">
                        <img class="bigimg" id="img" src="/images/${info['file']}"></img>
                        <div class="info">
                            <p class="info" id="file"><a class="link" href="/images/${info['file']}">${info['file']}</a></p>
                            <p class="info" id="time">${info['created']}</p>
                            <button class="smallbutton" id="kill" onclick="kill_img('${uid}')">kill</button>
                        </div>
                    </div>
                    `
                )

                $(".images").append(tip);
            }

            let params = getSearchParameters();
            // Check for jump arg
            if (params["current"]) {
                window.location.replace(`#${params['current']}`)
            }
        }
    )
}

function start_upload() {
    let url = $("#newurl").val();
    $(".error").text("");

    put(
        "https://tecktip.today:8325/img/add",
        {
            "key": localStorage.getItem("api-key"),
            "url": url
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                $(".error").text(`error: ${data["reason"]}`);
                return;
            }

            // start waiting
            let uuid = data["uuid"];
            window.location.replace(`/panel/publish_img.html?uuid=${uuid}`);
        }
    )
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function update_img_status() {
    const params = getSearchParameters();

    let uuid = params["uuid"];

    // check in for 15 seconds
    for (let i = 0; i < 15; i++) {
        // check status
        get(
            "https://tecktip.today:8325/img/check",
            {
                "key": localStorage.getItem("api-key"),
                "uuid": uuid
            },
            (data, status, xhr) => {
                if (data["success"]) {
                    $(".status").text("image uploaded successfully!");
                    $(".error").text("");
                    $("#secondarybutton").text("go back");
                    return;
                } else {
                    if (data["waiting"]) {
                        $(".status").text(`still waiting: ${i}s`);
                    }
                    else {
                        $(".status").text("server returned download error");
                        $(".error").text(data["reason"]).html();
                        $("#secondarybutton").text("go back");
                        return;
                    }
                }
            }
        )

        await sleep(1000);
    }

    $(".status").text("server timeout");
    $(".error").text("server didn't acknowledge download after 15s. aborting.");
    $("#secondarybutton").text("go back");
}

function kill_img(uuid) {
    put(
        "https://tecktip.today:8325/img/kill",
        {
            "key": localStorage.getItem("api-key"),
            "uuid": uuid
        },
        (data, status, xhr) => {
            if (!data["success"]) {
                $(".error").text(`error deleting: ${data['reason']}`);
                return;
            }

            $("#status").text(`image ${uuid} deleted.`)

            populate_images();
        }
    )
}