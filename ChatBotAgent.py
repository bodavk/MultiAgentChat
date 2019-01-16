#!/usr/bin/env python3
import time
from chatterbot import ChatBot
from spade.agent import Agent
#todo change behaviour of the agent
from spade.behaviour import OneShotBehaviour
from spade.message import Message

class ChattingAgent(Agent):
	messageToSend = ""
	class InformBehavior(OneShotBehaviour):
		content = ""
		async def run(self):
			msg = Message(to="twitterAgent@localhost")
			msg.sender = "chattingAgent@localhost"
			msg.set_metadata("performative", "inform")
			msg.set_metadata ("ontology","research-theme")
			msg.body = self.content

			await self.send(msg)
			
			print("Message with content: {} ; has been successfully sent to the agent".format(msg.body))
			self.exit_code = "Success"
			self.agent.stop

	def setup(self):
		print("Agent successfully started!")
		behaviour = self.InformBehavior()
		behaviour.content = self.messageToSend
		self.add_behaviour(behaviour)

if __name__ == "__main__":
	userInput=""
	while(userInput != "exit"):
		#instead of what do you want to search it should be "smarter"
		userInput = input("What do you want to search?")
		if (userInput != "" and userInput!="exit"):
			chatAgent = ChattingAgent('chattingAgent@localhost','chitchat')
			chatAgent.messageToSend = userInput
			chatAgent.start()
			#recieve successful search message
			#get response according to the input message (analyze the trained set, find best answer)
			while chatAgent.is_alive():
				try:
					time.sleep(1)
					chatAgent.stop()
				except KeyboardInterrupt:
					chatAgent.stop()
					userInput="exit"
					break

