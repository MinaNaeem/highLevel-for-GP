#!/usr/bin/env python
import curses
import rospy
from std_msgs.msg import Int32


screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)


def main():
    dc = rospy.Publisher('cmd_vel', Int32, queue_size=10)
    steer = rospy.Publisher('cmd_angle', Int32, queue_size=10)

    vel = 0
    angle = 90

    rospy.init_node('inputnode', anonymous=True)
    rospy.loginfo("Node started successfully")
    rate = rospy.Rate(1000)
    try:
        while not rospy.is_shutdown():
            char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
                print("Forward")
                vel += 1
                if vel > 1:
                    vel = 1

            elif char == curses.KEY_DOWN:
                print("Reverse")
                vel -= 1
                if vel < -1:
                    vel = -1

            elif char == curses.KEY_RIGHT:
                print("Turning Right")
                angle += 10
                if angle > 145:
                    angle = 145

            elif char == curses.KEY_LEFT:
                print("Turning Left")
                angle -= 10
                if angle < 60:
                    angle = 60

            elif char == 10:   #Enter for stop 
                print("stopping")
                vel = 0

            dc.publish(vel)
            steer.publish(angle)

            rate.sleep()

    finally:
        # Close down curses properly, inc turn echo back on!
        curses.nocbreak()
        screen.keypad(0)
        curses.echo()
        curses.endwin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
