#!/usr/bin/env python

import rospy
from smbus2 import SMBus
from std_msgs.msg import Int16

la_address = 11
bus = SMBus(0)


def write_array(value):
    bus.write_i2c_block_data(la_address, 0, value)
    return -1

    
def pos(data):
    rospy.loginfo(rospy.get_caller_id() + ' POS = %d', data.data)

    array = list()
    array.append((data.data >> 8) & 0xFF)
    array.append(data.data & 0xFF)
    write_array(array)


def actuator():
    # The anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('actuator', anonymous=True)

    rospy.Subscriber('pos', Int16, pos)    

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    actuator()
