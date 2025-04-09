import json
import logging

# from config import args
prompt_prefix = '''Given some triplets, please rate them based on contextual semantics. 
Score the confidence level of each relationship.
The confidence score ranges from 0 to 10, where a higher score indicates a higher likelihood of the relationship being correct.
Every relationship stated as a triple: (E_A, E_B, Relation). \n'''

score_criteria="""
Scoring criteria

Score 10:
Entity: Dominant presence, appears pervasively across context.
Relationship: Absolutely certain, explicit and deeply integrated in the text, no inference needed.

Score 9:
Entity: Very frequently appears, extremely relevant.
Relationship: Clear and direct, strongly supported by context.

Score 8:
Entity: Frequently appears, highly relevant.
Relationship: Very likely, clearly implied, minimal inference needed.

Score 7:
Entity: Often appears, closely related.
Relationship: Likely, can be inferred through clear chains with some background knowledge.

Score 6:
Entity: Mentioned multiple times, related.
Relationship: Possible, context provides hints but needs confirmation.

Score 5:
Entity: Occasionally mentioned, moderately relevant.
Relationship: Somewhat possible, weak or indirect support.

Score 4:
Entity: Rarely mentioned, low relevance.
Relationship: Vague or unclear connection, minimal evidence.

Score 3:
Entity: Hardly mentioned, very low relevance.
Relationship: Implied at best, requires heavy inference.

Score 2:
Entity: Barely or never mentioned.
Relationship: No clear connection, speculative.

Score 1:
Entity: Not present, unrelated.
Relationship: No connection to context.

\nSententence:
"""

prompt_suffix = '''\Scores: '''
prompt_suffix1='''\n Please output the scores according to the above requirements, do not generate code. do not explain. you should output the relationships. then the score. Please present it in one line  :'''

def get_discrimination_prompt(args, entities, relation_inf, sent):
    relation_prompt = (prompt_prefix + score_criteria+ sent +"\n These are target scoring triplets "+relation_inf + prompt_suffix1)
    return relation_prompt

    # (People, Work, Aim) 9
    # (People, People, Talk) 7
    # (People, Job, Complete) 8
    # (People, People, Learn) 9
    # (People, Animals, Kill) 1
    # (People, Hats, Wear) 1
    # (People, Work, Do) 9
    # (Work, People, Have) 6
    # (Work, Job, Have) 6
    # (Work, People, Be) 9
    # (Work, Job, Be) 9
