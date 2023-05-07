#!/usr/bin/env python3
import wave
import rospy
from std_msgs.msg import String
import speech_recognition as sr

def transcribe_audio_file(audio_file_path):
    try:
        with open(audio_file_path, "rb") as pcm_file:
            pcm_data = pcm_file.read()

        with wave.open("audio.wav", "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(16000)
            wav_file.writeframes(pcm_data)

        r = sr.Recognizer()

        with sr.AudioFile("audio.wav") as audio_file:
            audio_data = r.record(audio_file)
            text = r.recognize_google(audio_data, language="en-US")
            text = text + '\n'
        print("User: {}".format(text))
        return text
    except Exception as e:
        print("Error in recognize_speech_from_audio: {}".format(e))

if __name__ == "__main__":
    rospy.init_node("audio_chatgpt")
    audio_pub = rospy.Publisher("audio", String, queue_size=10)

    # Replace with the path to your audio file
    audio_file_path = "/home/audio/audio.pcm"

    while not rospy.is_shutdown():
        rospy.loginfo("Transcribing audio file...")
        transcribed_text = transcribe_audio_file(audio_file_path)
        rospy.loginfo("Transcribed text: %s", transcribed_text)
        audio_pub.publish(transcribed_text)
        rospy.sleep(10)
