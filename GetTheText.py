import glob
import os
import random
import speech_recognition as sr


#Configuration Variables
RecordedVoices = True
access_google_api = False
use_default_text = True
default_text = 'Hi there'

order_queries = [
                   "Hi, Can you order a black bath tub for Customer3?",
                   "Hey, I would like to order 5 blue kitchen sinks for Customer1.",
                   "Hello, place an order for 10 light bulbs and one sofa for Customer2.",
                   "Hi, Two kitchen tables need to be ordered for Customer4. ",
                   "Hey, Customer5 requires 5 taps. Please order them."
               ]

status_queries = [
                   "Hello, What is the status of the order: 123456 ?",
                   "Hello, Tell me the status of the order: 361251 ?",
                   "Could you please give me the status of the order with order number:125623 ?",
                   "Hello, status of the order please? Order number : 361251. ",
                   "Hello, Tell me the status of the order with order number: 124564."
                ]

delivery_query = [
                   "Greetings, When can I expect the delivery of the my order?",
                   "Ola, When does the order arrive ?",
                   "Ola, When is order number 124564 reach ?",
               ]

rate_query = [
                   "Hello, What is the best price I can get for the sanibel 2000 Eckdusche for Customer2?",
                   "Hi, Tell me the best price for sanibel 2000 Eckdusche for Customer1?",
                   "Hello, At what price can you sell the sanibel 2000 Eckdusche to Customer5?",
                   "Yo, Customer2's Best price for sanibel 2000 Eckdusche ?",
                   "Hello, Please give me the best price for the sanibel 2000 Eckdusche for Customer5 ?",
           ]

list_of_queries = [order_queries, status_queries, delivery_query, rate_query]
all_queries = []

for i in range(len(list_of_queries)):
    all_queries = all_queries + list_of_queries[i]
#all_queries = [all_queries + list_of_queries[x] for x in range(list_of_queries)]
print(len(all_queries))
if __name__ == "__main__":

    print("This is GC Group. How can I help you?")

    os.chdir("/home/senthil/GC_Group/AudioExample")
    list_of_audio_example = []
    for file in glob.glob("*.wav"):
        list_of_audio_example.append(file)

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    if not access_google_api:
        if use_default_text:
            text = default_text
        else:
            text = random.choice(all_queries)

    else:
        if RecordedVoices:
            audio_to_convert = random.choice(list_of_audio_example)
            print("using the audio file {}".format(audio_to_convert))
            audio_to_convert = sr.AudioFile(audio_to_convert)
            with audio_to_convert as source:
                audio = recognizer.record(source)

        else:
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

        text = recognizer.recognize_google(audio)


    print(text)
