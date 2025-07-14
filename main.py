from planner.Path import Path
from flask import Flask, render_template, request,make_response,jsonify

all_markers = [{'lat': 40.98765, 'lon': 29.05748}]

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/map")
def map():
    return render_template('Map.html',markers = all_markers)

@app.route("/add_marker", methods=['POST', 'GET'])
def add_marker():
    if request.method == 'POST':
        lat = float(request.form['lat'])
        lon = float(request.form['lon'])
        all_markers.append({'lat': lat, 'lon': lon})
        return make_response(jsonify({"message": "markes add operation is succes", "status": "success"}), 200)

# def main():
#     path = Path()
#     path.drawMap()
#     path.addMarker([40.98765,29.05748],"Start Point")
#     path.printMap()

if __name__ == "__main__":
    app.run()