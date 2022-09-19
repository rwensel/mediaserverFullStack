import datetime
import os
from dotenv import load_dotenv
from mrmemes import Facebook

load_dotenv('./home.env')

while len(Facebook().get_feed().json()['feed']['data']) > 1:
    date_time = datetime.datetime.now()
    feed = Facebook().get_feed()
    count = len(feed.json()['feed']['data'])

    if feed.ok and feed.status_code == int(200):
        fb_post = Facebook(url=os.getenv('purge')).post_image()
        if fb_post.ok and fb_post.status_code == int(200):
            fb_update = Facebook(post_id=fb_post.json()['post_id'],
                                 message=f'Automated message {date_time}: Incoming purge for a new test run. '
                                         f'Removing {count} post(s)').update_post()
            if fb_update.ok and fb_update.status_code == int(200):
                for post in feed.json()['feed']['data']:
                    Facebook(post_id=post.get('id')).delete_post()
