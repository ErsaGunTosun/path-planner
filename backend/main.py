from planner.Path import Path
from flask import Flask, render_template, request,make_response,jsonify

all_markers = [{'lat': 40.98765, 'lon': 29.05748}]

options = {
    "is_addMarker" : True,
    "is_addObstacle": False,
    "center_map":{"lat":40.98235397234183, "lng":29.05953843050679}
}

app = Flask(__name__)

@app.route("/map")
def map():
    return render_template('Map.html',markers = all_markers)

@app.route("/add_marker", methods=['POST'])
def add_marker():
    if request.method == 'POST':
        if options["is_addMarker"]:
            lat = float(request.form['lat'])
            lon = float(request.form['lon'])
            all_markers.append({'lat': lat, 'lon': lon})
            return make_response(jsonify({"message": "markes add operation is succes", "status": "success"}), 200)
        else:
            return make_response(jsonify({"message":"marked add status is false","status":"errror"}),400)
    
    return make_response(jsonify({"message":"...","status":"errror"}),500)


@app.route("/change_center",methods=['POST'])
def change_center():
    if request.method == 'POST':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        options["center_map"] = {lat,lon}
        return make_response(jsonify({"message": "center change operation is succes", "status": "success"}), 200)
    
    return make_response(jsonify({"message":"...","status":"errror"}),500)


if __name__ == "__main__":
    app.run()