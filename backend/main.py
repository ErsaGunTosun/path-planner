from flask import Flask, render_template, request,make_response,jsonify
from flask_cors import CORS
from planner.PathPlanner import PathPlanner

all_markers = []

path_data = None

options = {
    "is_addMarker" : True,
    "is_addObstacle": False,
    "center_map":{"lat":40.98235397234183, "lng":29.05953843050679}
}

app = Flask(__name__)
CORS(app)

@app.route("/map")
def map():
    return render_template('Map.html', markers=all_markers, path_data=path_data)

@app.route("/path/create",methods=['POST'])
def create_path():
    global path_data
    marker_count = 0
    markers = []
    
    for marker in all_markers:
        if marker['status'] == 'marker':
            marker_count += 1
            markers.append(marker)

    if marker_count == 2:
        planner = PathPlanner()
        source_destination= [markers[0]["lat"],markers[0]["lon"] ]
        target_destionation = [markers[1]["lat"], markers[1]["lon"]]
       
        path_edges = planner.CreatePathWithPoint(source_destination,target_destionation)

        center_lat = (markers[0]["lat"] + markers[1]["lat"]) / 2
        center_lon = (markers[0]["lon"] + markers[1]["lon"]) / 2

        path_data = {
            'edges': path_edges,
            'center_lat': center_lat,
            'center_lon': center_lon
        }
        
        return make_response(jsonify({"message": "Path created successfully", "status": "success"}), 200)
    else:
        return make_response(jsonify({"message": "Need exactly 2 markers to create path", "status": "error"}), 400)

@app.route("/path/create_astar",methods=['POST'])
def create_astar_path():
    global path_data
    marker_count = 0
    markers = []
    
    for marker in all_markers:
        if marker['status'] == 'marker':
            marker_count += 1
            markers.append(marker)

    if marker_count >= 2:
        planner = PathPlanner()
        
        marker_coords = []
        for marker in markers:
            marker_coords.append((marker["lat"], marker["lon"]))
        
        try:
            path_edges = planner.CreatePathWithAStar(marker_coords)
            
            if path_edges:
                total_lat = sum(marker["lat"] for marker in markers)
                total_lon = sum(marker["lon"] for marker in markers)
                center_lat = total_lat / len(markers)
                center_lon = total_lon / len(markers)

                path_data = {
                    'edges': path_edges,
                    'center_lat': center_lat,
                    'center_lon': center_lon,
                    'marker_count': marker_count,
                    'algorithm': 'A*'
                }
                
                return make_response(jsonify({
                    "message": f"A* multi-marker path created successfully through {marker_count} markers", 
                    "status": "success",
                    "segments": marker_count - 1,
                    "algorithm": "A* with Haversine heuristic"
                }), 200)
            else:
                return make_response(jsonify({
                    "message": "Could not create A* path between markers", 
                    "status": "error"
                }), 400)
                
        except Exception as e:
            return make_response(jsonify({
                "message": f"Error creating A* multi-marker path: {str(e)}", 
                "status": "error"
            }), 500)
    else:
        return make_response(jsonify({
            "message": f"Need at least 2 markers to create path. Currently have {marker_count} markers", 
            "status": "error"
        }), 400)

@app.route("/path/clear",methods=['POST'])
def clear_path():
    global path_data, all_markers

    path_data = None
    all_markers.clear()
    
    return make_response(jsonify({"message": "Path and markers cleared successfully", "status": "success"}), 200)

@app.route("/add_marker", methods=['POST'])
def add_marker():
    if request.method == 'POST':
        if options["is_addMarker"] or options["is_addObstacle"]:
            lat = float(request.form['lat'])
            lon = float(request.form['lon'])
            status = 'marker'
            if options['is_addMarker']:
                status = 'marker'
            elif options['is_addObstacle']:
                status = 'obstacle'

            all_markers.append({'lat': lat, 'lon': lon,'status':status})
            marker_data = {'lat': lat, 'lon': lon,'status':status}

            return make_response(jsonify({"message": "markes add operation is succes", "status": "success","marker":marker_data}), 200)
        else:
            return make_response(jsonify({"message":"marked add status is false","status":"errror"}),400)
    
    return make_response(jsonify({"message":"...","status":"errror"}),500)

@app.route("/change_center",methods=['POST'])
def change_center():
    if request.method == 'POST':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        options["center_map"] = {"lat": lat, "lon": lon}
        return make_response(jsonify({"message": "center change operation is succes", "status": "success"}), 200)
    
    return make_response(jsonify({"message":"...","status":"errror"}),500)

@app.route("/options/marker",methods=['POST'])
def options_marker():
    if request.method == 'POST':
        isMarkerMode = request.form["isMarkeMode"]
        options["is_addMarker"] = True if isMarkerMode == 'true' else False
        if options["is_addMarker"] == True and options["is_addObstacle"] == True:
            options["is_addObstacle"] = False
        return make_response(jsonify({"message": "center change operation is succes", "status": "success"}), 200)
    
@app.route("/options/obstacle",methods=['POST'])
def options_obstacle():
    if request.method == 'POST':
        isObstacleMode = request.form["isObstacleMode"]
        options["is_addObstacle"] = True if isObstacleMode == 'true' else False
        if options["is_addMarker"] == True and options["is_addObstacle"] == True:
            options["is_addMarker"] = False

        return make_response(jsonify({"message": "center change operation is succes", "status": "success"}), 200)



if __name__ == "__main__":
    app.run()