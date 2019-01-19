#!/usr/bin/env python3
import time
from chatterbot import filters
from chatterbot import ChatBot
from chatterbot import response_selection
from chatterbot import comparisons
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template
import logging

RECIEVE_STATE = "RECIEVE_STATE"
SEND_STATE = "SEND_STATE"
END_STATE = "END_STATE"
logging.basicConfig(level=logging.CRITICAL)
user_question = ""

#sentiment_comparison, jaccard_similarity, synset_distance, levenshtein_distance
bot = ChatBot('ChatAgent', storage_adapter='chatterbot.storage.SQLStorageAdapter',
	logic_adapters=[
		{'import_path':'chatterbot.logic.BestMatch',
		"statement_comparison_function": comparisons.jaccard_similarity,
		"response_selection_method": response_selection.get_random_response,
		'default_response':'I am sorry but I do not know what to say, ask me later'}], 
	database_uri='sqlite:///db.sqlite3',
	read_only=True,
	filters=[filters.get_recent_repeated_responses]
)

class BotBehaviour(FSMBehaviour):
	async def on_start(self):
		print(f"Agent starting at the initial state {self.current_state}")
	async def on_end(self):
		print(f"Agent finished at state {self.current_state}")

class EndState(State):
	async def run(self):
		print("Agent is shutting down.")
		self.kill()

class RecieveState(State):
	async def run(self):
		global user_question
		print("Still thinking!")
		self.msg = await self.receive(timeout=20)
		if(self.msg):
			#if message isn't empty, and has passed the template it should be the message we need	
			if self.msg.body != "" and self.msg.body!="failure":
				response = bot.get_response(user_question)
				#while(response.confidence < 0.1 and response.confidence!=0):
				#	response=bot.get_response(user_question)
				print (response)
				self.set_next_state(SEND_STATE)	
			else:
				self.set_next_state(RECIEVE_STATE)
		else:
			print("Sorry, can't think of anything,really")
			self.set_next_state(SEND_STATE)

class SendState(State):
	async def run(self):
		global user_question
		minimal_confidence = 0.2
		user_input = input("What would you like to talk about? ")
		if (user_input != "") and (user_input.lower()!="exit"):
			response = bot.get_response(user_input)
			user_question = user_input
			#if response score is low don't show it but instead ask bot to learn something new
			if response.confidence <= minimal_confidence:
				msg = Message(to = "twitterAgent@localhost")
				msg.sender = "chattingAgent@localhost"
				msg.body = user_input				
				msg.set_metadata("performative","inform")
				msg.set_metadata("ontology","research-theme")		
				await self.send(msg)
				print("One moment please, I'm trying to think of an anwser")
				self.set_next_state(RECIEVE_STATE)
			else:
				print(response)
				# it should again enter this same state because the talk should continue without using other agent
				self.set_next_state(SEND_STATE)
		elif user_input.lower()=="exit": 
			self.set_next_state(END_STATE)
		else:
			self.set_next_state(RECIEVE_STATE)

class ChattingAgent(Agent):
	def setup(self):
		print("Chatting agent created")
		behaviour = BotBehaviour()
		behaviour.add_state(name=SEND_STATE, state=SendState(), initial = True)
		behaviour.add_state(name=RECIEVE_STATE, state=RecieveState())
		behaviour.add_state(name=END_STATE, state=EndState())

		behaviour.add_transition(source=SEND_STATE, dest=RECIEVE_STATE)
		behaviour.add_transition(source=SEND_STATE, dest=SEND_STATE)
		behaviour.add_transition(source=SEND_STATE, dest=END_STATE)
		behaviour.add_transition(source=RECIEVE_STATE, dest=SEND_STATE)
		behaviour.add_transition(source=RECIEVE_STATE, dest=RECIEVE_STATE)
		
		template = Template()
		template.to="chattingAgent@localhost"		
		template.set_metadata("performative","inform")
		template.set_metadata("ontology","research-theme")
		self.add_behaviour(behaviour, template)

if __name__ == "__main__":
	chatAgent = ChattingAgent('chattingAgent@localhost','chitchat')
	chatAgent.start()
	while chatAgent.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			chatAgent.stop()
			break

