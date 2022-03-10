
from YouTubeStats import YTstats
import json
import csv

def create_csv_file():

    with open("chloe_ting.json")as file:
        data = json.load(file)
    
    video_data = data['UCCgLoMYIyP0U56dEhEL1wXQ']['video_data']
        
    f = open('video_stats.csv', 'w')
    keys = video_data.keys()
    
    f.write('publishedAt,title,viewCount,likeCount,commentCount,duration \n')
    for key in keys:
        value=video_data[key]
        #print(value)
        try:
            #publishedAt = value['publishedAt'].split('T')
            title = value['title'].replace(",","|")
            f.write(value['publishedAt']+','+title+','+value['viewCount']+','+value['likeCount']
            +','+value['commentCount']+','+value['duration']+'\n')
            
        except Exception as E: 
            print(E)

    
    f.close()
  


if __name__ == "__main__":
    create_csv_file()