import googleapiclient.discovery
import pandas as pd

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyATKUIZDk1xKyZ5Es3fYXKAdWY8z-y3Ilk"

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

def makeComments(video_id, maxPages):

    commentList = [] 
    next_page_token = None
    curPage = 1

    while curPage <= maxPages:

        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
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

video_id = "VGkmXzpTyfY"
maxPages = 100
comments = makeComments(video_id, maxPages)

        
df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])
df_sorted = df.sort_values(by='like_count', ascending=False)

print(df.head(100))