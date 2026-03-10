from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from startup_india import startup_india as si
from IEcode import IEcode as ie
from udayam import udayam as ud
import datetime
import threading
import queue
import json

app = Flask(__name__)

# ─── OTP QUEUES ──────────────────────────────────────────────────────────────
# otp_request_queue  : Python → browser  (tells browser "need OTP")
# otp_response_queue : browser → Python  (browser submits OTP values)
otp_request_queue  = queue.Queue()
otp_response_queue = queue.Queue()

# ─── HTML ROUTES ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/startup_india_form")
def startup_india_form():
    return render_template("startup_india_form.html")

@app.route("/single_file")
def single_file():
    return render_template("single_file.html")

@app.route("/allbasefile")
def allbasefile():
    return render_template("allbasefile.html")

@app.route("/multiplefiles")
def multiplefiles():
    return render_template("multiplefiles.html")

@app.route("/otp")
def otp_page():
    return render_template("otp.html")

# ─── SSE: Python notifies browser that OTP is needed ─────────────────────────
@app.route("/otp_stream")
def otp_stream():
    """
    Browser connects here via EventSource.
    When Python needs OTP, it puts a message in otp_request_queue.
    This endpoint picks it up and sends it to the browser as SSE.
    """
    def generate():
        yield "data: connected\n\n"
        while True:
            try:
                msg = otp_request_queue.get(timeout=120)  # wait up to 2 min
                yield f"data: {json.dumps(msg)}\n\n"
            except queue.Empty:
                yield "data: heartbeat\n\n"  # keep connection alive

    return Response(
        stream_with_context(generate()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no"
        }
    )

# ─── Browser submits OTP back to Python ──────────────────────────────────────
@app.route("/otp_submit", methods=["POST"])
def otp_submit():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No OTP data received"}), 400

    mobile_otp = data.get("mobile_otp", "")
    email_otp  = data.get("email_otp", "")

    if not mobile_otp or not email_otp:
        return jsonify({"status": "error", "message": "Both Mobile OTP and Email OTP are required"}), 400

    otp_response_queue.put({"mobile_otp": mobile_otp, "email_otp": email_otp})
    return jsonify({"status": "success", "message": "OTP submitted successfully"})

# ─── STARTUP INDIA ───────────────────────────────────────────────────────────
@app.route("/startup_india", methods=["POST"])
def call_startup_india():
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON payload in the request body",
            "timestamp": datetime.datetime.now().isoformat()
        }), 400

    # Pass the two queues into the script via data dict
    data["_otp_request_queue"]  = otp_request_queue
    data["_otp_response_queue"] = otp_response_queue

    result = si(data)

    return jsonify({
        "status": "success",
        "message": "Script executed",
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    })

# ─── IE CODE ─────────────────────────────────────────────────────────────────
@app.route("/IECODE", methods=["POST"])
def call_iecode():
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON payload in the request body",
            "timestamp": datetime.datetime.now().isoformat()
        }), 400
    try:
        result = ie()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }), 500
    return jsonify({
        "status": "success",
        "message": "Script executed",
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    })

# ─── UDAYAM ──────────────────────────────────────────────────────────────────
@app.route("/udayam", methods=["POST"])
def call_udayam():
    data = request.get_json()
    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON payload in the request body",
            "timestamp": datetime.datetime.now().isoformat()
        }), 400
    try:
        result = ud()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "timestamp": datetime.datetime.now().isoformat()
        }), 500
    return jsonify({
        "status": "success",
        "message": "Script executed",
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)
