import os
import json
from uuid import UUID


class VideoIds:
    def __init__(self, directory: str="",):
        self.directories = os.listdir("./data")
        self.directory = directory
    
    def validate_uuid(self, uuid_string):
        try:
            UUID(str(uuid_string))
            return True
        except ValueError:
            return False

    def video_ids(self):
        video_ids = []
        if self.directory != "":
            files = os.listdir(f"{self.directory}")
            for file in files:
                if file.endswith(".json") and file != "syllabus.json":
                    with open(f"{self.directory}/{file}", "r") as f:
                        data = json.load(f)
                        video_ids.append(list(data.keys()))
            return video_ids
        else:
            for directory in self.directories:
                if self.validate_uuid(directory):
                    files = os.listdir(f"./data/{directory}")
                    for file in files:
                        if file.endswith(".json") and file != "syllabus.json":
                            with open(f"./data/{directory}/{file}", "r") as f:
                                data = json.load(f)
                                video_ids.append(list(data.keys()))
        return video_ids

    def ids(self):
        video_ids = self.video_ids()
        return [item for sublist in video_ids for item in sublist]   
        
if __name__ == "__main__":
    VideoIds = VideoIds()
    print(VideoIds.ids())
    