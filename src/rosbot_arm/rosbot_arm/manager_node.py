import rclpy
import time
from rclpy.node import Node

from rosbot_msgs.msg import ArmPulses, BlockDetection, InverseMsg, Grip
 
import numpy as np


class MANAGERNode(Node):
    def __init__(self):
        super().__init__('manager_node')
        self.first = True
        self.arm_msg = ArmPulses()
        self.grip_msg = Grip()
        self.ik_msg = InverseMsg()
        self.test = False
        self.testIK = True

        #TEST!!! Publish to IK
        self.ik_pub = self.create_publisher(
                InverseMsg,'ik_node',10)
	
        #Subscribing to the block detection topic
        #self.block_sub = self.create_subscription(
        #        BlockDetection,'block_detector',self.block_callback,10)
                
        self.control_timer = self.create_timer(2.0, self.timer_callback)
        
        self.arm_pub = self.create_publisher(
        	ArmPulses, '/arm_control', 10)
        
        self.grip_pub = self.create_publisher(
        	Grip, '/grip_control', 10)
    
    def start(self):	
        startPose = [500, 600, 20, 250, 500]
        #arm_msg = ArmPulses()
        self.arm_msg.ids = [1, 2, 3, 4, 5]
        self.arm_msg.pulses = startPose

        print("Start Function Operating")
        self.arm_pub.publish(self.arm_msg)
        
    
    def timer_callback(self):
        if self.first:
            self.start()
            self.first = False

            print('Callback Function Operating')
            self.grip_pub.publish(self.grip_msg)
            print('Grip published')

        if self.test:
	        ## Find block
	
	        ## Pass block infor to ik_node
            time.sleep(2)
	        ## Change Gripper
            print('Closing the gripper')
            self.grip_msg.open = False
            self.grip_pub.publish(self.grip_msg)
            time.sleep(2)

            print('Opening gripper')
            self.grip_msg.open = True
            self.grip_pub.publish(self.grip_msg)
            time.sleep(2)
   	
   	        ## Move back
            self.arm_msg.pulses = [500,500,500,500,500]
            self.arm_pub.publish(self.arm_msg)
            time.sleep(2)

            self.arm_msg.pulses = [500,600,20,250,500]
            self.arm_pub.publish(self.arm_msg)
            time.sleep(2)
   	        ## Move block somewhere

        if self.testIK:
            self.ik_msg.x = 0.1
            self.ik_msg.y = 0.1
            self.ik_msg.z = 0.1
            self.ik_msg.pitch = 90.0
            self.ik_msg.roll = 0.0

            print('Moving arm 1')
            
            self.ik_pub.publish(self.ik_msg)
            time.sleep(2)

            self.ik_msg.x = 0.0
            self.ik_msg.y = 0.0
            self.ik_msg.z = 0.0
            self.ik_msg.x = 90.0
            self.ik_msg.x = 0.0

            print('Moving arm 2')
            
            self.ik_pub.publish(self.ik_msg)
            time.sleep(2)

   	
def main():
    rclpy.init()
    manager_node = MANAGERNode()
    rclpy.spin(manager_node)
    rclpy.shutdown()

