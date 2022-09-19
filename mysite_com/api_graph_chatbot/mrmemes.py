import cv2
import numpy as np
import os
import pandas as pd
import requests
import time
from dotenv import load_dotenv
from pytesseract import pytesseract
from requests import auth, structures
from sqlalchemy import create_engine, Table, MetaData, select, and_, desc

load_dotenv('./home.env')
cs = os.getenv('SQL_CON')
eng = create_engine(cs, pool_size=20, max_overflow=0)

page_id = os.getenv('dev_page_id')
graph_api = os.getenv('graph_api')

header = structures.CaseInsensitiveDict()
header["Accept"] = "application/json"
header["User-Agent"] = 'Mr Meme || py_bot'


class Database:

    def __init__(self, command_type=None, account=None, table=None, dataframe=None, score=0):
        self.command_type = command_type
        self.account = account
        self.table = table
        self.dataframe = dataframe
        self.score = score

    def get_settings(self):
        with eng.connect() as con:
            meta_obj = MetaData(bind=eng)
            tb_cfg = Table("links", meta_obj, autoload=True)
            stmt = select(tb_cfg.columns.link, tb_cfg.columns.header,
                          tb_cfg.columns.data).where(tb_cfg.columns.name == self.command_type)
            r = con.execute(stmt).first()
            con.close()
            return r

    def get_auth(self):
        with eng.connect() as con:
            meta = MetaData(bind=eng)
            tb_auth = Table("pyAuth", meta, autoload=True)
            stmt = select([tb_auth]).where(tb_auth.columns.identifier == self.account)
            r = con.execute(stmt).first()
            con.close()
            return r

    def write_to_sql(self):
        self.dataframe.to_sql(
            self.table, eng.connect(), if_exists="append", index=False)

    def get_reddit_posts(self):
        with eng.connect() as con:
            meta = MetaData(bind=eng)
            tb_redd = Table("redd", meta, autoload=True)
            stmt = select([tb_redd]).where(
                and_(tb_redd.columns.over_18 == 0, tb_redd.columns.score >= self.score)).order_by(
                desc(tb_redd.columns.hash))
            r = con.execute(stmt).fetchall()
            con.close()
            return r


