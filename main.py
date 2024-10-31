from __future__ import unicode_literals
import speech_recognition as sr
import base64
import pyaudio
import wave
import requests
import json


def sendShazamApiReq(payload):

	url = "https://shazam.p.rapidapi.com/songs/detect"

	headers = {
		"content-type": "text/plain",
		"X-RapidAPI-Key": "9080104f94msh25a59c6b453f961p146faejsn108abd8993e3",
		"X-RapidAPI-Host": "shazam.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	content = response.json()

	print("\n", response.text ,"\n LOOK BELOW\n", )
	print(type(content))

	print(content)

	with open("filename.json", "w") as write_file:
		json.dump(content, write_file, indent=2)
	
	print("\n\n--------------------------------------------------------\n===============================")
	print(content["track"]["title"])
	



'''
getting audio from the mic input and then making it mono (channels(1) = mono)
'''
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1 
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT, channels=CHANNELS, rate = RATE, input= True, frames_per_buffer=RATE)
print("starting recording...")

frames = []
seconds = 5

for i in range(0, int(RATE / CHUNK * seconds)):
	data = stream.read(CHUNK)
	frames.append(data)

print("recording stopped.")
stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("monoFRaw.raw", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b"".join(frames))
wf.close()



'''encoding string to base 64 string'''
encodeString = base64.b64encode(open("monoFRaw.raw", "rb").read())
payload = encodeString #print type of encode string and see what it was and then regret on why your other file wasnt working and understand
# print(type(payload)) #prints bytes

print(sendShazamApiReq(payload=payload))
