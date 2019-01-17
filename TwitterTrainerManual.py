from chatterbot.conversation import Statement
from chatterbot import trainers
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
        from twitter import Api as TwitterApi

        self.phrase = kwargs.get('parsed_phrase')
        #self.phrase = parsed_phrase
        self.api = TwitterApi(
            consumer_key=kwargs.get('twitter_consumer_key'),
            consumer_secret=kwargs.get('twitter_consumer_secret'),
            access_token_key=kwargs.get('twitter_access_token_key'),
            access_token_secret=kwargs.get('twitter_access_token_secret')
        )

    def get_statements(self):
        """
        Returns list of statements from the API.
        """
        from twitter import TwitterError
        statements = []

        random_word = self.phrase
        #TODO fix, code breaks somewhere here.
        self.chatbot.logger.info('Requesting 50 tweets containing the phrase {}'.format(random_word))
        tweets = self.api.GetSearch(term=random_word, count=20)
        for tweet in tweets:
            statement = Statement(text=tweet.text)
            if tweet.in_reply_to_status_id:
                try:
                    # korisnikovo pitanje umjesto status.text
                    statement.in_response_to = self.phrase
                    statements.append(statement)
                except TwitterError as error:
                    self.chatbot.logger.warning(str(error))

        self.chatbot.logger.info('Adding {} tweets with responses'.format(len(statements)))
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

