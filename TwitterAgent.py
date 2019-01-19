#!/usr/bin/env python3
from spade import agent
import time
import PhraseProcessor
import TwitterPostsTrainer
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template

RECIEVE_STATE = "RECIEVE_STATE"
SEND_STATE = "SEND_STATE"
END_STATE = "END_STATE"
user_message = "failure"
class BotBehaviour(FSMBehaviour):
	async def on_start(self):
		print(f"agent starting at the initial state {self.current_state}")
	async def on_end(self):
		print(f"Agent finished at state {self.current_state}")

class RecieveState(State):
	async def run(self):
		self.msg = await self.receive(timeout=15)
		if(self.msg):
				global user_message
				print("Message received with content: {}".format(self.msg.body))				
				keywords = PhraseProcessor.extract_keywords(self.msg.body)
				user_message = self.msg.body			
				TwitterPostsTrainer.TrainForPhrase(keywords, user_message)
		self.set_next_state(SEND_STATE)		

class SendState(State):
	async def run(self):
		global user_message
		if (user_message != "failure"):
			msg = Message(to = "chattingAgent@localhost")
			msg.sender = "twitterAgent@localhost"
			msg.body = user_message
			msg.set_metadata("performative","inform")
			msg.set_metadata("ontology","research-theme")		
			await self.send(msg)
		self.set_next_state(RECIEVE_STATE)

class TwitterAgent(Agent):	
	def setup(self):
		print("TwitterAgent created!")
		behaviour = BotBehaviour()
		behaviour.add_state(name=RECIEVE_STATE, state=RecieveState(), initial = True)
		behaviour.add_state(name=SEND_STATE, state=SendState())
		behaviour.add_transition(source=RECIEVE_STATE, dest=SEND_STATE)
		behaviour.add_transition(source=SEND_STATE, dest=RECIEVE_STATE)
		template = Template()
		template.to="twitterAgent@localhost"
		template.set_metadata("performative","inform")
		template.set_metadata("ontology","research-theme")
		self.add_behaviour(behaviour, template)

if __name__ == "__main__":
	twitterAgent = TwitterAgent("twitterAgent@localhost", "twitterPassword")
	twitterAgent.start()
	while twitterAgent.is_alive():
		try:
			time.sleep(1)
		except KeyboardInterrupt:
			twitterAgent.stop()
			break
	print("Twitter agent finished")