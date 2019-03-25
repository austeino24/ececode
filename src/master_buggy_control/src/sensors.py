#!/usr/bin/env python

import random
import rospy
from smbus2 import SMBus
from std_msgs.msg import Byte
from std_msgs.msg import ByteMultiArray


sens_address = 10
bus = SMBus(1)


def read_array():
    #return [87, 45, 77, 88, 99, 23]
    return bus.read_i2c_block_data(sens_address, 0, 6)
    
    
def sensors():
    # The anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    #pub_sensor = rospy.Publisher('sens', ByteMultiArray, queue_size=6)
    pub_sensor = rospy.Publisher('sens', ByteMultiArray, queue_size=1)
    rospy.init_node('sensors', anonymous=True)

    rate = rospy.Rate(2) # 10hz
    while not rospy.is_shutdown():
        sens = read_array()
        msg = ByteMultiArray(None, sens)
        
        rospy.loginfo(sens)
        #print(type(sens[0]))
        
        pub_sensor.publish(msg)
        #msg.data.clear()
        rate.sleep()
        
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    sensors()
