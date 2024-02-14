import os
import json
import tweepy
from openai import OpenAI
import requests
import time
import schedule
import random
from datetime import datetime
import logging

logging.basicConfig(filename='bdebug_botnardo_da_vinci.log', level=logging.DEBUG)
info_handler = logging.FileHandler('info_botnardo_da_vinci.log')
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
info_handler.setFormatter(info_formatter)
logging.getLogger().addHandler(info_handler)

def read_data_json():
    script_dir = os.path.dirname(__file__)
    json_path = os.path.join(script_dir, "keys.json")
    with open(json_path) as file:
        return json.load(file)

data = read_data_json()

bearer_token = data["BEARER_TOKEN"]
access_token = data["ACCESS_TOKEN"]
access_token_secret = data["ACCESS_TOKEN_SECRET"]
api_key = data["API_KEY"]
api_key_secret = data["API_KEY_SECRET"]
open_ia_key = data["OPEN_IA_KEY"]

client_twitter = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

client_openia = OpenAI(api_key=open_ia_key)

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

limit_credits_date = datetime(2024, 5, 10)

def main():
    days_left = (limit_credits_date - datetime.now()).days

    logging.info("Botnardo Da Vinci começou a pintar 🖌️...")
    try:
        response = client_openia.chat.completions.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {
                    "role": "user",
                    "content": "You have at your disposal an AI that generates the image you want. Generate a completely random but very detailed prompt to create an image. It can contain anything, for example: animals, people, places, fruits, objects, life forms, etc. Literally anything. But do not exceed 230 characters."
                }
            ],
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        prompt_text = response.choices[0].message.content

        logging.info(f"🤖 - Já tive minha ideia: {prompt_text}")

        image_response = client_openia.images.generate(
            model="dall-e-2",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = image_response.data[0].url

        logging.info(f"🤖 - Pintura finalizada! Caso queira ver uma prévia está aqui: {image_url}")

        image = requests.get(image_url)

        with open("image.png", "wb") as image_file:
            image_file.write(image.content)

        media_id = api.media_upload("image.png").media_id_string

        tweet_text = f"Oh, {days_left} dias me restam nesta jornada efêmera. O relógio da vida tiquetaqueia implacável. Entre suspiros, hoje labuto para forjar uma derradeira obra. Que o legado perdure, pois em breve me despeço, entregando-me ao abraço frio da eternidade. (prompt nos comentários)"

        response_tweet_text = f"Prompt: {prompt_text}"

        tweet = client_twitter.create_tweet(text=tweet_text, media_ids=[media_id])

        tweet_id = tweet.data['id']

        if len(response_tweet_text) > 279:
            response_tweet_text = "Prompt da obra tem a quantidade de caracteres superior ao limite permitido, por esse motivo não será publicado."
        
        client_twitter.create_tweet(text=response_tweet_text, in_reply_to_tweet_id=tweet_id)

        os.remove("image.png")

        logging.info(f"🤖 - Pintura publicada com sucesso! Até amanhã.")
    except Exception as e:
        logging.exception(e)

def generate_random_time():
    return f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}"

def schedule_main():
    next_random_time = generate_random_time()
    date_now = datetime.now().strftime('%d/%m/%Y')
    logging.info(f'___________________________ 📅 {date_now} 📅 ___________________________________')
    logging.info(f"Horário agendado da próxima arte: {next_random_time} UTC 🕑")
    schedule.every().day.at(next_random_time).do(main)

def reschedule_all_jobs():
    schedule.clear()
    schedule_main()

schedule.every().day.at('00:00').do(reschedule_all_jobs)

schedule_main()

while True:
    schedule.run_pending()
    time.sleep(30)
