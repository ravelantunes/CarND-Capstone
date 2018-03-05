
GAS_DENSITY = 2.858
ONE_MPH = 0.44704

from yaw_controller import YawController
from pid import PID

class Controller(object):
    def __init__(self, wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle):
        self.dbw_enabled = True

        # Initialize utility controllers
        self.yaw_controller = YawController(wheel_base, steer_ratio, min_speed, max_lat_accel, max_steer_angle)
        self.throttle_pid_controller = PID(1.0, 1.0, 1.0)
        self.steering_pid_controller = PID(1.0, 1.0, 1.0)

        # Initialize state that will be updated nodes dbw is subscribed to
        self.current_velocity = None
        self.twist = None

    def toggle_dbw(self, dbw_enabled):
        self.dbw_enabled = dbw_enabled

    def control(self):
        # Return 0 values if state not populated yet
        if self.current_velocity is None or self.twist is None:
            return 0.01, 0.0, 0.0
       
        throttle = self.control_throttle()
        steering = self.control_steering()

        # Return throttle, brake, steer
        return max(0.0, throttle), min(0.0, throttle), steering


    def control_throttle(self):
        self.velocity_error = self.twist.linear.x - self.current_velocity.linear.x
        throttle = self.throttle_pid_controller.step(self.velocity_error, 50)
        throttle = max(0.0, min(1.0, throttle))
        return throttle

    def control_steering(self):
        steering = self.yaw_controller.get_steering(self.twist.linear.x, self.twist.angular.z, self.current_velocity.linear.x)
        return steering        
