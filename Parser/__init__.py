import trafilatura
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# you must execute nltk.download('punkt') on a python console if you have not already

class Parser:
    def __init__(self, url):
        raw_html = trafilatura.fetch_url(url)
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.stop_words = set(stopwords.words('english'))
        self.raw_content = trafilatura.extract(
            raw_html, include_comments=False, include_tables=False, no_fallback=True
        )

    def generate_cloud(self):
        results_cloud = {}
        keys_list = []
        tokenizer = RegexpTokenizer(r'\w+')
        raw_tokens = self.tokenizer.tokenize(self.raw_content)
        filtered_tokens = [tkn for tkn in raw_tokens if not tkn.lower() in self.stop_words]
        [keys_list.append(tkn) for tkn in filtered_tokens if tkn not in keys_list]
        for key in keys_list:
            results_cloud[key] = filtered_tokens.count(key)
        return results_cloud