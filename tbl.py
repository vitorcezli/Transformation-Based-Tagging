#!/usr/bin/python
from template import Template


def get_best_instance( tags, tagging_corpus, tagged_corpus, template ):
	# it will be used to store the rules with their scores
	dictionary = {}

	# parse the corpus and the correct tagging
	for to_tags in tags:
		for index in range( len( tagging_corpus ) ):
			first_index = template.first_index( index )
			last_index = template.last_index( index, len( tagging_corpus ) )

			# invalid positions. The rule isn't applied on them
			if ( first_index != Template.INVALID ) and \
			   ( last_index != Template.INVALID ):
				# the rule must specify a change. So, if the tags are the same
				# no change will occur
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


def most_likely_tags( corpus ):
	return [ 'A', 'C', 'B', 'A', 'B', 'C', 'A', 'C', 'C' ]


def generate_relevant_templates():
	return [ ( 1, 1 ), ( 0, 1 ), ( 1, 0 ) ]


def tbl( tags, corpus, tagged_corpus ):
	tagging_corpus = most_likely_tags( corpus )
	forms = generate_relevant_templates()
	template_list = []
	
	while True:
		result = get_best_transform( tags, tagging_corpus, \
			tagged_corpus, forms )
		if result[ 0 ] <= 0:
			return template_list
		else:
			template = result[ 1 ]
			template_list.append( template )
			template.make_transformation( tagging_corpus )
			print template.get_rule
			print tagging_corpus



# this part is being used just for test
tags = [ 'A', 'B', 'C' ]
corpus = []
correct_tagging = [ 'A', 'C', 'A', 'A', 'A', 'C', 'A', 'C', 'B' ]

tbl( tags, corpus, correct_tagging )