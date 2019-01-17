from chatterbot.conversation import Statement
from chatterbot import trainers
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

        self.chatbot = chatbot
        self.keywords = kwargs.get('parsed_keywords')
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
        search_phrase = ' '.join(search_keywords)
        
        #TODO search twitter for phrases
        tso = TwitterSearchOrder()
        tso.set_keywords(search_keywords)
        tso.set_language('en')
        tso.set_include_entities(False)

        for tweet in self.ts.search_tweets_iterable(tso):
            tweet_text = tweet['text']
            statement = Statement(text=tweet_text, in_response_to=search_phrase)
            statements.append(statement)
        #TODO set constant number of tweets
        #TODO clean up tweets from @symbols
        return statements

    def train(self):
        for _ in range(0, 10):
            statements = self.get_statements()
            for statement in statements:
                self.chatbot.storage.create(
                    text=statement.text,
                    in_response_to=statement.in_response_to,
                    conversation=statement.conversation,
                    tags=statement.tags
                )

