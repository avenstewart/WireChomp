import unittest
from Analytics import TextAnalysis
from Sources import Reddit

class RedditParsingTests(unittest.TestCase):

    def setUp(self):
        self.chomper = Reddit.RedditChomper()

    def testA(self):
        # get all posts from a date with a 24 hour lookback, limited to 50 articles per subreddit
        bulk_posts = self.chomper.get_posts_before_datetime(1631163600, 24, 100, 10)
        filtered_posts = self.chomper.filter_by_score(bulk_posts, 1)
        clouds_list = []
        cloud_engine = TextAnalysis.CloudEngine()

        for post in filtered_posts:
            print(post['url'])
            cloud = cloud_engine.generate_cloud(post['url'])
            print(cloud)
            clouds_list.append(cloud)

        master_cloud = cloud_engine.merge_all(clouds_list)
        print(len(master_cloud))

