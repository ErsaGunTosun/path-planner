from planner.Path import Path
from flask import Flask, render_template, request,make_response,jsonify
from flask_cors import CORS
import math
import osmnx as ox
import networkx as nx
import folium

all_markers = [{'lat': 40.98765, 'lon': 29.05748,'status':'marker'}]

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
    
    print(marker_count)
    print(markers)
    if marker_count == 2:
        center_lat = (markers[0]["lat"] + markers[1]["lat"] ) / 2
        center_lon = (markers[0]["lon"]  + markers[1]["lon"] ) / 2
        center_point = (center_lat, center_lon)

        distance_between_points = haversine_distance(markers[0]["lat"], markers[0]["lon"], markers[1]["lat"], markers[1]["lon"])
        radius = distance_between_points * 0.7  
        if radius < 500: 
            radius = 500
        
        source_destination= [markers[0]["lat"],markers[0]["lon"] ]
        target_destionation = [markers[1]["lat"], markers[1]["lon"]]

        G = ox.graph_from_point(center_point, dist=radius, network_type='drive')
        
        gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)
        
        path_edges = []
        for idx, edge in gdf_edges.iterrows():
            coordinates = [[point[1], point[0]] for point in edge.geometry.coords]
            path_edges.append(coordinates)
        
        path_data = {
            'edges': path_edges,
            'center_lat': center_lat,
            'center_lon': center_lon
        }
        
        return make_response(jsonify({"message": "Path created successfully", "status": "success"}), 200)
    else:
        return make_response(jsonify({"message": "Need exactly 2 markers to create path", "status": "error"}), 400)

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
        options["center_map"] = {lat,lon}
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

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371000 
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    app.run()