#!/usr/bin/env python3

import sys
import select
import rospy
from std_msgs.msg import String
from threading import Event

def handle_chatgpt_reply(msg):
    print("\rBot: {}".format(msg.data))
    response_received.set()

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    return None

if __name__ == "__main__":
    rospy.init_node("chatgpt_dialogue_node")
    rospy.Subscriber("chatgpt_reply", String, handle_chatgpt_reply, queue_size=10)

    user_input_pub = rospy.Publisher("user_input", String, queue_size=10)
    rospy.loginfo("ChatGPT dialogue node is running. Type your message and press Enter.")

    response_received = Event()

    while not rospy.is_shutdown():
        response_received.clear()
        user_input = input("User: ")
        user_input_pub.publish(user_input)
        
        while not response_received.wait(0.1):
            if input_with_timeout("\rWaiting...\033[K", 0.1) is not None:
                print("\nPlease wait for the bot's response.")
                break
