from chatterbot.conversation import Statement
from chatterbot import trainers
from chatterbot import utils
from TwitterSearch import *

class TwitterTrainerManual(trainers.Trainer):
    """
    Allows the chat bot to be trained using data
    gathered from Twitter.
    :param random_seed_word: The seed word to be used to get random tweets from the Twitter API.
                             This parameter is optional. By default it is the word 'random'.
    :param twitter_lang: Language for results as ISO 639-1 code.
                         This parameter is optional. Default is None (all languages).
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)
        self.max_number_of_tweets = 10
        self.chatbot = chatbot
        self.keywords = kwargs.get('parsed_keywords') 
        self.phrase = kwargs.get('parsed_phrase')
        self.ts = TwitterSearch(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def get_statements(self):
        """
        Returns list of statements from the API.
        """       
        statements = []

        search_keywords = self.keywords
        search_phrase = self.phrase 
        tso = TwitterSearchOrder()
        tso.set_keywords(search_keywords)
        tso.set_language('en')
        tso.set_include_entities(True)
        tso.set_count(50)
        for tweet in self.ts.search_tweets_iterable(tso):
            try:
                #make sure the tweet message is intact and that it isn't a retweet so that the text is readable
                if (tweet['truncated'] == False and 'retweeted_status' not in tweet):
                    tweet_text = tweet['text']
                    statement_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(tweet_text)
                    phrase_search_text = self.chatbot.storage.tagger.get_bigram_pair_string(search_phrase)
                    statement = Statement(
                        text = tweet_text, 
                        search_text = statement_search_text,
                        in_response_to = search_phrase,
                        seach_in_response_to = phrase_search_text,
                        conversation = 'training')
                    statements.append(statement)
            except KeyError:
                return "Tweet is incorrect"
        #TODO clean up tweets from @symbols or make the tweets simpler to read, or less awkward as responses
        return statements

    def train(self):
        statements = self.get_statements()
        self.chatbot.storage.create_many(statements)

