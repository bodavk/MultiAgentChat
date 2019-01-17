# -*- coding: utf-8 -*-
from chatterbot import ChatBot
from settings import TWITTER
from TwitterTrainerManual import TwitterTrainerManual
import logging

def TrainForPhrase(parsed_keywords):
    bot = ChatBot(
        "VASMultiAgentSystem",
        logic_adapters=[
            "chatterbot.logic.BestMatch"
        ]
        #database="./twitter-database.db"        
    )
    trainer = TwitterTrainerManual(bot, parsed_keywords=parsed_keywords,
        twitter_consumer_key=TWITTER["CONSUMER_KEY"],
        twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
        twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
        twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"])
    trainer.train()
    print("successful training")