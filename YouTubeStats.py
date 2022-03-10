import requests
import json
from tqdm import tqdm


class YTstats:
    def __init__(self, api_key, channel_id):
        # passing API key and channel id and store it in the object var
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        # adding method to this class to get video_information, so add a video varaible that will later store data
        self.video_data = None

    # create a function, which will get  channel_statistics
    def get_channel_stats(self):
        # we need the url for the stats , lets create create url object
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)

        try:
            data = data["items"][0]["statistics"]
        except:

            data = None

        self.channel_statistics = data
        print(data)
        return data

    def get_channel_video_data(self):
        # part 1 - we will get all video ids
        # we will create a helper method for this _get_channel_videos
        channel_videos = self.get_channel_videos(limit=50)
        print(channel_videos)
        print(len(channel_videos))

        # part 2 -
        parts = ["snippet", "statistics", "contentDetails"]
        # we will check progress bar as this loop will take time more than a min , so importing tqdm
        # tqdm is a library in Python which is used for creating Progress Meters or Progress Bars
        # It gives Code Execution Time and Estimated Time for the code to complete which would help while working on huge datasets
        for video_id in tqdm(channel_videos):
            for part in parts:
              data = self.get_single_video_data(video_id, part)
              # We want to put the data in the channel video object we want to update data as per the video id
              #video_id is the key and the value will be given by update(data)
              channel_videos[video_id].update(data)

        # store this into the self.video_data
        self.video_data = channel_videos
        return channel_videos
              

    def get_single_video_data(self,video_id,part):
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data


    def get_channel_videos(self, limit=None):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet&order=date"
        print('1')
        # by default it will return the five latest result it will found  so we can add the limit parameter
        # need to check if limit is not none and we can check if it is valid integer , we can do that by ibuild isinstance()
        # The isinstance() function returns True if the specified object is of the specified type, otherwise False. e.g. x = isinstance(5, int)
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
            print(url)
        
        # we will call the vidoes_per_page and pass the url to that func
        videos, next_pg_tokn = self.get_channel_videos_per_page(url)
        

        idx = 0
        while next_pg_tokn is not None and idx < 5:
            next_url = url + "&pageToken=" + next_pg_tokn
            next_vid, next_pg_tokn = self.get_channel_videos_per_page(next_url)
            videos.update(next_vid)
            #print(next_pg_tokn)
            idx += 1

        #print(videos)
        return videos

    
    

    # we need to find all teh results per page till I dont find previousPageToken.
    def get_channel_videos_per_page(self, url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()  # an empty dictironary in the begiining
        # we will find the items key -> check for id -?> videoId
        if (
            "items" not in data
        ):  # return channle videos and alos the nextTokenPage number and if we have errror we will retrun NONE
            return channel_videos, None

        # if it is in data continue,
        item_data = data["items"]
        nextPageToken = data.get(
            "nextPageToken", None
        )  # pass the nextPageToken from the url data and place it in ger
        # lets itereate over items dat , we need kind- youtubeVideo
        for item in item_data:
            try:
                kind = item["id"]["kind"]
                if kind == "youtube#video":
                    video_id = item["id"]["videoId"]
                    channel_videos[video_id] = dict()
            except KeyError:
                print("Error")
        
        print(channel_videos)
        return channel_videos, nextPageToken

    


    def dump(self):
        if self.channel_statistics is None or self.video_data is None:
          print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
          return

        # lets get the channel name  and dump it to a file

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,
                              "video_data": self.video_data}}
        
        #print(self.video_data)                              
        Channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        
        """
        get method will find Title, if it wont then it will retun channel_id
        pop a random item and this will rteurn a tupple where the first item will be key and the seconf will be value, 
        we need value whcih has actual video data 
        """


        channel_title = Channel_title.replace(" ", "_").lower()
        file_name = Channel_title + ".json"
        filename = channel_title + '.json'
        
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)
        
        
        print('file dumped to', filename)
