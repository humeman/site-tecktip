function put(url, data, callback) {
    $.ajax(
        {
            type: "PUT",
            url: url,
            contentType: "application/json",
            data: JSON.stringify(data),
            success: callback,
            error: handle_req_error,
            dataType: "json",
            timeout: 1000
        }
    )
}

function get(url, args, callback) {
    $.ajax(
        {
            type: "GET",
            url: encode_query(url, args),
            success: callback,
            error: handle_req_error,
            dataType: "json",
            timeout: 1000
        }
    )
}

function encode_query(url, data) {
    let args = [];
    for (let item in data) {
        args.push(encodeURIComponent(item) + "=" + encodeURIComponent(data[item]));
    }
    let ext = args.join("&");

    if (ext.length > 0) {
        return `${url}?${ext}`
    } else {
        return url
    }
}

function handle_req_error(xhr, status, error) {
    console.log("request error: ", xhr, status, error);
}

// https://stackoverflow.com/questions/5448545/how-to-retrieve-get-parameters-from-javascript
function getSearchParameters() {
    var prmstr = window.location.search.substr(1);
    return prmstr != null && prmstr != "" ? transformToAssocArray(prmstr) : {};
}

function transformToAssocArray( prmstr ) {
    var params = {};
    var prmarr = prmstr.split("&");
    for ( var i = 0; i < prmarr.length; i++) {
        var tmparr = prmarr[i].split("=");
        params[tmparr[0]] = tmparr[1];
    }
    return params;
}

// https://stackoverflow.com/questions/24816/escaping-html-strings-with-jquery
function escapeHtml(unsafe)
{
    console.log(unsafe);
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
 }