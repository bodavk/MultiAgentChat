#!/usr/bin/env python3
import nltk
import spacy 
from spacy import displacy

def extract_keywords(original_phrase):
	nlp = spacy.load('en')

	document = nlp(original_phrase)

	entities = [ent for ent in document.ents]
	phrases = [chunk for chunk in document.noun_chunks]
	important_words = get_important_parts_of_text(document)
	keywords = get_most_common_words(phrases, entities,important_words)

	return keywords

def get_important_parts_of_text(doc):
	#maybe find a way to remove find, search, tell and similair vers that are not part of the question etc.
	noise_words = ['-PRON-', 'be']
	minimal_word_length = 2
	important = []
	for token in doc:
		if (len(token.string) > minimal_word_length) and (token.lemma_ not in noise_words) and (not token.is_stop):
			if 'subj' in token.dep_:
				important.append(token)
			if 'obj' in token.dep_:
				important.append(token)
			if 'VERB' == token.pos_ or 'ROOT' in token.dep_:
				important.append(token)
			if 'poss' in token.dep_:
				important.append(token)
	return important

def get_most_common_words(list_phrases, list_entitites, list_of_important_words):
	keywords = []

	#if something is an entity it probably is the keyword
	#if keywords isn't empty check if entity already made the list, else just add it.
	if(keywords.count != 0):
		for entity in list_entitites:
			if (not any(entity.text in keyword.text for keyword in keywords)):
				keywords.append(entity)
	elif (list_entitites.count != 0):
		for entity in list_entitites:
			keywords.append(entity)
	if(len(list_of_important_words) != 0):
		for important_word in list_of_important_words:
			if important_word not in keywords:
				keywords.append(important_word)
	return keywords

if __name__ == "__main__":
	phrase = "what's the tommorrow's weather in miami or rather tell me more about the trump's wall"
	print (phrase)
	keywords = extract_keywords(phrase)
	displacy.serve(keywords, style='dep')
	print (keywords)
