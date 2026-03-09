from flask import Flask, request, jsonify
from startup_india import startup_india as si
from IEcode import IEcode as ie
from udayam import udayam as ud
import datetime

app = Flask(__name__)

@app.route("/startup_india", methods=["POST"])
def call_startup_india():

    data = request.get_json()

    if not data:
        return jsonify({
            "status": "error",
            "message": "Missing JSON payload in the request body",
            "timestamp": datetime.datetime.now().isoformat()
        }), 400

    result = si(data)

    return jsonify({
        "status": "success",
        "message": "Script executed",
        "result": result,
        "timestamp": datetime.datetime.now().isoformat()
    })

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
    app.run(debug=True, port=5000)