import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import UInt16
from rosbot_msgs.msg import ArmPulses, BlockDetection, InverseMsg
 
import numpy as np


class MANAGERNode(Node):
    def __init__(self):
        super().__init__('manager_node')
        self.first = True
	
        #Subscribing to the block detection topic
        #self.block_sub = self.create_subscription(
        #        BlockDetection,'block_detector',self.block_callback,10)
                
        self.control_timer = self.create_timer(2.0, self.timer_callback)
        
        self.arm_pub = self.create_publisher(
        	ArmPulses, '/arm_control', 10)
        
        self.grip_pub = self.create_publisher(
        	UInt16, '/grip_control', 10)
    
    def start(self):	
        startPose = [500, 600, 20, 250, 500, 350]
        arm_msg = ArmPulses()
        arm_msg.ids = [1, 2, 3, 4, 5]
        arm_msg.pulses = startPose
        self.arm_pub.publish(arm_msg)
        
    
    def timer_callback(self):
        if self.first:
            self.start()
            self.first = False

        time.sleep(2)

        ## Find block

        ## Pass block info to ik_node

        ## Change gripper
        # Publish a valid ArmPulses message here
        time.sleep(1)

        ## Move back
        self.start()
        time.sleep(1)

        ## Move block somewhere
   	
def main():
    rclpy.init()
    manager_node = MANAGERNode()
    rclpy.spin(manager_node)
    rclpy.shutdown()

