from flask import Flask, request


app = Flask(__name__)
bat_detected = False

@app.route("/on", methods=["GET", "POST"])
def on():
    global bat_detected
    bat_detected = True
    return "OK"

@app.route("/off", methods=["GET", "POST"])
def off():
    global bat_detected
    bat_detected = False
    return "OK"

@app.route("/status", methods=["GET"])
def status():
    global bat_detected
    return "true" if bat_detected else "false"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
