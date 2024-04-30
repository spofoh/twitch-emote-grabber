import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_emotes(broadcaster_id, token, client_id):
    url = "https://api.twitch.tv/helix/chat/emotes"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    params = {
        "broadcaster_id": broadcaster_id
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_badges(broadcaster_id, token, client_id):
    url = "https://api.twitch.tv/helix/chat/badges"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }
    params = {
        "broadcaster_id": broadcaster_id
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def download_emote(emote, folder):
    emote_id = emote['id']
    emote_name = emote['name']
    emote_url = emote['images']['url_4x']
    if 'animated' in emote['format']:
        parts = emote_url.rsplit('static', 1)
        emote_url = 'animated'.join(parts)
        file_extension = '.gif'
    else:
        file_extension = '.png'
    if not os.path.exists(f"{folder}/{emote_name}{file_extension}"):
        response = requests.get(emote_url)
        with open(f"{folder}/{emote_name}{file_extension}", 'wb') as f:
            f.write(response.content)
        print(f"+ {emote_name}{file_extension}")

def download_badge(badge, folder):
    badge_id = int(badge['id'])
    badge_name = badge['title']
    badge_url = badge['image_url_4x']
    file_extension = '.png'
    if not os.path.exists(f"{folder}/{badge_name}{file_extension}"):
        response = requests.get(badge_url)
        with open(f"{folder}/{badge_name}{file_extension}", 'wb') as f:
            f.write(response.content)
        print(f"+ {badge_name}{file_extension}")

def main():
    broadcaster_id = os.getenv("TWITCH_BROADCASTER_ID")
    token = os.getenv("TWITCH_TOKEN")
    client_id = os.getenv("TWITCH_CLIENT_ID")
    base_folder = "Emotes"
    emotes = get_emotes(broadcaster_id, token, client_id)
    for emote in emotes['data']:
        if emote['emote_type'] == 'subscriptions':
            if int(emote['tier']) < 2000:
                folder = os.path.join(base_folder, 'Emotes', 'T1 Emotes')
            elif int(emote['tier']) < 3000:
                folder = os.path.join(base_folder, 'Emotes', 'T2 Emotes')
            else:
                folder = os.path.join(base_folder, 'Emotes', 'T3 Emotes')
            os.makedirs(folder, exist_ok=True)
            download_emote(emote, folder)
        elif emote['emote_type'] == 'bitstier':
            folder = os.path.join(base_folder, 'Emotes', 'Bits Emotes')
            os.makedirs(folder, exist_ok=True)
            download_emote(emote, folder)
        elif emote['emote_type'] == 'follower':
            folder = os.path.join(base_folder, 'Emotes', 'Follower Emotes')
            os.makedirs(folder, exist_ok=True)
            download_emote(emote, folder)
    badges = get_badges(broadcaster_id, token, client_id)
    for badge in badges['data']:
        if badge['set_id'] == 'subscriber':
            for version in badge['versions']:
                if int(version['id']) < 2000:
                    folder = os.path.join(base_folder, 'Sub Badges', 'T1')
                elif int(version['id']) < 3000:
                    folder = os.path.join(base_folder, 'Sub Badges', 'T2')
                else:
                    folder = os.path.join(base_folder, 'Sub Badges', 'T3')
                os.makedirs(folder, exist_ok=True)
                download_badge(version, folder)
        elif badge['set_id'] == 'bits':
            folder = os.path.join(base_folder, 'Bits Badges')
            os.makedirs(folder, exist_ok=True)
            for version in badge['versions']:
                download_badge(version, folder)

if __name__ == "__main__":
    main()
