# Path Planner

An advanced web-based robotic path planning system that combines real-world mapping data with sophisticated navigation algorithms. Built with Flask backend and React frontend, featuring real-time robot simulation, obstacle avoidance, and comprehensive waypoint management for autonomous navigation research and development.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![React](https://img.shields.io/badge/React-19.1.0-green)
![Flask](https://img.shields.io/badge/Flask-3.1.1-red)
![OSMnx](https://img.shields.io/badge/OSMnx-2.0.5-orange)

## 🎬 Demo Video

[Demo video/GIF would go here]

## Project Overview

This project develops an intelligent path planning system capable of generating optimal routes for robotic navigation using real-world OpenStreetMap data. The system combines advanced graph algorithms, PID control systems, and interactive web interfaces to provide comprehensive path planning solutions for autonomous vehicles and robots.

### Key Features

- **Real-World Path Planning**: OpenStreetMap integration with OSMnx for accurate street-based navigation
- **Interactive Web Interface**: Modern React-based UI with intuitive controls for waypoint management
- **Advanced Robot Simulation**: Realistic robot movement simulation with PID controller for smooth navigation
- **Dynamic Obstacle Avoidance**: Real-time obstacle detection and dynamic path recalculation
- **Intelligent Bookmark System**: Save, organize, and manage favorite locations with quick access
- **Live Robot Tracking**: Real-time visualization of robot position, status, and movement patterns
- **Graph-Based Optimization**: NetworkX algorithms for finding optimal routes with customizable cost functions
- **RESTful API**: Comprehensive API for integration with external robotics systems

## System Architecture

### Core Components

```
backend/
├── main.py                 # Flask application entry point and API routes
├── planner/
│   └── PathPlanner.py     # Core path planning algorithms and graph processing
├── robot/
│   ├── Robot.py           # Robot simulation and movement control
│   └── PIDController.py   # PID control system for smooth navigation
├── static/                # Static web assets and JavaScript modules
│   ├── js/
│   │   ├── main.js            # Main application logic
│   │   ├── map-init.js        # Map initialization and configuration
│   │   ├── marker-manager.js  # Waypoint and marker management
│   │   ├── path-renderer.js   # Path visualization and rendering
│   │   └── robot-control.js   # Robot control interface
│   └── css/
│       └── map.css            # Map styling and UI components
└── templates/
    └── Map.html           # Main map interface template

frontend/
├── src/
│   ├── App.js             # Main React application component
│   └── components/        # Modular React components
│       ├── Map/           # Interactive map component
│       ├── ControlPanel/  # Robot and path control interface
│       ├── BookmarksPanel/# Bookmark management system
│       ├── StatusBar/     # Real-time status display
│       └── TopMenu/       # Navigation and settings menu
```

### Technology Stack

#### Backend Technologies
- **Python 3.8+** with Flask web framework
- **OSMnx 2.0.5**: OpenStreetMap network analysis and graph generation
- **NetworkX 3.4.2**: Advanced graph algorithms for path optimization
- **GeoPandas 1.1.1**: Geospatial data processing and analysis
- **Folium 0.20.0**: Interactive map generation and visualization
- **Matplotlib 3.10.3**: Data visualization and plotting
- **Shapely 2.1.1**: Geometric operations and spatial analysis
- **Flask-CORS**: Cross-origin resource sharing for API access

#### Frontend Technologies
- **React 19.1.0**: Modern UI framework with hooks and context
- **Tailwind CSS 3.4.17**: Utility-first CSS framework for responsive design
- **React Icons 5.5.0**: Comprehensive icon library

### Control Systems

- **PID Controller**: Proportional-Integral-Derivative control for smooth robot movement
- **Path Optimization**: A* and Dijkstra algorithms for optimal route finding
- **Obstacle Avoidance**: Dynamic path recalculation with penalty-based cost functions
- **Real-time Tracking**: Live position updates with configurable update intervals

## Getting Started

### Prerequisites

- **Python 3.8+** with pip package manager
- **Node.js 16+** and npm/yarn

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ErsaGunTosun/ersgn_path-planner.git
   cd ersgn_path-planner
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv ppenv
   source ppenv/bin/activate  # On Windows: ppenv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start Flask server
   python main.py
   ```
   Backend will be available at `http://localhost:5000`

3. **Frontend Setup** (in new terminal):
   ```bash
   cd frontend
   
   # Install Node.js dependencies
   npm install
   
   # Start React development server
   npm start
   ```
   Frontend will be available at `http://localhost:3000`

4. **Open the application**:
   - Navigate to `http://localhost:3000` in your browser
   - The system will automatically connect to the backend API

## Controls & Usage

### Web Interface Controls

| Action | Method | Description |
|--------|--------|-------------|
| **Add Waypoint** | Click on map | Place waypoint markers on the map |
| **Toggle Marker Mode** | Control Panel | Switch between marker and obstacle modes |
| **Create Path** | Control Panel Button | Generate optimal path between waypoints |
| **Start Robot** | Control Panel Button | Begin robot simulation following the path |
| **Pause/Resume** | Control Panel Button | Pause or resume robot movement |
| **Clear Path** | Control Panel Button | Remove current path and reset |
| **Save Bookmark** | Bookmark Panel | Save current location with custom name |
| **Load Bookmark** | Bookmark Panel | Jump to saved location instantly |

### Operating Modes

#### 1. Path Planning Mode
```bash
# Standard workflow for path planning
1. Switch to Marker Mode
2. Click on map to place waypoints
3. Click "Create Path" to generate route
4. Review generated path visualization
```

#### 2. Obstacle Avoidance Mode
```bash
# Adding obstacles to the planning
1. Switch to Obstacle Mode
2. Click on map to place obstacles
3. Create path - system will avoid obstacles
4. Observe dynamic path recalculation
```

#### 3. Robot Simulation Mode
```bash
# Autonomous robot navigation
1. Ensure path is created
2. Click "Start Robot" 
3. Monitor real-time position updates
4. Adjust speed as needed during movement
```

### Advanced Features

#### Real-time Path Optimization
- **Dynamic Recalculation**: Paths automatically update when obstacles are added/removed
- **Cost Function Tuning**: Penalty-based system for obstacle avoidance
- **Multi-objective Optimization**: Balance between distance and safety

#### Bookmark System
- **Location Persistence**: Bookmarks saved in JSON format for future sessions
- **Metadata Storage**: Include custom names, descriptions, and timestamps
- **Quick Navigation**: One-click navigation to frequently used locations

## Technical Details

### Path Planning Algorithm

The system uses advanced graph-based algorithms with OpenStreetMap data:

```python
# Core path planning with obstacle avoidance
def find_optimal_path(self, start_coords, end_coords, obstacle_points=[]):
    # Download OSM network data
    G = ox.graph_from_point(center_point, dist=5000, network_type='drive')
    
    # Apply obstacle penalties
    for u, v, key, data in G.edges(keys=True, data=True):
        if self.is_edge_near_obstacle(u, v, G, obstacle_points):
            G[u][v][key]['length'] *= self.obstacle_penalty
    
    # Find shortest path using NetworkX
    try:
        path = nx.shortest_path(G, start_node, end_node, weight='length')
        return self.extract_coordinates(G, path)
    except nx.NetworkXNoPath:
        return None
```

### Robot Control System

The robot simulation uses a sophisticated PID control system:

```python
class Robot:
    def __init__(self, start_lat=40.982354, start_lon=29.059538):
        self.lat = start_lat
        self.lon = start_lon
        self.speed = 0.0002  # degrees/second
        self.arrival_threshold = 0.0003
        
        # PID controller for smooth movement
        self.pid_controller = RobotPIDController()
        self.use_pid = True
    
    def move_towards_target(self, target_lat, target_lon):
        if self.use_pid:
            return self.pid_controller.calculate_movement(
                self.lat, self.lon, target_lat, target_lon
            )
```

### PID Controller Implementation

```python
class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.integral = 0
        self.previous_error = 0
    
    def calculate(self, error, dt):
        self.integral += error * dt
        derivative = (error - self.previous_error) / dt
        
        # PID calculation
        output = (self.kp * error + 
                 self.ki * self.integral + 
                 self.kd * derivative)
        
        self.previous_error = error
        return output
```

### Real-time Data Processing

The system processes and visualizes data in real-time:

```python
# WebSocket-like updates for robot position
@app.route('/robot/status')
def robot_status():
    return jsonify({
        'position': {'lat': robot.lat, 'lon': robot.lon},
        'status': robot.status,
        'current_target': robot.current_target,
        'heading': robot.heading,
        'speed': robot.speed,
        'path_progress': robot.get_progress_percentage()
    })
```

## API Endpoints

### Path Planning
- `POST /path/create` - Generate optimal path between 2 markers
- `POST /path/create_astar` - Generate A* path with obstacle avoidance (supports multiple markers)
- `POST /path/clear` - Clear current path and all markers

### Robot Control
- `POST /robot/start` - Start or resume robot movement
- `POST /robot/stop` - Stop robot movement completely
- `POST /robot/pause` - Pause robot movement (can be resumed)
- `GET /robot/status` - Get complete robot status and position
- `GET /robot/position` - Get robot position and heading only
- `POST /robot/update` - Update robot position (single step)

### Markers & Map Control
- `POST /add_marker` - Add new waypoint marker or obstacle (based on mode)
- `POST /remove_marker` - Remove specific marker by coordinates
- `POST /change_center` - Change map center coordinates
- `POST /options/marker` - Enable marker placement mode
- `POST /options/obstacle` - Enable obstacle placement mode

### Bookmarks
- `POST /bookmark/save` - Save current route with markers and path
- `GET /bookmarks/list` - Retrieve all saved bookmarks
- `POST /bookmark/load/<bookmark_id>` - Load specific bookmark by ID
- `DELETE /bookmark/delete/<bookmark_id>` - Delete specific bookmark by ID

### Main Routes
- `GET /` - Main map interface (HTML template)
- `GET /map` - Map interface (HTML template)

## Data Storage

The system automatically saves and manages various types of data:

- **`bookmarks.json`**: Persistent storage of user bookmarks with metadata
- **Route cache**: Temporarily stored path calculations for performance
- **Robot logs**: Movement history and performance metrics
- **Map tiles cache**: Offline map data for improved loading times

### Data Structure

#### Bookmark Storage Format
```json
{
  "id": "bookmark_001",
  "name": "Istanbul Technical University",
  "coordinates": {
    "lat": 40.98235397234183,
    "lon": 29.05953843050679
  },
  "created_at": "2025-01-15T10:30:00Z",
  "category": "university",
  "description": "Main campus entrance"
}
```

#### Robot Status Data
```json
{
  "timestamp": 1642234567.123,
  "position": {
    "lat": 40.98235397234183,
    "lon": 29.05953843050679
  },
  "status": "moving",
  "current_target": 2,
  "heading": 45.5,
  "speed": 0.0002,
  "path_progress": 0.65,
  "pid_output": {
    "x": 0.001,
    "y": -0.0005
  }
}
```

## Configuration

### System Parameters (in `backend/main.py`)

```python
# Default application settings
options = {
    "is_addMarker": True,
    "is_addObstacle": False,
    "center_map": {
        "lat": 40.98235397234183, 
        "lon": 29.05953843050679
    }
}
```

### Robot Configuration (in `backend/robot/Robot.py`)

```python
class Robot:
    def __init__(self):
        self.speed = 0.0002           # Speed (degrees/second)
        self.arrival_threshold = 0.0003  # Arrival precision (degrees)
        self.heading = 0              # Initial heading (degrees)
        self.use_pid = True          # Enable PID control
        
        # PID Controller settings
        self.pid_controller = RobotPIDController()
```

### PID Controller Gains (in `backend/robot/PIDController.py`)

```python
class RobotPIDController:
    def __init__(self):
        # Position control PID gains
        self.position_kp = 2.0       # Proportional gain
        self.position_ki = 0.1       # Integral gain  
        self.position_kd = 0.5       # Derivative gain
        
        # Heading control PID gains
        self.heading_kp = 1.5        # Proportional gain
        self.heading_ki = 0.05       # Integral gain
        self.heading_kd = 0.3        # Derivative gain
        
        # Anti-windup limits
        self.max_integral = 100      # Integral windup protection
        self.max_output = 0.001      # Maximum control output
```

### Path Planning Parameters (in `backend/planner/PathPlanner.py`)

```python
class PathPlanner:
    def __init__(self):
        self.obstacle_penalty = 10000      # Obstacle avoidance penalty
        self.search_radius = 5000          # OSM download radius (meters)
        self.network_type = 'drive'        # Road network type
        self.obstacle_radius = 100         # Obstacle detection radius (meters)
```

## Performance Features

### Multi-Path Planning
- **Alternative Routes**: Generate multiple path options with different optimization criteria
- **Dynamic Re-routing**: Real-time path recalculation when obstacles are detected
- **Cost Function Customization**: Adjustable weighting for distance, safety, and time

### Advanced Robot Control
- **Smooth Trajectory Following**: PID-controlled movement with minimal overshoot
- **Adaptive Speed Control**: Dynamic speed adjustment based on path curvature
- **Precision Waypoint Navigation**: High-accuracy waypoint approach and departure