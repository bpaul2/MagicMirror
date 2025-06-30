import multiprocessing as mp
import yaml
from google import genai
from google.genai import types
import speech_recognition as sr

RULES_FILE = "rules.yml"

def magic_mirror(e_exit, rules, api_key):
    # Companion Initialization
    client = genai.Client(api_key=api_key)
    max_out_tokens = 100
    voice_name = "Rasalgethi"
    safety = [
        types.SafetySetting(
            category='HARM_CATEGORY_HARASSMENT',
            threshold='BLOCK_MEDIUM_AND_ABOVE',
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_HATE_SPEECH',
            threshold='BLOCK_MEDIUM_AND_ABOVE',
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_SEXUALLY_EXPLICIT',
            threshold='BLOCK_LOW_AND_ABOVE',
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_DANGEROUS_CONTENT',
            threshold='BLOCK_LOW_AND_ABOVE',
        ),
        types.SafetySetting(
            category='HARM_CATEGORY_CIVIC_INTEGRITY',
            threshold='BLOCK_MEDIUM_AND_ABOVE',
        )
    ]

    # Speech Recogniser Initilization
    r = sr.Recognizer()
    index = 0

    # Loop
    while not e_exit.is_set():
        with sr.Microphone(device_index=index) as source:
            r.adjust_for_ambient_noise(source)
            print("Recording Audio...\n")
            audio = r.listen(source=source)

        if (e_exit.is_set()):
            break
        print("Processing...\n")
        try:
            # script = r.recognize_faster_whisper(audio)
            script = r.recognize_whisper(audio)

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config=types.GenerateContentConfig(
                        system_instruction=rules,
                        max_output_tokens=max_out_tokens,
                        safety_settings=safety
                    ),
                contents=script
            )
            print(response.text)

        except sr.UnknownValueError:
            print("Did not understand")
        except sr.RequestError as e:
            print(e)

def main():

    with open(RULES_FILE) as stream:
        try:
            data = yaml.safe_load(stream)
            api_key = data['api_key']
            rules = data['rules']

            e_exit = mp.Event()
            p1 = mp.Process(target=magic_mirror, args=(e_exit,rules,api_key))

            p1.start()

            print("Program starting. Enter 'q' to quit.")
            while(True):
                key = input()
                if len(key) <= 1 and ord(key) == ord('q'):
                    print("Quitting...")
                    e_exit.set()
                    break

            p1.join()

        except yaml.YAMLError as exc:
            print(exc)
            exit

if __name__ == '__main__':
    main()