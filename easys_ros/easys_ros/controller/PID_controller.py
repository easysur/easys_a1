from .PID import PID

class PID_controller:
    def __init__(self, config):
        # PID parameters
        self.rollP = config["rollP"]
        self.rollI = config["rollI"]
        self.rollD = config["rollD"]
        self.pitchP = config["pitchP"]
        self.pitchI = config["pitchI"]
        self.pitchD = config["pitchD"]
        self.dt = config["dt"]

        self.roll_PID = PID(self.rollP, self.rollI, self.rollD, self.dt, -999, 999)
        self.pitch_PID = PID(self.pitchP, self.pitchI, self.pitchD, self.dt, -999, 999)

        self.prev_Vx = 0
        self.prev_Vz = 0
        self.prev_yaw_rate = 0

        # filter parameter
        self.alpha = 0.12

    # Main control routine
    def control(self, current_roll, current_pitch, Vx, Vz, yaw_rate):
        # Define axes: X follows the camera view, Z follows gravity, Y points to the robot's right when seen from behind; origin matches the 9-axis sensor.
        # Vx: velocity along the Z axis (possibly limited to the three values -/0/+)
        # Vz: velocity along the Z axis
        # yaw_rate: angular velocity around the yaw axis

        # low pass filter
        Vx_filtered = (1 - self.alpha) * self.prev_Vx + self.alpha * Vx
        Vz_filtered = (1 - self.alpha) * self.prev_Vz + self.alpha * Vz
        yaw_rate_filtered = (1 - self.alpha) * self.prev_yaw_rate + self.alpha * yaw_rate

        self.prev_Vx = Vx_filtered
        self.prev_Vz = Vz_filtered
        self.prev_yaw_rate = yaw_rate_filtered

        # Thruster outputs; indices 0-3 from left to right when viewing the robot from behind.
        # The values set to 1.0 are tuning parameters; adjust them after experimentation.
        # These parameters have length units; treat them as the lever arm used to convert to torque.
        kr = 1.0
        kp = 1.0
        ky = 1.0
        T1 = -(0.5*(kp*self.pitch_PID.control(current_pitch, 0) + kr*self.roll_PID.control(current_roll, 0)) + Vz_filtered)
        T2 = -(0.5*(kp*self.pitch_PID.control(current_pitch, 0) - kr*self.roll_PID.control(current_roll, 0)) + Vz_filtered)
        T0 = Vx_filtered - yaw_rate_filtered*ky
        T3 = Vx_filtered + yaw_rate_filtered*ky

        # Entry 0: forward thrust (x-axis) and yaw contribution; lower left.
        # Entry 1: yaw, roll, and pitch contributions; upper left.
        # Entry 2: yaw, roll, and pitch contributions; upper right.
        # Entry 3: forward thrust (x-axis) and yaw contribution; lower right.
        thruster = [T0,T1,T2,T3]
        return thruster
