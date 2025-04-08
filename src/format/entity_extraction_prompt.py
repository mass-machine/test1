import json

# from config import args
prompt_prefix = '''Given a sentence, possible entities may include:'''

prompt_suffix = ''', Find all entities based on the provided sentence.'''

def get_ner_list(type_list_file):
    try:
        f = open(type_list_file, "r", encoding="utf-8")
        entities = "["
        for idx, entity in enumerate(f):
            entities = entities + entity[:-1] + ","
        entities = entities[:-1] + "]"
        return entities
    except FileNotFoundError as e:
        raise FileNotFoundError('can\'t find the demo file: {}'.format(type_list_file))

def get_ner_prompt(type_list_file):
    ner_prompt = prompt_prefix + get_ner_list(type_list_file) + prompt_suffix
    return ner_prompt

def ner_sentence(ner_prompt, sentence):
    prompt = ner_prompt + "\nSentence: " + sentence + "\nEntity: "
    showentity="entities:dickens, eggs, mushroom,bank"
    prompt1 = ner_prompt + "\nSentence: " + sentence + "\nYou need to find the entity of the above question and display it, there is no need to answer the question, Please return a list of entities, as shown in the following example"+ showentity
    prompt2=ner_prompt + "\nSentence: " + sentence + "\nPlease find the above Sentence Entity :"
    return prompt2