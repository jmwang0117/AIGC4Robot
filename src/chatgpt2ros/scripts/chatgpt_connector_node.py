#!/usr/bin/env python3

import rospy
import openai
import json
import threading
from std_msgs.msg import String
from queue import Queue

# Read OpenAI API key from a JSON file
def read_api_key_from_file(filename):
    with open(filename, "r") as file:
        data = json.load(file)
        return data["api_key"]

api_key = read_api_key_from_file("/home/catkin_ws/src/chatgpt2ros/scripts/api_key.json")
openai.api_key = api_key

# Global variables
user_input_queue = Queue()
conversation_history = []

def handle_user_input(msg):
    global user_input_queue
    user_input_queue.put(msg.data)

def chatgpt_reply_thread():
    global user_input_queue, conversation_history
    while not rospy.is_shutdown():
        if not user_input_queue.empty():
            user_input = user_input_queue.get()
            conversation_history.append(user_input)

            prompt = "\n\nUser: " + "\n\nAssistant: ".join(conversation_history) + "\n\nUser: "
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.5,
            )
            reply = response.choices[0].text.strip()
            #rospy.loginfo("GPT replied: %s", reply)
            chat_pub.publish(reply)
            conversation_history.append(reply)

if __name__ == "__main__":
    rospy.init_node("chatgpt_connector_node")
    chat_pub = rospy.Publisher("chatgpt_reply", String, queue_size=10)
    rospy.Subscriber("user_input", String, handle_user_input, queue_size=10)

    reply_thread = threading.Thread(target=chatgpt_reply_thread)
    reply_thread.start()

    rospy.loginfo("ChatGPT connector node is running.")
    rospy.spin()