class Imaging:

    def __init__(self, img=None):

        self.img = img

    def meme_ocr(self):

        path_to_tesseract = os.getenv('TES')
        pytesseract.tesseract_cmd = path_to_tesseract

        resp = requests.get(self.img, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        grey = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        blur = cv2.GaussianBlur(grey, (3, 3), 0)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
        invert = 255 - opening
        text = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
        return text.replace('\n', '')

    def check_hash(self):

        img = self.img
        with eng.connect() as con:
            meta_obj = MetaData(bind=eng)
            repo = Table("redd", meta_obj, autoload=True)
            stmt = select(repo.columns.url).where(and_
                                                  (repo.columns.url == img))
            if con.execute(stmt).first() is None:
                _hash_code = Imaging(img=img).get_hash()
                stmt = select(repo.columns.hash).where(and_
                                                       (repo.columns.hash == _hash_code))
            if con.execute(stmt).first() is None:
                con.close()
                return _hash_code
            else:
                con.close()
                return None

    def get_hash(self):

        import hashlib
        import tempfile

        img = self.img
        req = requests.get(img).content
        tmp_file = tempfile.TemporaryFile(delete=False)
        fn = tmp_file.name
        tmp_file.write(req)
        hash_md5 = hashlib.md5()
        with open(tmp_file.name, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        tmp_file.close()
        os.remove(fn)
        return hash_md5.hexdigest()


class Reddit:

    def __init__(self, permalink=None, hash_code=None, score=0, post_id=None, guid=None):

        self.permalink = permalink
        self.hash = hash_code
        self.score = score
        self.post_id = post_id
        self.guid = guid

    @staticmethod
    def get_pat():

        (au, ap) = Database(account=os.getenv('rddt_app_id')).get_auth()
        (u, p) = Database(account=os.getenv('rddt_user')).get_auth()
        (link, _, post_data) = Database(command_type=os.getenv('token_rdt')).get_settings()
        data = structures.CaseInsensitiveDict()
        data["grant_type"] = "password"
        data["username"] = u
        data["password"] = p
        data["scope"] = post_data
        client_auth = auth.HTTPBasicAuth(au, ap)
        response = requests.post(link,
                                 auth=client_auth, data=data, headers=header)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            return response.status_code

    def get_repost(self):

        with eng.connect() as con:
            meta_obj = MetaData(bind=eng)
            repo = Table("redd", meta_obj, autoload=True)
            stmt = select(repo.columns.permalink).where(
                and_(repo.columns.permalink == self.permalink))
            r = con.execute(stmt).first()
            con.close()
            return r is not None

    @staticmethod
    def get_subs():

        (link, sub_header, post_data) = Database(command_type=os.getenv('subscribers_rdt')).get_settings()
        headers = structures.CaseInsensitiveDict()
        headers["Authorization"] = post_data.format(Reddit().get_pat())
        headers["User-Agent"] = sub_header
        with requests.Session() as sess:
            return sess.get(link, headers=headers).json()['data']['children']

    def get_posts(self):

        from uuid import uuid4
        import re

        pattern = re.compile('.*(?:imgur|redd.it).*(?:jpg|png)')
        df = pd.DataFrame()
        for sub in Reddit().get_subs():
            subreddit = sub['data']['display_name']
            (link, *_) = Database(command_type=os.getenv('posts_rdt')).get_settings()
            print(f'fetching sub: {subreddit}\n\r')
            for post in requests.get(link.format(subreddit)).json()['data']:
                permalink = post['permalink']
                img = post['url']
                if (
                        post['score'] >= self.score
                        and Reddit(permalink=permalink).get_repost() is False
                        and bool(pattern.search(img))
                        and requests.get(img).ok
                ):
                    hash_code = Imaging(img=img).check_hash()
                    if hash_code is not None:
                        u = uuid4()
                        df = df.append({
                            'guid': str(u),
                            'id': post['id'],
                            'author': post['author'],
                            'subreddit': subreddit,
                            'title': post['title'],
                            'url': img,
                            'permalink': permalink,
                            'full_link': post['full_link'],
                            'num_comments': post['num_comments'],
                            'over_18': post['over_18'],
                            'score': post['score'],
                            'date': post['created_utc'],
                            'hash': hash_code
                        }, ignore_index=True)
                        Reddit(post_id=post['id'], guid=str(u)).get_comments()
        Database(table='redd', dataframe=df).write_to_sql()

    def get_comments(self):

        df = pd.DataFrame()
        (pid, *_) = Database(command_type=os.getenv('comIds_rdt')).get_settings()
        (cid, *_) = Database(command_type=os.getenv('comms_rdt')).get_settings()
        for comm in requests.get(pid.format(self.post_id)).json()['data']:
            # print(requests.get(cid.format(comm)).json()['data'][0]['body'])
            df = df.append({
                'guid': self.guid,
                'comm_id': comm,
                'comment': requests.get(cid.format(comm)).json()['data'][0]['body'].replace('(', '').replace(')',
                                                                                                             '').replace(
                    '#', '')
            }, ignore_index=True)
        Database(dataframe=df, table='Comments').write_to_sql()


class Facebook:

    def __init__(self, post_id=None, message=None, url=None, payload=None, count=0):

        self.post_id = post_id
        self.title = message
        self.url = url
        self.payload = payload
        self.count = count

    @staticmethod
    def get_feed():

        api_call = f"{graph_api}/me"
        fb_data = structures.CaseInsensitiveDict()
        fb_data["fields"] = "feed.limit(100)"
        fb_data['access_token'] = os.getenv('dev_page_token')
        with requests.Session() as sess:
            return sess.get(api_call, headers=header, params=fb_data)

    def delete_post(self):

        api_call = f"{graph_api}/{self.post_id}"
        fb_data = structures.CaseInsensitiveDict()
        fb_data['access_token'] = os.getenv('dev_page_token')
        with requests.Session() as sess:
            return sess.delete(api_call, headers=header, params=fb_data)

    def update_post(self):

        api_call = f"{graph_api}/{self.post_id}"
        fb_data = structures.CaseInsensitiveDict()
        fb_data['access_token'] = os.getenv('dev_page_token')
        fb_data['message'] = self.title
        with requests.Session() as sess:
            return sess.post(api_call, headers=header, params=fb_data)

    def post_image(self):

        api_call = f"{graph_api}/{page_id}/photos"
        fb_data = structures.CaseInsensitiveDict()
        fb_data['access_token'] = os.getenv('dev_page_token')
        fb_data['url'] = self.url
        with requests.Session() as sess:
            return sess.post(api_call, headers=header, params=fb_data)

    @staticmethod
    def get_app_token():

        auth_url = os.getenv('auth_url')
        client_id = os.getenv('app_id')
        client_secret = os.getenv('app_secret')
        fb_data = structures.CaseInsensitiveDict()
        fb_data['grant_type'] = 'client_credentials'
        fb_data['client_id'] = client_id
        fb_data['client_secret'] = client_secret
        with requests.Session() as sess:
            return sess.get(auth_url, headers=header, params=fb_data)

    def post_multi_image(self):

        df_post = pd.DataFrame()
        df_update = pd.DataFrame()
        for i in range(self.count):
            ts = time.time()
            fb_post = Facebook(url=self.payload[i]['url']).post_image()
            if fb_post.status_code == 200:
                df_post = df_post.append({
                    'guid': self.payload[i]['guid'],
                    'post_id': fb_post.json()['post_id'],
                    'id': str(fb_post.json()['id']),
                    'status_code': fb_post.status_code,
                    'post_url': fb_post.url,
                    'JSON': fb_post.text,
                    'response_time': fb_post.elapsed.seconds,
                    'execution_time': ts
                }, ignore_index=True)
                message = f"""
                            \t\tReddit user - {self.payload[i]['author']} - says: {self.payload[i]['title']}\r\r\r\r
                            -- Reddit Info --\r\r
                            Link: {self.payload[i]['full_link']}
                            Number of comments: {self.payload[i]['num_comments']}
                            Score: {self.payload[i]['score']}
                            Subreddit: {self.payload[i]['subreddit']}
                            -- Technical info --\r\r
                            Bot GUID: {self.payload[i]['guid']}
                            Image MD5: {self.payload[i]['hash']}
                            Facebook Post ID: {fb_post.json()['id']}
                            """
                fb_update = Facebook(fb_post.json()['post_id'], message).update_post()
                if fb_update.ok:
                    df_update = df_update.append({
                        'guid': self.payload[i]['guid'],
                        'post_id': fb_post.json()['post_id'],
                        'id': str(fb_post.json()['id']),
                        'message': self.payload[i]['title'],
                        'status_code': fb_update.status_code,
                        'post_url': fb_update.url,
                        'JSON': fb_update.text,
                        'response_time': fb_update.elapsed.seconds,
                        'execution_time': ts
                    }, ignore_index=True)
                else:
                    df_update = df_update.append({
                        'guid': self.payload[i]['guid'],
                        'post_id': 'failed',
                        'id': 'failed',
                        'message': self.payload[i]['title'],
                        'status_code': fb_update.status_code,
                        'post_url': fb_update.url,
                        'JSON': fb_update.text,
                        'response_time': fb_update.elapsed.seconds,
                        'execution_time': ts
                    }, ignore_index=True)
            else:
                df_post = df_post.append({
                    'guid': self.payload[i]['guid'],
                    'post_id': 'failed',
                    'id': 'failed',
                    'status_code': fb_post.status_code,
                    'post_url': fb_post.url,
                    'JSON': fb_post.text,
                    'response_time': fb_post.elapsed.seconds,
                    'execution_time': ts
                }, ignore_index=True)
        Database(table='fb_post', dataframe=df_post).write_to_sql()
        Database(table='fb_update', dataframe=df_update).write_to_sql()
