from flask import Flask, jsonify,request

from db import Technician

app = Flask(__name__)

# load data from the json file

data = Technician()

@app.route("/technicians")
def root(methods=["GET"]):
    # returns the all the distances for each tech if no arguments are provided
    name = request.args.get("name",default = "", type = str)
    unit = request.args.get("unit", default = "m", type = str)
    if unit not in ["m", "ft"]:
        # we dont support that unit
        return jsonify({"error":{"type": "INVALID_ARGUMENT", "field": "unit"}}), 400

    response = {}

    if not name:
        for name, tech_data in data.fetch_all_distances().items():
            response[name] = {}
            for other_name, dist in tech_data.items():
                d = None
                if unit == "m":
                    d = dist.m
                elif unit == "ft":
                    d = dist.ft
                response[name][other_name] = {
                    f"distance_{unit}":d,
                    "is_within_1000ft": True if dist.ft <= 1000 else False
                }
    else:
        try:
            for other_name, dist in data.fetch_distance(name):
                d = None
                if unit == "m":
                    d = dist.m
                elif unit == "ft":
                    d = dist.ft
                response[name][other_name] = {
                    f"distance_{unit}":d,
                    "is_within_1000ft": True if dist.ft <= 1000 else False
                }
        except KeyError:
            return jsonify({"error":{"type": "INVALID_ARGUMENT", "field": "name"}}), 404

    return jsonify({"data":response}),200


app.run()
