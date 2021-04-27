import os

import pandas as pd
from pyyoutube import Api

PLAYLIST_ID = "PLvHyFbz_PpaZ7833xPxXXPgSi50phCH-P"

api = Api(api_key=os.environ["GOOGLE_API_KEY"])


def fetch_youtube_data():
    video_list = []
    playlist = api.get_playlist_items(playlist_id=PLAYLIST_ID)
    next_page = playlist.nextPageToken
    video_list.extend(playlist.items)
    while next_page:
        playlist = api.get_playlist_items(playlist_id=PLAYLIST_ID, page_token=next_page)
        next_page = playlist.nextPageToken
        video_list.extend(playlist.items)

    dates = []
    titles = []
    views = []
    for video in video_list:
        videos = api.get_video_by_id(video_id=video.contentDetails.videoId).items
        if videos:
            video = videos[0]
            dates.append(video.snippet.publishedAt)
            titles.append(video.snippet.title)
            views.append(int(video.statistics.viewCount))

    dataframe = pd.DataFrame()
    dataframe["date"] = pd.to_datetime(dates)
    dataframe["title"] = titles
    dataframe["views"] = views
    return dataframe.set_index("date")
