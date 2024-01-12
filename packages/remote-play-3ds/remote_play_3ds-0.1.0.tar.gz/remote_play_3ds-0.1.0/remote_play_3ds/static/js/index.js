/**
 * @param obj {{type: "hatRelease" | "slidepadRelease" | "touchscreenRelease"} | {type: "buttonHold" | "buttonRelease" | "hatHold", id: number} | {type: "slidepadHold" | "touchscreenHold", x: number, y: number}}
 */
function postControl(obj) {
    setTimeout(() => {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/control", true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(obj));
    }, 0);
}

for (let id of [0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 12]) {
    const button = document.getElementById(`button${id}`);
    button.onmousedown = () => postControl({ type: "buttonHold", id: id });
    button.onmouseup = () => postControl({ type: "buttonRelease", id: id });
}

for (let id = 0; id < 8; id++) {
    const hat = document.getElementById(`hat${id}`);
    hat.onmousedown = () => postControl({ type: "hatHold", id: id });
    hat.onmouseup = () => postControl({ type: "hatRelease" });
}

const video = document.getElementById("video");
let coord = null;
const rectX = 40;
const rectY = 250;
const rectWidth = 320;
const rectHeight = 240;

function isOnTouchScreen(x, y) {
    return x >= rectX && x <= rectX + rectWidth &&
        y >= rectY && y <= rectY + rectHeight
}

video.addEventListener("mousedown", (e) => {
    const mouseX = e.offsetX;
    const mouseY = e.offsetY;

    if (isOnTouchScreen(mouseX, mouseY)) {
        coord = { x: mouseX - rectX, y: mouseY - rectY };
        postControl({ type: "touchscreenHold", ...coord });
    }
});
video.addEventListener("mousemove", (e) => {
    if (!coord) {
        return;
    }

    const mouseX = e.offsetX;
    const mouseY = e.offsetY;

    let x = mouseX - rectX;
    x = (x < 0 ? 0 : (rectWidth < x ? rectWidth : x));
    let y = mouseY - rectY;
    y = (y < 0 ? 0 : (rectHeight < y ? rectHeight : y));
    coord = { x: x, y: y };
    postControl({ type: "touchscreenHold", ...coord });
});
video.addEventListener("mouseup", (e) => {
    if (!coord) {
        return;
    }

    coord = null;
    postControl({ type: "touchscreenRelease" });
});

const slidepad = nipplejs.create({
    zone: document.getElementById("slidepad"),
    color: "black",
    mode: "static",
    size: 85,
    position: { top: "50%", left: "50%" }
});
slidepad.on("move", (_, data) => {
    // vector.x is -1 at the left and 1 at the right
    // vector.y is -1 at the top and 1 at the bottom
    const x = Math.round((data.vector.x + 1) / 2 * 255);
    const y = Math.round((data.vector.y * -1 + 1) / 2 * 255);
    postControl({ type: "slidepadHold", x: x, y: y });
}).on("end", () => {
    postControl({ type: "slidepadRelease" });
});