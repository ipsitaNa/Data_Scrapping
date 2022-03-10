from YT_comments import YTstats

API_key = "AIzaSyCpM3ha1whS3kDiFURq8dG9eSQmFn61Ejs"
Channel_id = "UCCgLoMYIyP0U56dEhEL1wXQ"

yt = YTstats(API_key, Channel_id)
#yt.get_channel_stats()
#yt.get_channel_video_data()
yt.get_comments_deetails()
#yt.dump()
