import json
import logging

# from config import args
prompt_prefix = '''Given a context and all the entities within it, please extract the relationships associated with these entities and form multiple triplet relations. 
The format should be (Ei, Ej, r).\nContext: '''

prompt_suffix = '''\nRelation: '''
prompt_suffix1='''\n Please extract the relationship according to the above requirements, do not generate code.do not explain. you just need output the entities relations:'''
def get_extract_prompt(entities, sent):
    relation_prompt = prompt_prefix + sent + "\nEntities: " + entities + prompt_suffix1
    return relation_prompt
