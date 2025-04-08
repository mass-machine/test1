import json
import logging

# from config import args
prompt_prefix = '''Given a sentence, all entities and all relationships within the sentence. 
Answering the question.
Every relationship stated as a triple: (E_A, E_B, Relation)\nSentence: '''

prompt_suffix = '''Please only give the only answer choice as (A,B,C,D,E). \nAnswer: '''
prompt_suffix1 = '''Please only give the only answer choice as (A)or(B)or(C)or(D)or(E). \nTherefore the answer is : '''
prompt_suffix2 = '''Please carefully consider the above requirements then give the only answer choice as yes or no. \nTherefore the answer is : '''
prompt_suffix_for_gsm8k='''Please carefully consider the above requirements then Provide corresponding explanations after answering correctly  \nTherefore the answer is : '''
prompt_suffix_for_logiqa = '''Please only give the only answer choice as (A)or(B)or(C)or(D). \nTherefore the answer is : '''
prompt_suffix_for_openquestion="\nYou first answer the question, then output the explanation, with the answer starting with Therefore the answer is :"

def get_qa_prompt(args, entities, relation, sent):
    relation_prompt = (prompt_prefix + sent + "\Entities: " + entities
                            + "\nRelationships:: " + relation
                                + "\nQuestion: " + sent + prompt_suffix1)
    return relation_prompt