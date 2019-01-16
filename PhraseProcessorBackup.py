#!/usr/bin/env python3
import nltk

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag
from nltk.corpus import wordnet

def extract_keywords(original_phrase):

	tokenized_words = word_tokenize(original_phrase)

	#ovo je trenutni rezultat, "important_words", zasad je problem prevelik broj rijeci
	tagged_words = nltk.pos_tag(tokenized_words)
	important_words = extract_important_parts_of_speech(tagged_words)

	#syns = [wordnet.synsets(word) for word in important_words]
	
	#lemmatizer = WordNetLemmatizer()
	#stems = [lemmatizer.lemmatize() for (word, p) in tagged_words]
	#stem = lemmatizer.lemmatize("")
	
	return important_words
#
# 7, 12, 14 27
# 7 adjective JJ (JJR, JJS comparative, superlative)
# 12 noun (NN singular, NNS noun plural)
# 14 proper noun singular (NNP, NNPS plural)
# 27 verb base form
#

def extract_important_parts_of_speech(words):
	# lambda argument_list: expression
	is_noun = lambda pos: pos == 'NN' or pos == 'NNP' or pos == 'JJ' or pos == 'VB'
	extracted_parts = [word for (word, pos) in words if is_noun(pos)]
	named_entities = nltk.ne_chunk(extracted_parts)
	#named entities trenutno ne radi na ovako maloj recenici
	#ne_taged_words = nltk.ne_chunk(tagged_words)
	#ne_taged_words.draw()
	return extracted_parts



if __name__ == "__main__":
	phrase = "please find me something about the Trump's wall"
	print (phrase)
	keywords = extract_keywords(phrase)
	print (keywords)
