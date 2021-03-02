import os

import googleapiclient.discovery
import googleapiclient.errors

CHANNEL_ID = "UC5oWzIBclqteQvZg5WDjdKQ"


def fetch_youtube_data():
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=os.environ["GOOGLE_API_KEY"]
    )
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics", id=CHANNEL_ID
    )
    response = request.execute()

    name = response["items"][0]["snippet"]["description"]
    statistics = response["items"][0]["statistics"]

    return name, statistics
