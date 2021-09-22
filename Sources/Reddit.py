import configparser
import praw
import json
from time import sleep
from requests import Session, get

class RedditChomper:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('resources/sourceconfig.ini')
        self.reddit_config = config['REDDIT']

        self.session = Session()
        self.session.verify = self.reddit_config['certfile_path']
        self.reddit = praw.Reddit(
            client_id=self.reddit_config['client_id'],
            client_secret=self.reddit_config['client_secret'],
            password=self.reddit_config['password'],
            requestor_kwargs={"session": self.session},
            user_agent=self.reddit_config['user_agent'],
            username=self.reddit_config['username']
        )

    # get a list of all (up tp max_articles) article objects -
    # returned in a 24 hours window before supplied datetime
    def get_posts_before_datetime(self, date_millis, lookback_hours, max_results):
        results = []
        elapsed_time = 3600000*lookback_hours
        after_timestamp = date_millis - elapsed_time
        subslist = self.reddit_config['subreddit_list']
        sub_urls = json.loads(subslist)

        for sub in sub_urls:
            pushshift_url = (
                "https://api.pushshift.io/reddit/search/submission?subreddit=%s&after=%d&before=%d&size=%d"
                % (sub, after_timestamp, date_millis, max_results)
            )
            bulk_articles_json = get(pushshift_url).json()
            subreddit = self.reddit.subreddit(sub)
            for post_obj in bulk_articles_json['data']:
                results.append(post_obj)
            sleep(int(self.reddit_config['request_delay']))
        return results

    @staticmethod
    def filter_by_score(posts_json, score_thresh):
        results = []
        for post in posts_json:
            if post['score'] >= score_thresh:
                results.append(post)
        return results

    @staticmethod
    def filter_by_keywords(posts_json, keywords=list):
        results = []
        for post in posts_json:
            # noinspection PyTypeChecker
            if all(word in post['title'] for word in keywords):
                results.append(post)
        return results

    @staticmethod
    def filter_by_news_source(posts_json, exclusive=bool, hostnames=list):
        results = []
        for post in posts_json:
            # noinspection PyTypeChecker
            if any(hostname in post['domain'] for hostname in hostnames):
                results.append(post)
        return results


