function scrape() {
    let elements = document.querySelectorAll("#ys-chat-msgs .ys-player");
    let ids = [];
    elements.forEach((e) => {
        let id = e.dataset["id"];
        if (id) {
            ids.push(id);
        }
    });
    return ids.toString();
}

let ids;
setInterval(function () {
    // This should put it on the clipboard automatically.
    ids = scrape();
    console.log(ids);
}, 5000);

// code for getting the ids from yahoo
function scrapePlayers() {
    let players = document.querySelectorAll(".ysf-player-name");
    let out = [];
    players.forEach((p) => {
        let splitURL = p.children[0].href.split("/");
        let id = splitURL[splitURL.length-1];
        out.push(id + "|" + p.innerText);
    });
    return out.toString();
}

