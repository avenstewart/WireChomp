import unittest
from Parser import Parser
from Sources import Reddit

class RedditParsingTests(unittest.TestCase):

    def setUp(self):
        self.chomper = Reddit.RedditChomper()

    def testA(self):
        # get all posts from a date with a 24 hour lookback, limited to 50 articles per subreddit
        bulk_posts = self.chomper.get_posts_before_datetime(1632291231, 24, 1500)
        filtered_posts = self.chomper.filter_by_score(bulk_posts, 25)
        clouds_list = []
        for post in filtered_posts:
            print(post['url'])
            cloud = Parser(post['url']).generate_cloud()
            print(cloud)
            clouds_list.append(cloud)
