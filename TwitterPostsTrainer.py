# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from settings import TWITTER
from TwitterTrainerManual import TwitterTrainerManual
import logging


# Comment out the following line to disable verbose logging
#logging.basicConfig(level=logging.INFO)
def TrainForPhrase(parsed_phrase):
    bot = ChatBot(
        "VASMultiAgentSystem",
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ],
        database="./twitter-database.db",
        input_adapter = "chatterbot.input.VariableInputTypeAdapter",
        twitter_consumer_key=TWITTER["CONSUMER_KEY"],
        twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
        twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
        twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
        
    )
    #bot.set_trainer(TwitterTrainerManual,parsed_phrase=parsed_phrase)
    #bot.train()
    trainer = TwitterTrainerManual(bot, parsed_phrase=parsed_phrase)
    trainer.train()
    print("successful training")