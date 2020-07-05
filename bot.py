from datetime import datetime, timedelta
from auth import client_id, client_secret, token, requests, json
from edit import video_length_seconds, get_total_length, change_fps

# if __name__ == '__main__'

def get_clips(daysdiff, game_name):
    d = datetime.utcnow() - timedelta(days=daysdiff)
    started_at = d.isoformat("T") + "Z"
    r = requests.get(api_endpoint + f'?game_id={categories[game_name]}&first=100&started_at={started_at}',
                     headers=headers)
    return r.json()["data"]

def process_clips(clips, language):
    for clip in clips:
        vid_id = clip["thumbnail_url"].split("-preview")[0] + ".mp4"
        clip["video_url"] = vid_id
        for stat in unnecessary_stats:
            del clip[stat]

    processed_clips = [clip for clip in clips if language in clip["language"]]
    return processed_clips

def downloadfile(name, url, s):
    r=s.get(url)
    f=open(f'videos/{name}.mp4','wb');
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
    f.close()

def sort_clips_chronologically(arg):
    arg.sort(key=lambda k : k["created_at"])


api_endpoint = "https://api.twitch.tv/helix/clips"
headers = {'Client-ID': client_id,
           "Authorization": "Bearer {}".format(token)}

categories = {
    "League of Legends": "21779",
    "Just Chatting": "509658",
    "Fortnite": "33214",
    "COD MW": "512710",
    "Dota 2": "29595",
    "GTA V": "32982",
    "Minecraft": "27471",
    "CSGO": "32399",
    "Hyper Space": "518306",
    "Valorant": "516575",
    "WoW": "18122",
    "Tarkov": "491931",
    "Apex Legends": "511224",
    "Tarkov": "491931"
}

shoutouts = []
unnecessary_stats = ["embed_url", "creator_id", "creator_name", "game_id",
                     "view_count", "thumbnail_url"]

clips = get_clips(2, "Fortnite")
processed_clips = process_clips(clips, "en")
#sort_clips_chronologically(processed_clips)

print(json.dumps(processed_clips, indent = 4))

length = get_total_length()
s = requests.Session()


for i, clip in enumerate(processed_clips):
    if length >= 601:
        break
    if(clip["broadcaster_name"] not in shoutouts):
        shoutouts.append(clip["broadcaster_name"].lower())
    downloadfile(i, clip["video_url"], s)
    length = get_total_length()
    print(length)

print(shoutouts)
#sleep(20)
change_fps()
