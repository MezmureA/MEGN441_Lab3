import rclpy
from rclpy.node import Node
from std_msgs.msg import UInt16
from rosbot_msgs.msg import ArmPulses
from ros_robot_controller.ros_robot_controller_sdk import Board


class ArmControl(Node):
    def __init__(self):
        super().__init__('arm_control')
        # TODO: Subscribe to a forward control topic
        self.arm_sub = self.create_subscription(
                ArmPulses,'/arm_control',self.direct,10)
        # TODO: Subscribe to a gripper control topic
        self.grip_sub = self.create_subscription(
                UInt16, '/grip_control', self.gripper_callback,10)


    # TODO: Write an arm_control node to receive joint angles
    # and send messages to the Board.
    def direct(self,arm_pulses):
        board = Board()
        targets = []
        for i in range(4):
            targets.append((arm_pulses.ids[i], arm_pulses.pulses[i]))		
        
        board.bus_servo_set_position(1.0, targets)
    	
    def gripper_callback(self,gripper_pulse):
        board = Board()
        targets = [(10, gripper_pulse.data)]
        board.bus_servo_set_position(1.0, targets)
		

    # See arm_test for example of board functionality.


def main():
    rclpy.init()
    node = ArmControl()
    rclpy.spin(node)
    rclpy.shutdown()
    

if __name__=="__main__":
    main()
