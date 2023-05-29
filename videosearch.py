import requests

# Set up the YouTube Data API endpoint URL
api_url = "https://www.googleapis.com/youtube/v3/search"

searchkey = "improve counter attack"

# Set up the search query parameters
params = {
    "part": "id,snippet",
    "channelId": ["UCsH9CrSfzknNKKwS6wGCeQQ","UC5SQGzkWyQSW_fe-URgq7xw","UC9xRcqG8V6yNi6Hum92EoGg"],
    "q": searchkey,
    "type": "video",
    "maxResults": 10,
    "key": "AIzaSyDdlQBcR6HSwgIB7fL9ix-JgPqr7FtWWtA",
}

# Send the API request and retrieve the response
response = requests.get(api_url, params=params)

# Parse the response JSON and print the found videos
for item in response.json()["items"]:
    video_title = item["snippet"]["title"]
    thumbnail_url = item["snippet"]["thumbnails"]["high"]["url"]
    video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
    channel_name = item["snippet"]["channelTitle"]
    print(video_title,"\n",video_url,"\n",thumbnail_url,"\n",channel_name)