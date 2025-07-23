from flask import Flask, render_template, request,make_response,jsonify
from flask_cors import CORS
from planner.PathPlanner import PathPlanner
import json
import os
from datetime import datetime

all_markers = []

path_data = None

bookmarks_file = 'bookmarks.json'
bookmarks = []

def load_bookmarks():
    global bookmarks
    if os.path.exists(bookmarks_file):
        try:
            with open(bookmarks_file, 'r', encoding='utf-8') as f:
                bookmarks = json.load(f)
        except:
            bookmarks = []
    else:
        bookmarks = []

def save_bookmarks():
    with open(bookmarks_file, 'w', encoding='utf-8') as f:
        json.dump(bookmarks, f, indent=2, ensure_ascii=False)

load_bookmarks()

options = {
    "is_addMarker" : True,
    "is_addObstacle": False,
    "center_map":{"lat":40.98235397234183, "lon":29.05953843050679}
}

app = Flask(__name__)
CORS(app)

@app.route("/map")
def map():
    return render_template('Map.html', markers=all_markers, path_data=path_data,center_map=options["center_map"])

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
    obstacle_count = 0
    markers = []
    obstacles = []
    
    for marker in all_markers:
        if marker['status'] == 'marker':
            marker_count += 1
            markers.append(marker)
        elif marker['status'] == 'obstacle':
            obstacle_count += 1
            obstacles.append(marker)

    if marker_count >= 2:
        planner = PathPlanner()
        
        marker_coords = []
        for marker in markers:
            marker_coords.append((marker["lat"], marker["lon"]))
        
        obstacle_coords = None
        if obstacles:
            obstacle_coords = [(obs["lat"], obs["lon"]) for obs in obstacles]
        
        try:
            path_edges = planner.CreatePathWithAStar(marker_coords, obstacle_coords)
            
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
                    'obstacle_count': obstacle_count,
                    'algorithm': 'A* with obstacles'
                }
                
                obstacle_message = f" while avoiding {obstacle_count} obstacles" if obstacle_count > 0 else ""
                return make_response(jsonify({
                    "message": f"A* multi-marker path created successfully through {marker_count} markers{obstacle_message}", 
                    "status": "success",
                    "segments": marker_count - 1,
                    "obstacles": obstacle_count,
                    "algorithm": "A* with Haversine heuristic and obstacle avoidance"
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

@app.route("/remove_marker", methods=['POST'])
def remove_marker():
    if request.method == 'POST':
        try:
            lat = float(request.form['lat'])
            lon = float(request.form['lon'])
            
            marker_to_remove = None
            for i, marker in enumerate(all_markers):
                if abs(marker['lat'] - lat) == 0 and abs(marker['lon'] - lon) == 0:
                    marker_to_remove = i
                    break
            
            if marker_to_remove is not None:
                removed_marker = all_markers.pop(marker_to_remove)
                return make_response(jsonify({
                    "message": "Marker removed successfully", 
                    "status": "success",
                    "removed_marker": removed_marker
                }), 200)
            else:
                return make_response(jsonify({
                    "message": "Marker not found", 
                    "status": "error"
                }), 404)
                
        except Exception as e:
            return make_response(jsonify({
                "message": f"Error removing marker: {str(e)}", 
                "status": "error"
            }), 500)
    
    return make_response(jsonify({"message": "Invalid request method", "status": "error"}), 405)

@app.route("/bookmark/save",methods=['POST'])
def bookmark_save():
    global bookmarks
    try:
        bookmark_name = request.form.get('name', f'Route_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        
        if not all_markers:
            return make_response(jsonify({
                "message": "No markers to save", 
                "status": "error"
            }), 400)
            
        if not path_data:
            return make_response(jsonify({
                "message": "No path data to save", 
                "status": "error"
            }), 400)
        
        bookmark = {
            "id": len(bookmarks) + 1,
            "name": bookmark_name,
            "created_at": datetime.now().isoformat(),
            "markers": all_markers.copy(),
            "path_data": path_data.copy(),
            "marker_count": sum(1 for m in all_markers if m['status'] == 'marker'),
            "obstacle_count": sum(1 for m in all_markers if m['status'] == 'obstacle')
        }
        
        bookmarks.append(bookmark)
        save_bookmarks()
        
        return make_response(jsonify({
            "message": f"Route '{bookmark_name}' saved successfully", 
            "status": "success",
            "bookmark": bookmark
        }), 200)
        
    except Exception as e:
        return make_response(jsonify({
            "message": f"Error saving bookmark: {str(e)}", 
            "status": "error"
        }), 500)

@app.route("/bookmarks/list", methods=['GET'])
def bookmarks_list():
    try:
        return make_response(jsonify({
            "bookmarks": bookmarks,
            "count": len(bookmarks),
            "status": "success"
        }), 200)
    except Exception as e:
        return make_response(jsonify({
            "message": f"Error loading bookmarks: {str(e)}", 
            "status": "error"
        }), 500)

@app.route("/bookmark/load/<int:bookmark_id>", methods=['POST'])
def bookmark_load(bookmark_id):
    global all_markers, path_data
    try:
        bookmark = next((b for b in bookmarks if b['id'] == bookmark_id), None)
        
        if not bookmark:
            return make_response(jsonify({
                "message": "Bookmark not found", 
                "status": "error"
            }), 404)
        
        all_markers = bookmark['markers'].copy()
        path_data = bookmark['path_data'].copy()
        
        return make_response(jsonify({
            "message": f"Route '{bookmark['name']}' loaded successfully", 
            "status": "success",
            "bookmark": bookmark
        }), 200)
        
    except Exception as e:
        return make_response(jsonify({
            "message": f"Error loading bookmark: {str(e)}", 
            "status": "error"
        }), 500)

@app.route("/bookmark/delete/<int:bookmark_id>", methods=['DELETE'])
def bookmark_delete(bookmark_id):
    global bookmarks
    try:
        bookmark_to_remove = next((i for i, b in enumerate(bookmarks) if b['id'] == bookmark_id), None)
        
        if bookmark_to_remove is None:
            return make_response(jsonify({
                "message": "Bookmark not found", 
                "status": "error"
            }), 404)
        
        removed_bookmark = bookmarks.pop(bookmark_to_remove)
        save_bookmarks()
        
        return make_response(jsonify({
            "message": f"Route '{removed_bookmark['name']}' deleted successfully", 
            "status": "success"
        }), 200)
        
    except Exception as e:
        return make_response(jsonify({
            "message": f"Error deleting bookmark: {str(e)}", 
            "status": "error"
        }), 500)

if __name__ == "__main__":
    app.run()