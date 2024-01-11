import googleapiclient.discovery
import pandas as pd
from textblob import TextBlob
from dataclasses import dataclass

def determineScore(text: str):

    sentiment = TextBlob(text).sentiment.polarity

    return sentiment


def makeComments(video_id, maxPages):

    commentList = [] 
    next_page_token = None
    curPage = 1

    while curPage <= maxPages:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=20,
            pageToken=next_page_token,
            order="relevance"
        )
        
        response = request.execute()

        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']
            commentList.append([
                comment['authorDisplayName'],
                comment['publishedAt'],
                comment['updatedAt'],
                comment['likeCount'],
                comment['textDisplay']
            ])

        next_page_token = response.get('nextPageToken')
        curPage += 1

        if not next_page_token or curPage > maxPages:
            break
    
    return commentList


api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyATKUIZDk1xKyZ5Es3fYXKAdWY8z-y3Ilk"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

video_id = "XqZsoesa55w"
maxPages = 100
comments = makeComments(video_id, maxPages)


df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])


numComments = 200

first_row = (df.loc[:numComments, 'text']).tolist()

totalScore = 0

for i in first_row:
    totalScore += determineScore(i)

print(totalScore/numComments)
