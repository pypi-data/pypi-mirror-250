import argparse
import atexit
import logging
import signal
import sys
import typing

import cv2
import flask
import qingpi
from qingpi import *  # type: ignore
import serial


app = flask.Flask(__name__)
logging.basicConfig(level=logging.INFO)

cap: cv2.VideoCapture | None = None
ser: serial.Serial | None = None
hold: qingpi.HoldFunction | None = None
release: qingpi.ReleaseFunction | None = None


@app.route("/")
def index():
    return flask.render_template("index.html")


def get_frame():
    assert cap is not None

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            ret, buffer = cv2.imencode(".jpg", frame)
            if not ret:
                break

            frame = buffer.tobytes()
            yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")


@app.route("/video")
def video():
    return flask.Response(
        get_frame(), mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/control", methods=["POST"])
def control():
    assert hold is not None
    assert release is not None

    SUCCESS: typing.Final = "OK", 200

    json = flask.request.json
    if json is None:
        return SUCCESS

    try:
        type = str(json["type"])
    except:
        return SUCCESS

    if type in ["buttonHold", "buttonRelease", "hatHold"]:
        try:
            id = int(json["id"])
        except:
            return SUCCESS

        app.logger.info({"type": type, "id": id})

        Target = Button if type.startswith("button") else Hat
        func = hold if type.endswith("Hold") else release

        func(Target(id))

    elif type in ["slidepadHold", "touchscreenHold"]:
        try:
            x = int(json["x"])
            y = int(json["y"])
        except:
            return SUCCESS

        app.logger.info({"type": type, "x": x, "y": y})

        Target = SlidePad if type.startswith("slidepad") else TouchScreen

        hold(Target(x, y))

    elif type in ["hatRelease", "slidepadRelease", "touchscreenRelease"]:
        app.logger.info({"type": type})

        Target = (
            Hat
            if type.startswith("hat")
            else SlidePad
            if type.startswith("slidepad")
            else TouchScreen
        )

        release(Target)

    return SUCCESS


def _cleanup():
    assert release is not None
    global cap

    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    app.logger.debug("cleanup")

    if cap:
        cap.release()
    release()

    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    global cap, ser, hold, release

    parser = argparse.ArgumentParser(
        prog=__file__,
        description="Remote play your modded 3DS.",
    )
    parser.add_argument(
        "port",
        type=str,
        help="Serial port name.",
    )
    parser.add_argument(
        "index",
        type=int,
        help="Video capture index.",
    )
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.index)
    ser = serial.Serial(args.port)
    hold, release = qingpi.init(ser)

    atexit.register(_cleanup)
    signal.signal(signal.SIGTERM, lambda _0, _1: sys.exit(1))

    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
