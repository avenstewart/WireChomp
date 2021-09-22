# WireChomp
Bulk language extraction engine designed to generate large word clouds from
bulk news data within a specified 24 hour period. The resulting information 
may be useful for sentiment analysis or other projects.

## Dependencies
WireChomp uses python3+, and requires the following extensions:
- [**NLTK**](https://www.nltk.org/) : natural language process library
- [**Trafiltura** ](https://trafilatura.readthedocs.io/en/latest/): HTML content processing tool
- [**PRAW**](https://praw.readthedocs.io/en/stable/) : Reddit API tools, not currently used but may be useful as project progresses
```
pip3 install nltk trafiltura praw
```

## Usage
Currently this project contains 2 packages; **Sources** and **Analytics**.
WireChomp works by ingesting raw news data from multiple sources,
pulling the main textual content, and parsing it into _"word clouds"_,
which are then merged to create larger clouds representing the most 
common words for that 24 hour period.

- The Sources package contains classes built to handle the ingesting of 
news articles from various sources and APIs. At this time, this is limited to Reddit,
ingested using the [PushShift](https://github.com/pushshift/api).

- The Analytics package contains methods that can be used for parsing, manipulation, and 
analysis of raw data returned by the sources.

The **test** and **resources** folders are self-explanatory,
within these you will find unit tests and configuration files, respectively.

### Configuration
Within the resources folder you will find _sourceconfig.ini.example_.
This is an example config file containing multiple sections with config variables 
corresponding to the different data sources used by WireChomp. You must use 
this file to create your own config file in the same directory and name it 
_sourceconfig.ini_.

**Reddit Configuration Variables**
- _subreddit_list_: comma delimited, double quoted list of subreddits to scrape
- _post_score_threshold_: minimum post score for inclusion
- _exclude_news_domains_: comma delimited, double quoted domain blacklist
- _praw_certfile_path_: path to certfile.pem
- _praw_client_id_: obtained by creating a reddit developer app [here](https://www.reddit.com/prefs/apps)
- _praw_client_secret_ = obtained by creating a reddit developer app
- _praw_reddit_username_: Reddit account username
- _praw_reddit_password_: Reddit account password
- _user_agent_: user agent for requests
- _request_delay_: minimum delay between requests in seconds

## Testing
The unit testing class is currently utilized by the developers of this project to test
different methods and functions as we develop them. 


## Contributing
Only contributions from approved developers are accepted at this time.  Please make sure to update tests as appropriate.
