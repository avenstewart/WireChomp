import trafilatura
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

class CloudEngine:

    def __init__(self):
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words('english'))

    def generate_cloud(self, url=str):
        results_cloud = {}
        keys_list = []

        raw_html = trafilatura.fetch_url(url)
        raw_content = trafilatura.extract(
            raw_html, include_comments=False, include_tables=False, no_fallback=True
        )

        raw_tokens = self.tokenizer.tokenize(raw_content)
        filtered_tokens = [tkn for tkn in raw_tokens if not tkn.lower() in self.stop_words]
        [keys_list.append(tkn) for tkn in filtered_tokens if tkn not in keys_list]
        for key in keys_list:
            results_cloud[key] = filtered_tokens.count(key)
        return results_cloud

    @staticmethod
    def merge_all(clouds_list=list):
        results_cloud = {}
        keys_list = []

        # noinspection PyTypeChecker
        for cloud in clouds_list:
            [keys_list.append(tkn) for tkn in cloud if tkn not in keys_list]
            for key in keys_list:
                results_cloud[key] += keys_list[key]
        return results_cloud

