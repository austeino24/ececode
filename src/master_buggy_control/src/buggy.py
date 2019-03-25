#!/usr/bin/env python

import rospy
import random
import _random
from std_msgs.msg import Int16
from std_msgs.msg import Byte
from std_msgs.msg import ByteMultiArray

'''
*****************************************************************
*   This function contains the main functionality of the buggy  *
*   - Prototype buggy parameters -                              *
*                                                               *
*   Actuator range:                                             *
*   ---------------- Max right:   700                           *
*   ---------------- Max left:    350                           *
*   Motor max speed:                                            *
*   ---------------- RPM:         100                           *
*   Direction:                                                  *
*   ---------------- Forward:       0                           *
*   ---------------- Reverse:       1                           *
*****************************************************************
'''


def sens_array(val):
    # Store sensor data in array for analysis
    arr = list()
    arr = val.data

    # Threshold values
    front_thres = 48
    side_thres = 36
    c_side_thres = 18

    if arr[1] < front_thres or arr[2] < front_thres:
        # Stop if object too close to front sensors
        motor_publish(0)

    elif arr[3] < c_side_thres or arr[0] < c_side_thres:
        # Stop if object too close to side sensors
        motor_publish(0)

    elif arr[0] < side_thres:
        # Reduce speed
        motor_publish(50)

        # Steer right
        actuator_publish(650)

    elif arr[3] < side_thres:
        # Reduce speed
        motor_publish(50)

        # Steer left
        actuator_publish(400)

    else:
        # Max speed
        motor_publish(100)

        # Go straight
        actuator_publish(525)


def dir_publish(direction):
    # Create direction topics
    pub_motor_dir = rospy.Publisher('dir', Int16, queue_size=1)

    # Publish to topic
    rospy.loginfo(direction)
    pub_motor_dir.publish(direction)


def motor_publish(rpm):
    # Create motor topics
    pub_motor_rpm = rospy.Publisher('rpm', Int16, queue_size=1)

    # Publish to topic
    rospy.loginfo(rpm)
    pub_motor_rpm.publish(rpm)


def actuator_publish(pos):
    # Create linear actuator topics
    pub_actuator = rospy.Publisher('pos', Int16, queue_size=1)

    # Publish to topic
    rospy.loginfo(pos)
    pub_actuator.publish(pos)


def buggy():
    rospy.init_node('buggy', anonymous=True)  # test

    # Initialize Node
    rospy.Subscriber('sens', ByteMultiArray, sens_array)
    
    rate = rospy.Rate(1)  # 10hz

    while not rospy.is_shutdown():
        rate.sleep()
       

if __name__ == '__main__':
    try:
        buggy()
    except rospy.ROSInterruptException:
        pass
