import rclpy
from rclpy.node import Node

from rosbot_msgs.msg import ArmPulses, BlockDetection, InverseMsg
 
import numpy as np


##  Joint Links ##
# l0 refers to the height of the arm base wrt base_link
l0 = 0.05 + 0.0654868 + 0.0338648 + 0.0772047
l1 = 0.130
l2 = 0.130
l3 = 0.055
tool_link = 0.117

L = [l0, l1, l2, l3+tool_link, 0]


arm_ids = [1, 2, 3, 4, 5]

# Only joint 2 is limited to protect the screen
min_pulses = [0, 125, 0, 0, 0]
max_pulses = [1000, 775, 1000, 1000, 1000]
min_angles = [-120, -90, -120, -120, -120]
max_angles = [120, 66, 120, 120, 120]



# All joints operate in the range -120 to 120 with a pulse width range of 0 to 1000

# TODO: Write helper scripts to convert from one to the other.

def angle_to_pulse(angle):
    # TODO
    pulse = (25/6)*(angle) + 500
    return pulse

def pulse_to_angle(pulse):
    # TODO
    angle = 0.24*pulse - 120
    
    return angle

class IKNode(Node):
    def __init__(self):
        super().__init__('ik_node')

        #Subscribing to the block detection topic
        #self.block_sub = self.create_subsription(
        #        BlockDetection,'block_detector',self.block_callback,10)
                
        self.ik_sub = self.create_subscription(
        	InverseMsg, '/inverse_kinematics', self.inverse_callback, 10)

        #Instantiating a publisher to upload block data to the robot arm
        self.arm_pub = self.create_publisher(
                ArmPulses,'/arm_control',10)

    def inverse_callback(self,inv_msg):
        xe = inv_msg.x
        ye = inv_msg.y
        ze = inv_msg.z
        phi = inv_msg.pitch
        roll = inv_msg.roll

        print(f'Position received!\nMoving to [{xe},{ye},{ze}]\n at Pitch={phi} and Roll={roll}')
        
        r = np.sqrt((xe**2)+(ye**2))
        x3 = r - L[3]*np.cos(phi)
        y3 = z - L[3]*np.sin(phi) - L[0]
        rw = r - L[3]*np.cos(phi)
        zw = (ze-L[0])-L[3]*np.sin(phi)
        Le = np.sqrt((x3**2)+(y3**2))
        theta_1 = np.arctan2(ye/xe)
        
        theta_3 = 2*np.arctan2(np.sqrt(((L[1]+L[2])**2-rw**2)/(rw**2-(L[1]-L[2])**2)))
        
        theta_2 = np.arctan2(zw/rw)-np.arctan2((L[2]*np.sin(theta_3)/(L[1]+L[2]*np.cos(theta_3))))
	
        theta_4 = phi - theta_2 - theta_3
        
        angles = [theta_1, theta_2, theta_3, theta_4, 500]
        
        arm_msg = ArmPulses()
        arm_msg.ids = arm_ids
        pulses = []
        
        for i in range(4):
            if angles[i] >= max_angles[i]:
                angles[i] = max_angles[i]    
            elif angles [i] <= min_angles[i]:
                angles[i] = min_angles[i]
                pulses.append(angles_to_pulse(angles[i]))
       
        arm_msg.pulses = pulses
        self.arm_pub.publish(arm_msg)

def main():
    rclpy.init()
    ik_node = IKNode()
    rclpy.spin(ik_node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
