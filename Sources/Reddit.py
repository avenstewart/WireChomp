import configparser
import praw
from requests import Session

class RedditChomper:

    config = configparser.ConfigParser()
    config.read('resources/sourceconfig.ini')
    reddit_config = config['REDDIT']

    def init_session(self):

        session = Session()
        session.verify = self.reddit_config['certfile_path']
        return praw.Reddit(
            client_id="",
            client_secret="",
            password="",
            requestor_kwargs={"session": session},
            user_agent="",
            username=""
        )

    @staticmethod
    def get_before_date(datetime, max_articles):
        # get a list of all (up tp max_articles) article objects -
        # returned in a 24 hours window before supplied datetime
        config = configparser.ConfigParser()
        config.read('sourceconfig.ini')
        sub_urls = config['REDDIT']['subreddit_list']

        for sub in sub_urls:
            subreddit =  praw.reddit.Subreddit(sub)
            for submission in praw

    @staticmethod
    def get_raw_links_from_sub(sub, date, limit):
        sub_url = "https://reddit.com/r/%s" % sub


    def map_article_to_obj(self, raw):
        # map each articles datetime, title, and primary content to an ArticleMap object
        # assign a popularity weight to the article based on upvotes

    def content_from_raw(self):
        # retrieve the raw article and determine the type of source
        # grab the main content with the corresponding extraction method for that specific news source

