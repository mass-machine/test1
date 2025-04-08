import json
import logging
import re
import json
from config import args
from utils import write_json, print_now, load_data, print_exp, mkpath
from src.format.entity_extraction_prompt import get_ner_list, get_ner_prompt, ner_sentence
from src.model.llama2_predict import predict, model_init,predict128
from src.format.relation_extract import get_extract_prompt
from src.format.discrimination import get_discrimination_prompt
from src.format.qa import get_qa_prompt
from transformers import LlamaTokenizer, LlamaForCausalLM, AutoConfig
from src.format.entity_filtra import filtrationprompt_for_entities
from src.format.getkkgroad import get_KGrelation_prompt,kganswerprompt,Repeatremoval,Dual_threshold_Filtering
def run_llama():
    ner_prompt = get_ner_prompt(args.type_list_file)
    question, answer, ids = load_data(args)
    model, tokenizer = model_init(args)
    for idx, element in enumerate(question):
        prompt = ner_sentence(ner_prompt, element)
        answernow=answer[idx]
        print(answernow)
        #Filter entity module
        entities = predict(args, prompt, model, tokenizer)   
        filtrationprompt_entities=filtrationprompt_for_entities(element,entities)
        entities = predict(args, filtrationprompt_entities, model, tokenizer)
        #Relationship extraction module
        prompt = get_extract_prompt(entities, element)
        relation_ext = predict(args, prompt, model, tokenizer) 
        relation = relation_ext
        #Threshold rating
        high_relation = "\n The currently selected high score relationships : "
        middle_relation="\n The currently selected middle score relationships : "
        low_relation="\n The currently selected low score relationships : "
        try: 
            ralation_inf_list = re.findall(r'[(](.*?)[)]', relation_ext) 
            prompt = get_discrimination_prompt(args, entities, relation_ext, element)
            scores = predict(args, prompt, model, tokenizer)
            relation_inf_list1=scores.splitlines()
            scorelist=['1','2','3','4','5','6','7','8','9']
            for i in range(len(relation_inf_list1)):
                for j in  reversed(relation_inf_list1[i]):
                    if j in scorelist:
                        if int(j)>=7:
                            index = relation_inf_list1[i].rfind(j)
                            high_relation = high_relation +"\n"+ relation_inf_list1[i]
                            break
                        elif int(j)<=3:
                            low_relation = low_relation +"\n"+relation_inf_list1[i]
                            break
                        else:
                            middle_relation = middle_relation +"\n"+relation_inf_list1[i]
        except Exception as e: 
            relation = relation_ext
        if middle_relation=="":
            relation = relation+high_relation
        else:
                Dual_threshold_Filtering_prompt=Dual_threshold_Filtering(args,high_relation,low_relation,middle_relation,element)
                relation_fin=predict(args,Dual_threshold_Filtering_prompt,model,tokenizer)
                relation=relation+high_relation+relation_fin
        #Path construction
        knowledgerelatio_promt=get_KGrelation_prompt(args,relation,element)
        knowledgerelatio=predict128(args, knowledgerelatio_promt, model, tokenizer)
        #Path optimization
        knowledgerelatioreprompt=Repeatremoval(args,knowledgerelatio)
        knowledgerelatiore=predict128(args, knowledgerelatioreprompt, model, tokenizer)
        kgpredictprompt=kganswerprompt(args, knowledgerelatiore, element)
        #Self consistency answer
        for i in range(10):
            modelanswer = predict(args, kgpredictprompt, model, tokenizer)
            print(modelanswer)

if __name__ == '__main__':
    print_exp(args) 
    enginellama=['llama2-7b',"llama3-8b","Mistral-7b","llama3-70b"]
    if args.engine in enginellama:
        run_llama()