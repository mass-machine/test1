def filtrationprompt_for_entities(sentence,entities):
    prompt = "\nSentence: " + sentence + "\nEntity: "+entities+"\nPlease filter the entity list below based on the sentence above and select the entities that you think are relevant to the sentence and do not need to answer the questions in the sentence and return the entities in a list." 
    return prompt