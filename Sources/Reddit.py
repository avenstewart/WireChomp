import configparser
# import praw
import json
from time import sleep
from requests import Session, get

class RedditChomper:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('resources/sourceconfig.ini')
        self.reddit_config = config['REDDIT']

        # PRAW initialization code, not currently used

        # self.session = Session()
        # self.session.verify = self.reddit_config['certfile_path']
        # self.reddit = praw.Reddit(
        #    client_id=self.reddit_config['client_id'],
        #    client_secret=self.reddit_config['client_secret'],
        #    password=self.reddit_config['password'],
        #    requestor_kwargs={"session": self.session},
        #    user_agent=self.reddit_config['user_agent'],
        #    username=self.reddit_config['username']
        # )

    # get a list of all (up tp max_articles) article objects -
    # returned in a 24 hours window before supplied datetime

    def get_posts_before_datetime(self, unix_timestamp, lookback_hours, comment_thresh, max_results):
        print("Querying Reddit API for bulk posts.")
        results = []
        elapsed_time = 3600*lookback_hours
        after_timestamp = unix_timestamp - elapsed_time
        sub_list = json.loads(self.reddit_config['subreddit_list'])
        blacklist_hosts = json.loads(self.reddit_config['blacklist_domains'])
        blacklist_suffix = json.loads(self.reddit_config['blacklist_suffix'])

        for sub in sub_list:
            print("Ingesting posts from subreddit: "+sub)
            pushshift_url = (
                "https://api.pushshift.io/reddit/search/submission/?" +
                "subreddit=" + sub +
                "&after=" + str(after_timestamp) +
                "&before=" + str(unix_timestamp) +
                "&num_comments=>" + str(comment_thresh) +
                "&size=" + str(max_results) +
                "&is_video=false" +
                "&fields=domain,url,title,created_utc"
            )
            bulk_articles_json = get(pushshift_url).json()

            # PRAW code, not currently used
            # subreddit = self.reddit.subreddit(sub)

            for post_obj in bulk_articles_json['data']:
                if (not any(host in post_obj['domain'] for host in blacklist_hosts)) and \
                        (not any(post_obj['url'].endswith(ext) for ext in blacklist_suffix)):
                    results.append(post_obj)

            sleep(float(self.reddit_config['request_delay']))
        print("Query complete.")
        return results

    # method currently broken due to inaaccurate API scores
    # @staticmethod
    # def filter_by_score(posts_json, score_thresh):
    #     results = []
    #     for post in posts_json:
    #         if post['score'] >= score_thresh:
    #             results.append(post)
    #     return results

    @staticmethod
    def filter_by_keywords(posts_json, keywords=list):
        results = []
        for post in posts_json:
            # TODO figure out why this is throwing an odd non-iterable error for List
            # noinspection PyTypeChecker
            if all(word in post['title'] for word in keywords):
                results.append(post)
        return results

    @staticmethod
    def filter_by_hostname(posts_json, exclusive=bool, hostnames=list):
        results = []
        for post in posts_json:
            # TODO figure out why this is throwing an odd non-iterable error for List
            # noinspection PyTypeChecker
            if any(hostname in post['domain'] for hostname in hostnames):
                results.append(post)
        return results