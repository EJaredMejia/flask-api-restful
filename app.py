from flask import Flask, request
import platform
import psutil
import requests

app = Flask(__name__)


def controller_status():
    ram = round(psutil.virtual_memory().total/1000000000, 2)
    return {"status": "server is running", "ram": f"{ram} GB", "operatingSystem": platform.system()}, 200


@app.route("/status")
def status():
    res = controller_status()
    return res


def controller_poke(headers):

    try:
        endpoint_poke_api = headers["endpoint_poke_api"]
        ability_name = headers["ability_name"]

        response = requests.get(endpoint_poke_api).json()

        for ability in response["abilities"]:
            if (ability["ability"]["name"] == ability_name):
                return {"status": "success", "has_ability": True}, 200

    except KeyError:
        return {"status": "error", "message": "invalid URL"}, 400

    except Exception as err:
        return {"status": "error", "message": err.args[0]}, 400

    return {"status": "success", "has_ability": False}, 200


@app.route("/poke")
def has_ability():

    res = controller_poke(request.headers)
    return res


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
