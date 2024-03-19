import base64
import json
import os
import pprint

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException
from rmbg import inference

app = Flask(__name__)


@app.errorhandler(Exception)
def server_error(e):
    pprint.pprint(e)
    return jsonify(error=str(e)), 500


@app.errorhandler(HTTPException)
def not_found(e):
    pprint.pprint(e)
    return jsonify(error=str(e)), e.code


@app.route("/api/status")
def status():
    return jsonify({"status": "ok"})


@app.route("/api/rmbg", methods=["POST"])
def rmbg():
    # with open("data.txt", "wb") as binary_file:
    #     binary_file.write(request.data)
    data = request.data or '{"image": ""}'
    body = json.loads(data)
    base64_image = body.get("image")
    img_bytes = base64.decodebytes(base64_image.encode())
    # print(type(img_bytes))
    # with open("request_image.jpg", "wb") as binary_file:
    #     binary_file.write(img_bytes)

    result_bytes = inference(img_bytes)

    # with open("result_image.png", "wb") as binary_file:
    #     binary_file.write(result_bytes)

    base64_result = base64.b64encode(result_bytes)

    return jsonify({
        "image": base64_result.decode()
    })


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
