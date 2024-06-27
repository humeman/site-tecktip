function check_login(origin) {
    // if they're logged in, redirect to panel
    let key = localStorage.getItem("api-key");

    if (key !== null) {
        // redirect
        if (origin != "index") {
            window.location.replace("/panel/index.html");
        }
    }

    else {
        if (origin != "login") {
            window.location.replace("/panel/login.html");
        }
    }
}

function init_login() {
    $("#loginerror").text("");
    // get key
    let key = $("#keyinput").val();

    console.log(key);

    put(
        "https://tecktip.today:8325/test_login",
        {
            "key": key
        },
        (data, status, xhr) => {
            if (data["success"] == true) {
                // store & redirect
                localStorage.setItem("api-key", key);

                window.location.replace("/panel/index.html");
            } else {
                // set error
                $("#loginerror").text(`error: ${data["reason"]}`)
            }
        }
    )
}

function logout() {
    localStorage.removeItem("api-key");
    window.location.replace("https://tecktip.today/panel/login.html");
}