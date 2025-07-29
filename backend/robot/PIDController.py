import time
import math

class PID:
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        
        # Internal variables
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()
        
        # Limits
        self.integral_limit = 100  # Anti-windup
        self.output_limit = None
    
    def set_gains(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki 
        self.kd = kd
    
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint
    
    def set_output_limit(self, min_val, max_val):
        self.output_limit = (min_val, max_val)
    
    def reset(self):
        self.integral = 0
        self.previous_error = 0
        self.last_time = time.time()
    
    def compute(self, current_value):
        now = time.time()
        dt = now - self.last_time
        
        # Avoid division by zero
        if dt <= 0:
            dt = 0.01
        
        # Calculate error
        error = self.setpoint - current_value
        
        # Proportional term
        p_term = self.kp * error
        
        # Integral term with anti-windup
        self.integral += error * dt
        if abs(self.integral) > self.integral_limit:
            self.integral = math.copysign(self.integral_limit, self.integral)
        i_term = self.ki * self.integral
        
        # Derivative term
        derivative = (error - self.previous_error) / dt
        d_term = self.kd * derivative
        
        # PID output
        output = p_term + i_term + d_term
        
        # Apply output limits
        if self.output_limit:
            min_val, max_val = self.output_limit
            output = max(min_val, min(output, max_val))
        
        # Update for next iteration
        self.previous_error = error
        self.last_time = now
        
        return output
    
    def get_components(self, current_value):
        error = self.setpoint - current_value
        p_term = self.kp * error
        i_term = self.ki * self.integral
        d_term = self.kd * (error - self.previous_error)
        
        return {
            'error': error,
            'p_term': p_term,
            'i_term': i_term, 
            'd_term': d_term,
            'output': p_term + i_term + d_term
        }

class RobotPIDController:
    def __init__(self):

        self.position_pid = PID(kp=2.0, ki=0.05, kd=0.1, setpoint=0)
        self.position_pid.set_output_limit(-0.002, 0.002)  # Speed limits (5x düşürüldü)
        
        # Heading PID - yön kontrolü
        self.heading_pid = PID(kp=1.5, ki=0.02, kd=0.1, setpoint=0)  
        self.heading_pid.set_output_limit(-20, 20)  # Turn rate limits (3x düşürüldü)
        
        # Speed PID - hız kontrolü (opsiyonel)
        self.speed_pid = PID(kp=1.0, ki=0.2, kd=0.0, setpoint=0)
        
    def update_position_control(self, current_distance):
        return self.position_pid.compute(current_distance)
    
    def update_heading_control(self, heading_error):
        return self.heading_pid.compute(heading_error)
    
    def set_position_gains(self, kp, ki, kd):
        self.position_pid.set_gains(kp, ki, kd)
    
    def set_heading_gains(self, kp, ki, kd):
        self.heading_pid.set_gains(kp, ki, kd)
    
    def reset_controllers(self):
        self.position_pid.reset()
        self.heading_pid.reset()
        self.speed_pid.reset()
    
    def get_debug_info(self, current_distance, heading_error):
        return {
            'position': self.position_pid.get_components(current_distance),
            'heading': self.heading_pid.get_components(heading_error)
        } 