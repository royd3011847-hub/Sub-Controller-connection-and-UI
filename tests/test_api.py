from flask import Flask, jsonify
import math, time

app = Flask(__name__)

start_time = time.time()

@app.route("/boxes_get")
def boxes_get():
    t = time.time() - start_time  # seconds since start

    return jsonify({
        "boxes": [
            {"BoxID": 1, "Name": "depth",   "Value": round(math.sin(t) * 10, 3)},
            {"BoxID": 2, "Name": "heading", "Value": round((t * 30) % 360, 3)},
            {"BoxID": 3, "Name": "speed",   "Value": round(abs(math.cos(t)) * 5, 3)},
            {"BoxID": 4, "Name": "pitch",   "Value": round(math.sin(t * 0.5) * 15, 3)},
            {"BoxID": 5, "Name": "roll",    "Value": round(math.cos(t * 0.7) * 8, 3)},
            {"BoxID": 6, "Name": "temp",    "Value": round(20 + math.sin(t * 0.1) * 2, 3)},
        ]
    })
    
@app.route("/odometry")
def odometry():
    t = time.time() - start_time

    return jsonify({
        "x":      round(math.sin(t) * 5, 3),
        "y":      round(math.cos(t) * 5, 3),
        "z":      round(math.sin(t * 0.5) * 3, 3),
        "vx":     round(math.cos(t) * 1.5, 3),
        "vy":     round(math.sin(t) * 1.5, 3),
        "vz":     round(math.cos(t * 0.5) * 0.8, 3),
        "ax":     round(math.sin(t * 2) * 0.5, 3),
        "ay":     round(math.cos(t * 2) * 0.5, 3),
        "az":     round(9.81 + math.sin(t) * 0.1, 3),
        "roll":   round(math.sin(t * 0.7) * 15, 3),
        "pitch":  round(math.cos(t * 0.5) * 10, 3),
        "yaw":    round((t * 20) % 360, 3),
        "vroll":  round(math.cos(t) * 2, 3),
        "vpitch": round(math.sin(t) * 1.5, 3),
        "vyaw":   round(math.sin(t * 0.3) * 3, 3),
    })

@app.route("/command_publisher", methods=["POST"])
def command_publisher():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)