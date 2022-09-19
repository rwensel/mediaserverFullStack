import pandas as pd
from mrmemes import Imaging, Database

df = pd.DataFrame()
for post in Database(score=35).get_reddit_posts():
    df = df.append({
        'guid': post['guid'],
        'ocr': Imaging(img=post['url']).meme_ocr()
    }, ignore_index=True)

Database(dataframe=df, table='ocr').write_to_sql()
