import time
import math
from .PIDController import RobotPIDController

class Robot:
    def __init__(self, start_lat=40.98235397234183, start_lon=29.05953843050679):
        self.lat = start_lat  # Start latitude
        self.lon = start_lon  # Start longitude
        self.speed = 0.0002   # Speed (degree/second) - For precise movement
        self.status = "stopped"  # Status: stopped, moving, paused
        self.path = []        # Path to follow
        self.current_target = 0  # Current target waypoint
        self.heading = 0      # Heading (degree)
        self.arrival_threshold = 0.0003  # Arrival threshold (3x increased - easier transition)
        
        self.pid_controller = RobotPIDController()
        self.use_pid = True  # Enable/disable PID control
        
    def set_path(self, path_coordinates):
        self.path = path_coordinates
        self.current_target = 0
                
        if self.path and len(self.path) > 0:
            first_waypoint = self.path[0]
            self.lat = first_waypoint[0]
            self.lon = first_waypoint[1]
        
    def set_speed(self, new_speed):
        if new_speed > 0:
            self.speed = new_speed
    
    def set_pid_mode(self, use_pid):
        self.use_pid = use_pid
        if use_pid:
            self.pid_controller.reset_controllers()
    
    def set_position_pid_gains(self, kp, ki, kd):
        self.pid_controller.set_position_gains(kp, ki, kd)
    
    def set_heading_pid_gains(self, kp, ki, kd):  
        self.pid_controller.set_heading_gains(kp, ki, kd)
    
    def get_pid_gains(self):
        return {
            "position": {
                "kp": self.pid_controller.position_pid.kp,
                "ki": self.pid_controller.position_pid.ki,
                "kd": self.pid_controller.position_pid.kd
            },
            "heading": {
                "kp": self.pid_controller.heading_pid.kp,
                "ki": self.pid_controller.heading_pid.ki,
                "kd": self.pid_controller.heading_pid.kd
            }
        }
        
    def start(self):
        if self.path:
            self.status = "moving"
            return True
        return False
        
    def stop(self):
        self.status = "stopped"
        
    def pause(self):
        self.status = "paused"
        
    def get_status(self):
        status = {
            "lat": self.lat,
            "lon": self.lon,
            "speed": self.speed,
            "status": self.status,
            "heading": self.heading,
            "current_target": self.current_target,
            "total_waypoints": len(self.path),
            "use_pid": self.use_pid
        }
        
        if self.use_pid and self.path and self.current_target < len(self.path):
            target_lat, target_lon = self.get_target_coordinates()
            if target_lat is not None:
                distance = self.calculate_distance(self.lat, self.lon, target_lat, target_lon)
                desired_heading = self.calculate_heading(self.lat, self.lon, target_lat, target_lon)
                heading_error = self.normalize_angle(desired_heading - self.heading)
                
                pid_debug = self.pid_controller.get_debug_info(distance, heading_error)
                status["pid_debug"] = pid_debug
        
        return status
        
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)
    
    def calculate_heading(self, lat1, lon1, lat2, lon2):
        lat_diff = lat2 - lat1
        lon_diff = lon2 - lon1
        heading_rad = math.atan2(lon_diff, lat_diff)
        heading_deg = math.degrees(heading_rad)
        return (heading_deg + 360) % 360
    
    def get_target_coordinates(self):
        if self.current_target < len(self.path):
            coords = self.path[self.current_target]
            return coords[0], coords[1]
        return None, None
        
    def update_position(self):
        if self.status != "moving" or not self.path:
            return
            
        target_lat, target_lon = self.get_target_coordinates()
        if target_lat is None:
            return
        
        if self.use_pid:
            self._update_position_with_pid(target_lat, target_lon)
    
    def _update_position_with_pid(self, target_lat, target_lon):
        distance = self.calculate_distance(self.lat, self.lon, target_lat, target_lon)
        desired_heading = self.calculate_heading(self.lat, self.lon, target_lat, target_lon)
        heading_error = self.normalize_angle(desired_heading - self.heading)
        
        if distance < self.arrival_threshold:
            self._move_to_next_waypoint()
            return
        
        speed_command = abs(self.pid_controller.update_position_control(-distance))
        
        turn_rate = self.pid_controller.update_heading_control(heading_error)
        
        dt = 0.5
        
        self.heading += turn_rate * dt
        self.heading = self.normalize_angle(self.heading)
        
        heading_rad = math.radians(self.heading)
        self.lat += speed_command * math.cos(heading_rad) * dt
        self.lon += speed_command * math.sin(heading_rad) * dt
    

    def _move_to_next_waypoint(self):
        self.current_target += 1
        if self.current_target >= len(self.path):
            self.status = "completed"
        else:
            target_lat, target_lon = self.get_target_coordinates()
            if target_lat is not None:
                self.heading = self.calculate_heading(self.lat, self.lon, target_lat, target_lon)
                if self.use_pid:
                    self.pid_controller.reset_controllers()
    
    def normalize_angle(self, angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle 