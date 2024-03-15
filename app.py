import base64
import json

from flask import Flask, jsonify, request
import os
import pprint

from werkzeug.exceptions import HTTPException

from rmbg import inference

app = Flask(__name__)

@app.errorhandler(Exception)
def server_error(e):
    # pprint.pprint(e)
    return jsonify(error=str(e)), 500

@app.errorhandler(HTTPException)
def not_found(e):
    # pprint.pprint(e)
    return jsonify(error=str(e)), e.code

@app.route("/api/status")
def status():
    return jsonify({"status": "ok"})

@app.route("/api/rmbg", methods=["POST"])
def rmbg():
    data = request.data or '{}'
    body = json.loads(data)
    base64_image = body.get("image")
    img_bytes = base64.decodebytes(base64_image.encode())
    result_bytes = inference(img_bytes)
    # with open("/home/cchase/git/github/cfchase/rmbg-service/examples/result_bytes.png", "wb") as binary_file:
    #     # Write bytes to file
    #     binary_file.write(result_bytes)

    base64_result = base64.b64encode(result_bytes)
    # print(type(base64_result.decode()))
    #
    # with open("/home/cchase/git/github/cfchase/rmbg-service/examples/result_bytes.txt", "w") as outfile:
    #     outfile.write(base64_result.decode())
    #
    # with open("/home/cchase/git/github/cfchase/rmbg-service/examples/result_bytes.json", "w") as outfile:
    #     outfile.write(json.dumps({
    #         "image": base64_result.decode()
    #     }, indent=4))

    return jsonify({
        "image": base64_result.decode()
    })


if __name__ == '__main__':
    port = os.environ.get('FLASK_PORT') or 8080
    port = int(port)

    app.run(port=port,host='0.0.0.0')
