#!/usr/bin/env python3
import time
from chatterbot import ChatBot
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from spade.template import Template

#TODO change agent behavior to be a FiniteStateMachine
#TODO machine should have send state and receive state 
# -> receive should only check if the other agent is done training the set
	#TODO first check if there already exists an answer to the user's question and try to answer
	#TODO if it doesn't exist send it to the other agent and wait for done signal

RECIEVE_STATE = "RECIEVE_STATE"
SEND_STATE = "SEND_STATE"
END_STATE = "END_STATE"

class BotBehaviour(FSMBehaviour):
	async def on_start(self):
		print(f"agent starting at the initial state {self.current_state}")
	async def on_end(self):
		print(f"Agent finished at state {self.current_state}")

class RecieveState(State):
	async def run(self):
		print("Receive state:")
		self.msg = await self.receive(timeout=10)
		if(self.msg):
				print("Message received {}with content: {}".format(self.msg.sender, self.msg.body))	
				#if self.msg.body == "done":  			**idea, maybe send back the words which to search for
				#	chatbot.get_answer(user_question) 	**current problem is that the user input isn't forwarded
		self.set_next_state(SEND_STATE)		

class SendState(State):
	async def run(self):
		print("Send state:")
		#if flag set to true send, else don't
		user_input = input("What would you like to talk about? ")
		#try to answer with current knowledge
		# 	 if answer grade is low, ask agent to learn how to answer the question
		#else: do stuff written bellow
		if (user_input != "") or (not (user_input.lower()=="exit")):
			msg = Message(to = "twitterAgent@localhost")
			msg.sender = "chattingAgent@localhost"
			msg.body = user_input
			msg.set_metadata("performative","inform")
			msg.set_metadata("ontology","research-theme")		
			await self.send(msg)
			print ("Message from {} sent, content:{}".format(msg.sender, msg.body))
		#if user_input.lower()=="exit": 
			#self.set_next_state(END_STATE)
		#else:
		self.set_next_state(RECIEVE_STATE)

class ChattingAgent(Agent):
	def setup(self):
		print("Chatting agent created")
		behaviour = BotBehaviour()
		behaviour.add_state(name=SEND_STATE, state=SendState(), initial = True)
		behaviour.add_state(name=RECIEVE_STATE, state=RecieveState())
		#behaviour.add_state(name=END_STATE,)

		behaviour.add_transition(source=SEND_STATE, dest=RECIEVE_STATE)
		behaviour.add_transition(source=RECIEVE_STATE, dest=SEND_STATE)
		
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

