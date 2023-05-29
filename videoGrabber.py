from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from urllib.request import urlopen
import json
import re

YTDataAPI = "AIzaSyDdlQBcR6HSwgIB7fL9ix-JgPqr7FtWWtA"
ServiceName = "youtube"
APIVersion = "v3"
channel_link = input()
channel_name = re.findall(r"youtube.com/@(\w+)", channel_link)



ChannelUsername = channel_name[0]

url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={ChannelUsername}&type=channel&key={YTDataAPI}"
response = urlopen(url)
data_json = json.loads(response.read())
chID = data_json['items'][0]['id']['channelId']
print(chID)


ChannelID = chID


# create a YouTube API client
youtube = build(ServiceName, APIVersion, developerKey=YTDataAPI)

try:
    # retrieve the channel's uploads playlist ID
    channel_response = youtube.channels().list(
        part="contentDetails",
        id=ChannelID
    ).execute()
    playlist_id = channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# retrieve all videos from the uploads playlist
    video_response = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50000
    ).execute()
# iterate through each video and extract the information
    for item in video_response["items"]:
        video_title = item["snippet"]["title"]
        if "shot" in video_title:
            video_url = f'https://www.youtube.com/watch?v={item["snippet"]["resourceId"]["videoId"]}'
            video_thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
            print(video_title, video_url, video_thumbnail)

except HttpError as error:
    print("An HTTP error occurred: %s" % error)
