from yt_dlp import YoutubeDL
from geminiServices import GeminiService
import os
import json
from tqdm import tqdm as bar

class YtSearch:
    def __init__(self, user_id: str):
        self.ydl_options = {
            'format': 'bestaudio/best',
            'noplaylist': False,
            'quiet': True,
            'no_warnings': True,
            'simulate': False,
            'extract_flat': True
        }
        self.USER_ID: str = user_id

    def queries(self):
        """
        Extract all search queries with hierarchical metadata.

        Args:
            course_data (dict): Course structure containing topics, subtopics, and queries

        Returns:
            list: List of dictionaries containing query metadata
        """
        queries = []

        with open(f"./data/{self.USER_ID}/syllabus.json", "r") as f:
            course_data = json.load(f)

        for i, topic in enumerate(course_data["topics"]):
            for j, subtopic in enumerate(topic["subtopics"]):
                for k, query in enumerate(subtopic["search_queries"]):
                    queries.append({
                    "topic_index": i,
                    "topic_title": topic["title"],
                    "subtopic_index": j,
                    "subtopic_title": subtopic["title"],
                    "query_index": k,
                    "query": query,
                    "path": f"topics[{i}].subtopics[{j}].search_queries[{k}]"
                })

        return queries

    def search(self, query, max_results=5):
        """
            Searches YouTube using yt-dlp and returns video metadata.

        Args:
            query (str): The search query.
            max_results (int): The maximum number of results to return.

        Returns:
            list: A list of dictionaries, each containing metadata for a video.
        """
        search_query =  f"ytsearch{max_results}:{query}"
        
        results = []
        try:
            with YoutubeDL(self.ydl_options) as ydl:
                info_dict = ydl.extract_info(search_query, download=False)
                    
                if 'entries' in info_dict:
                    results = info_dict['entries']
                
        except Exception as e:
            print(f"An error occurred: {e}")

        return results

    def run(self):
        queries = self.queries()
        for query in bar(queries, total=len(queries)):
            results = self.search(query["query"])
            print(results)
            info = {}
            for i in results:
                info[i["id"]] = {
                    "title": i["title"],
                    "url": i["url"],
                    "description": i["description"],
                    "duration": i["duration"],
                    "channel": i["channel"],
                    "channel_url": i["channel_url"],
                    "uploader": i["uploader"],
                    "uploader_url": i["uploader_url"],
                    "view_count": i["view_count"]
                }

            # store the info dictionary in a json file
            os.makedirs(f"./data/{self.USER_ID}", exist_ok=True)
            with open(f"./data/{self.USER_ID}/{query['topic_title'].replace('/', '_')}.json", "w") as f:
                json.dump(info, f)
        return f"./data/{self.USER_ID}"

if __name__ == "__main__":
    user_goal_context: str = input("Enter the user goal context: ")
    gemini_service = GeminiService(user_goal_context)
    gemini_service.run()
    user_id = gemini_service.user_id()
    yt_search = YtSearch(user_id)
    yt_search.run()
