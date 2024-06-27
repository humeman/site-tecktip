var in_progress = false;
var in_progress_i = false;
var current_anim = 0;
var new_tip = null;
var auto_tip = false;
var atrunning = false;

// Change old tip
$("#oldtip").text($("newtip").text());

function toggle_auto() {
    auto_tip = !auto_tip;

    $("#auto-toggle").text(auto_tip ? "auto-tip: on" : "auto-tip: off");

    if (!atrunning) {
        $(".buttons").css("display", "none");

        atrunning = true;
        window.setTimeout(
            () => {
                check_auto()
            }, 10000
        )
    }
}

function check_auto() {
    if (auto_tip) {
        get_tip();
        get_image();


        window.setTimeout(
            () => {
                check_auto();
            }, 10000
        )
    } else {
        $(".buttons").css("display", "inline-block");
        atrunning = false;
    }
}

function set_image(img) {
    $(() => {
        if (in_progress_i) {
            return;
        }

        in_progress_i = true;

        // Fade out old bg
        $("html").css("opacity", "0%");
        $("html").css("animation-play-state", "paused");
        $("html").css("animation", "appear 1s infinite");
        $("html").css("animation-direction", "reverse");
        $("html").css("animation-play-state", "running");

        window.setTimeout(() => {
            $("html").css("animation-play-state", "paused");
            finish_img_animation(img);
        }, 1000);
    });
}

function set_tip(tip) {
    $(() => {
        if (in_progress) {
            console.log("in progress")
            return;
        }

        in_progress = true;

        new_tip = tip;

        // Fade out old tip
        $("#tip").css("opacity", "0%");
        $("#tip").css("animation-play-state", "paused");
        $("#tip").css("animation", "appear 1s infinite");
        $("#tip").css("animation-direction", "reverse");
        $("#tip").css("animation-play-state", "running");

        window.setTimeout(() => {
            $("#tip").css("animation-play-state", "paused");
            finish_animation(tip);
        }, 1000);
    });
}

function finish_animation(tip) {
    console.log(tip);
    // Change text
    $("#tip").text(tip).html();

    // Fade back in
    console.log("fading in")
    $("#tip").css("animation-direction", "normal");
    $("#tip").css("animation-play-state", "running");
    window.setTimeout(() => {
        $("#tip").css("animation-play-state", "paused");
        $("#tip").css("animation", "none");
        $("#tip").css("opacity", "100%");
        console.log("done");
        in_progress = false;
    }, 1000);
}

function finish_img_animation(img) {
    console.log(img);
    // Change text
    $("html").css("background", `url("/images/${img}") no-repeat center center fixed`)
    $("html").css("background-size", `100% 100vh`)

    // Fade back in
    console.log("fading in")
    $("html").css("animation-direction", "normal");
    $("html").css("animation-play-state", "running");
    window.setTimeout(() => {
        $("html").css("animation-play-state", "paused");
        $("html").css("animation", "none");
        $("html").css("opacity", "100%");
        console.log("done");
        in_progress_i = false;
    }, 1000);
}

async function get_tip() {
    $.get("https://tecktip.today:8325/", (data, status) => {
        set_tip(data);
    })
}

async function get_image() {
    $.get("https://tecktip.today:8325/img", (data, status) => {
        set_image(data);
    });
}

$(() => {

})
/*
    $("#tip").on("animationend", () => {
        console.log("anim end");
        $("#tip").removeClass("animate_appear");

        if (current_anim == 0) { // fade out
            console.log("faded out");
            // set opacity to 0
            $("#tip").css("opacity", "0%");
            console.log($("#tip"));
            // fade back in with new tip
            finish_animation(new_tip);
        } else { // fade in
            console.log("faded in");
            // set opacity to 100
            $("#tip").css("opacity", "100%");

            in_progress = false;
        }
    })
})
*/