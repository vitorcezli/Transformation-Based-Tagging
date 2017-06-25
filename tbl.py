#!/usr/bin/python
from __future__ import division
from template import Template
import collections


def get_best_instance( tags, tagging_corpus, tagged_corpus, template ):
	# it will be used to store the rules with their scores
	dictionary = {}

	# parse the corpus and the correct tagging
	for index in range( len( tagging_corpus ) ):
		first_index = template.first_index( index )
		last_index = template.last_index( index, len( tagging_corpus ) )

		# invalid positions. The rule isn't applied on them
		if ( first_index != Template.INVALID ) and \
		   ( last_index != Template.INVALID ):
			# the rule must specify a change. So, if the tags are the same
			# no change will occur
			for to_tags in tags:
				if ( tagging_corpus[ index ] != to_tags ):
					# the rule's score is incremented because for this example
					# it will be a good transition
					if to_tags == tagged_corpus[ index ]:
						if ( tagging_corpus[ first_index ], \
							 tagging_corpus[ last_index ], \
							 tagging_corpus[ index ], \
							 to_tags ) in dictionary:
							dictionary[ tagging_corpus[ first_index ], \
							            tagging_corpus[ last_index ], \
							            tagging_corpus[ index ], \
							            to_tags ] += 1
						else:
							dictionary[ tagging_corpus[ first_index ], \
							            tagging_corpus[ last_index ], \
							            tagging_corpus[ index ], \
							            to_tags ] = 1
					# the rule's score is decremented because for this example
					# it will be a bad transition
					else:
						if ( tagging_corpus[ first_index ], \
							 tagging_corpus[ last_index ], \
							 tagging_corpus[ index ], \
							 to_tags ) in dictionary:
							dictionary[ tagging_corpus[ first_index ], \
							            tagging_corpus[ last_index ], \
							            tagging_corpus[ index ], \
							            to_tags ] -= 1
						else:
							dictionary[ tagging_corpus[ first_index ], \
							            tagging_corpus[ last_index ], \
							            tagging_corpus[ index ], \
							            to_tags ] = -1

	# gets the rule with the best score from the dictionary
	best_score = 0
	best_rule = ( '0' )
	for rule, score in dictionary.viewitems():
		if score > best_score:
			best_score = score
			best_rule = rule

	# returns the best rule and its score
	return ( best_score, best_rule )


def get_best_transform( tags, tagging_corpus, tagged_corpus, forms ) :
	best_score = 0

	itv = '\0' # invalid template value
	best_template = Template( itv, itv, itv, itv, itv, itv )

	for form in forms:
		template = Template( form[ 0 ], itv, form[ 1 ], itv, itv, itv )
		values_best_instance = get_best_instance( tags, tagging_corpus, \
			tagged_corpus, template )
		score = values_best_instance[ 0 ]
		
		if score > best_score:
			best_score = score
			rule = values_best_instance[ 1 ]
			best_template = Template( form[ 0 ], rule[ 0 ], form[ 1 ], \
				rule[ 1 ], rule[ 2 ], rule[ 3 ] )

	return ( best_score, best_template )


def get_corpus( corpus_path ):
	file  = open( corpus_path, 'r' )
	corpus = file.read()
	file.close()
	corpus_list = []
	
	for word_and_tagging in corpus.split():
		word = word_and_tagging.split( '/' )
		corpus_list.append( word[ 0 ] )
	return corpus_list


def get_tagging():
	file  = open( 'corpus.txt', 'r' )
	corpus = file.read()
	file.close()
	tagging_list = []
	
	for word_and_tagging in corpus.split():
		tagging = word_and_tagging.split( '/' )
		tagging_list.append( tagging[ 1 ] )
	return tagging_list


def most_likely_tags_dictionary( corpus, tagging ):
	# count the different taggings of each word
	dictionary = {}
	for index in range( len( corpus ) ):
		if ( corpus[ index ], tagging[ index ] ) in dictionary:
			dictionary[ corpus[ index ], tagging[ index ] ] += 1
		else:
			dictionary[ corpus[ index ], tagging[ index ] ] = 1

	# orders the dictionary
	tagging_dictionary = {}
	sorted_dictionary = collections.OrderedDict( sorted( dictionary.items() ) )

	# gets the most likely tags and put them on another dictionary
	last_word = ''
	best = 0
	for tagging, times in sorted_dictionary.viewitems():
		if last_word != tagging[ 0 ]:
			best = times
			tagging_dictionary[ tagging[ 0 ] ] = tagging[ 1 ]
		else:
			if times > best:
				best = times
				tagging_dictionary[ tagging[ 0 ] ] = tagging[ 1 ]

	return tagging_dictionary


def most_likely_tags( corpus, tagging_dictionary ):
	# gets the most likely tagging classification for the corpus
	most_likely_tagging = []
	for index in range( len( corpus ) ):
		if corpus[ index ] in tagging_dictionary:
			most_likely_tagging.append( tagging_dictionary[ corpus[ index ] ] )
		else:
			most_likely_tagging.append( 'ukn' ) # for unknown words

	# returns the most likely tagging
	return most_likely_tagging


def generate_relevant_templates():
	return [ ( 1, 1 ), ( 0, 1 ), ( 1, 0 ) ]


def tbl( tags, corpus, tagged_corpus ):
	tagging_dictionary = most_likely_tags_dictionary( corpus, tagged_corpus )
	tagging_corpus = most_likely_tags( corpus, tagging_dictionary )
	forms = generate_relevant_templates()
	template_list = []
	number_rules = 0
	
	while True:
		if( number_rules == 10 ):
			return template_list
		result = get_best_transform( tags, tagging_corpus, \
			tagged_corpus, forms )
		if result[ 0 ] <= 0:
			return template_list
		else:
			template = result[ 1 ]
			template_list.append( template )
			template.make_transformation( tagging_corpus )
			print template.get_rule()
			number_rules += 1
	return template_list


def print_tagging_error( corpus, correct, dictionary ):
	error = 0

	for index in range( len( corpus ) ):
		if correct[ index ] != dictionary[ corpus[ index ] ]:
			error += 1

	error_rate = error / len( corpus )
	print error_rate


# get the data for the training
corpus = get_corpus( 'corpus.txt' )
corpus = corpus[ 0 : 10000 ]
correct_tagging = get_tagging()
correct_tagging = correct_tagging[ 0 : 10000 ]
tagging_dictionary = most_likely_tags_dictionary( corpus, correct_tagging )
tags = list( set( correct_tagging ) )

print_tagging_error( corpus, correct_tagging, tagging_dictionary )

# train the tbl
template_rules = tbl( tags, corpus, correct_tagging )

# make a classification based on the training
file  = open( 'classify.txt', 'r' )
corpus_to_classify = file.read()
file.close()
corpus_to_classify = corpus_to_classify.split()
tagged_corpus = most_likely_tags( corpus_to_classify, tagging_dictionary )
for template in template_rules:
	template.make_transformation( tagged_corpus )

# print the classification
for index in range( len( corpus_to_classify ) ):
	word = corpus_to_classify[ index ] + '/' + tagged_corpus[ index ]
	print word,
print
