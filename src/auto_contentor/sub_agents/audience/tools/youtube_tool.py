"""
YouTube Data API Tool for Audience Research Agent
Searches videos and extracts comments for buyer persona analysis
"""

import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from typing import List, Dict, Any


class YouTubeDataTool:
    """YouTube Data API integration for audience research"""

    def __init__(self):
        self.api_key = os.getenv('YOUTUBE_API_KEY')
        if not self.api_key:
            raise ValueError("YOUTUBE_API_KEY environment variable is required. Please set it in your .env file.")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.max_comments = 20
        self.max_videos = 5

    def search_videos(self, query: str) -> List[Dict[str, Any]]:
        """Search for videos related to the query"""
        try:
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=self.max_videos,
                type='video',
                order='relevance'
            ).execute()

            videos = []
            for item in search_response['items']:
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'channel': item['snippet']['channelTitle'],
                    'description': item['snippet']['description'][:200],  # First 200 chars
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_data)

            return videos

        except HttpError as e:
            print(f"YouTube API error: {e}")
            return []

    def get_video_comments(self, video_id: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Get comments from a specific video"""
        try:
            comments_response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=max_results,
                order='relevance'
            ).execute()

            comments = []
            for item in comments_response['items']:
                comment_data = {
                    'text': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                    'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                    'likes': item['snippet']['topLevelComment']['snippet']['likeCount'],
                    'published_at': item['snippet']['topLevelComment']['snippet']['publishedAt']
                }
                comments.append(comment_data)

            return comments

        except HttpError as e:
            print(f"Error getting comments for video {video_id}: {e}")
            return []

    def collect_audience_data(self, query: str) -> Dict[str, Any]:
        """Main function to collect audience data from YouTube"""
        print(f"🔍 Searching YouTube for: '{query}'")

        # Step 1: Search for relevant videos
        videos = self.search_videos(query)
        if not videos:
            return {"error": "No videos found for the query"}

        print(f"📹 Found {len(videos)} relevant videos")

        # Step 2: Collect comments from videos
        all_comments = []
        comments_per_video = max(1, self.max_comments // len(videos))

        for video in videos:
            video_comments = self.get_video_comments(
                video['video_id'],
                max_results=comments_per_video
            )

            # Add video context to comments
            for comment in video_comments:
                comment['video_title'] = video['title']
                comment['video_channel'] = video['channel']

            all_comments.extend(video_comments)

            # Stop if we have enough comments
            if len(all_comments) >= self.max_comments:
                break

        # Limit to max_comments
        all_comments = all_comments[:self.max_comments]

        print(f"💬 Collected {len(all_comments)} comments for analysis")

        # Step 3: Structure the data for analysis
        audience_data = {
            "query": query,
            "videos_analyzed": len(videos),
            "total_comments": len(all_comments),
            "videos": videos,
            "comments": all_comments,
            "summary": {
                "top_channels": list(set([v['channel'] for v in videos])),
                "comment_engagement": sum([c['likes'] for c in all_comments]),
                "date_range": {
                    "oldest": min([c['published_at'] for c in all_comments]) if all_comments else None,
                    "newest": max([c['published_at'] for c in all_comments]) if all_comments else None
                }
            }
        }

        return audience_data


# Create the tool function for ADK agent
def youtube_search_tool(query: str) -> str:
    """
    YouTube search tool for ADK agent
    Searches YouTube videos and extracts comments for audience analysis

    Args:
        query: Search query (e.g., "Create a topic about AI Agent")

    Returns:
        JSON string with structured audience data from YouTube
    """
    tool = YouTubeDataTool()
    data = tool.collect_audience_data(query)

    # Return as JSON string for the agent to process
    return json.dumps(data, indent=2, ensure_ascii=False)


# Test function
def test_youtube_tool():
    """Test the YouTube tool with sample query"""
    result = youtube_search_tool("Create a topic about AI Agent")
    print("🧪 Test Result:")
    print(result)
    return result


if __name__ == "__main__":
    test_youtube_tool()
