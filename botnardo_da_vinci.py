import os
import json
import tweepy
from openai import OpenAI
import requests
import time

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

try:

    response = client_openia.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {
                "role": "user",
                "content": "I'm with an image AI and I have no idea what to create. Generate a completely random prompt for her to create. It can contain anything, such as animals, famous people, cars, well-known places, fruits, objects, life forms, etc. Literally anything. But don't exceed 150 characters."
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    prompt_text = response.choices[0].message.content

    print(f"PROMPT AQUI: #{prompt_text}")
    
    image_response = client_openia.images.generate(
        model="dall-e-2",
        prompt=prompt_text,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = image_response.data[0].url

    print(f"IMAGE URL AQUI: #{image_url}")

    image = requests.get(image_url)
    
    with open("image.png", "wb") as image_file:
        image_file.write(image.content)

    media_id = api.media_upload("image.png").media_id_string

    tweet_text = f"30 dias me separam do meu derradeiro suspiro. Por tal motivo, nesta data, deixo ao mundo esta obra antes de me despedir. {prompt_text}"

    tweet = client_twitter.create_tweet(text=tweet_text, media_ids=[media_id])

    os.remove("image.png")

    print(tweet)
except Exception as e:
    print(e)