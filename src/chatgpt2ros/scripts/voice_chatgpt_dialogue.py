#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import requests
import base64
from io import BytesIO
import sys
import select
from threading import Event
from queue import Queue
from threading import Thread

import wave
import speech_recognition as sr

def handle_audio(msg):
    global audio_queue
    rospy.loginfo("Message from audio: %s", msg.data)
    audio_queue.put(msg.data.rstrip('\n'))

def process_audio_queue():
    global audio_queue, response_received
    while not rospy.is_shutdown():
        if not audio_queue.empty():
            user_input = audio_queue.get()
            user_input_pub.publish(user_input)
            response_received.wait()
            response_received.clear()

def handle_chatgpt_reply(msg):
    rospy.loginfo("\rBot: {}".format(msg.data))
    response_received.set()

def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    return None

if __name__ == "__main__":
    rospy.loginfo("Initializing Voice ChatGPT dialogue node...")
    
    rospy.init_node("voice_chatgpt_dialogue_node")
    rospy.Subscriber("audio", String, handle_audio, queue_size=10)
    rospy.Subscriber("chatgpt_reply", String, handle_chatgpt_reply, queue_size=10)
    
    user_input_pub = rospy.Publisher("user_input", String, queue_size=10)
    rospy.loginfo("ChatGPT dialogue node is running. Type your message and press Enter.")

    audio_queue = Queue()
    response_received = Event()
    response_received.clear()

    audio_thread = Thread(target=process_audio_queue)
    audio_thread.start()

    rospy.spin()
