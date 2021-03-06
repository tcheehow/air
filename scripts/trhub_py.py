#!/usr/bin/python

# import main ROS python library

import rospy
import mraa
import teraranger
from teraranger_array.msg import RangeArray

# import the Float32 message type

from sensor_msgs.msg import LaserScan

# simple class to contain the node's variables and code

class TROneNode:     # class constructor; subscribe to topics and advertise intent to publish
    def __init__(self):
        self.update_rate = 1 # hertz
#        self.update_timer = 1/ (self.update_rate)
        self.sensor = []

        try:
            self.sensor = [teraranger.TeraRangerOne(address=(0x30 + i), debug=False) for i in range(self.sensorCount)]
            #print i    # advertise that we'll publish on the sum and moving_average topics
            rospy.sleep(1.)
            self.range_pub = [rospy.Publisher("teraranger%d/laser/scan" %(i+1), LaserScan, queue_size=1) for i in range(self.sensorCount)]       
        except:
            print "error initializing terarangers"

        rate = rospy.Rate(self.update_rate)

        while not rospy.is_shutdown():
            self.timer_callback()
            rate.sleep()

        # create the Timer with period self.moving_average_period
#        rospy.Timer(rospy.Duration(self.update_timer, self.timer_callback))

        # print out a message for debugging
#        rospy.loginfo("Created terarangers publishing node with period of %f seconds", self.update_timer)

    # the callback function for the timer event
    def timer_callback(self):         # create the message containing the moving average

        for i in range(len(self.sensor)):
            #print "publishing"
            distance = self.sensor[i].readRangeData()
            #print distance
            #if (distance < 14000 and distance > 200):
            terarangers_msg = LaserScan()
            terarangers_msg.header.frame_id = "base_range"
            terarangers_msg.header.stamp = rospy.Time.now()
            terarangers_msg.angle_min = 0
            terarangers_msg.angle_max = 0
            terarangers_msg.angle_increment = 0
            terarangers_msg.time_increment = 0 # 14 metres
            terarangers_msg.scan_time = 0
            terarangers_msg.range_min = 200
            terarangers_msg.range_max = 14000
            terarangers_msg.ranges = [distance/1000.0]
            terarangers_msg.intensities = [0]
                # publish the moving average
            self.range_pub[i].publish(terarangers_msg)
            rospy.sleep(1.)

if __name__ == "__main__":     # initialize the ROS client API, giving the default node name

    rospy.init_node("teraranger_node")

    node = TROneNode()

    # enter the ROS main loop
    # rospy.spin()
