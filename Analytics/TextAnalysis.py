import trafilatura
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from math import ceil


class CloudEngine:

    def __init__(self):
        print("Initializing Analysis Engine...")
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words('english'))
        print("Initialization complete.")

    def generate_cloud(self, url=str):
        print("Generating cloud for url: "+url)
        results_cloud = {}
        keys_list = []

        raw_html = trafilatura.fetch_url(url)

        if not raw_html:
            raise IOError

        raw_content = trafilatura.extract(
            raw_html, include_comments=False, include_tables=False, no_fallback=True
        )


        if not raw_content:
            raise IOError

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
                if key in cloud:
                    if key not in results_cloud:
                        results_cloud[key] = 0
                    results_cloud[key] += cloud[key]

        results_iter = list(results_cloud)
        avg_freq = ceil(sum(results_cloud.values())/len(results_cloud))

        # remove words with below average frequency
        for i in range(len(results_iter)):
            key = results_iter[i]
            if results_cloud[key] and results_cloud[key] < avg_freq:
                results_cloud.pop(key)

        return results_cloud

