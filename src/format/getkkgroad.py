def get_KGrelation_prompt(args,relation,element):
    format1 = """
    Please construct multiple inference paths based on the given triplet relationship and relevant text. The format of the inference path is: entity → relationship → entity → relationship...
    """
    prompt_prefix="""Given a sentence, and hign value relationships within the sentence. 
    You need to generate one or more reasoning paths based on these relationships. Examples of reasoning paths are as follows.
    """
    prompt_prefix1 = """Given a sentence, and hign value relationships within the sentence. 
    You need to generate one or up to five reasoning paths based on these relationships. An example of a reasoning path is as follows.
    """

    prompt_suffix = "\nPlease generate one or more what you believe to be the correct and factual reasoning path based on the above requirements, do not generate code. do not explain. do not answer the Question.Your path should mimic examples, not be displayed with letters :"
    prompt=(prompt_prefix1+format1+"\nQuestion: "+element+"\n  The relations will be presented, with the last number representing the score for each relationship \n"+relation+"\n"+prompt_suffix)
    return prompt

def Repeatremoval(args,relation):
    prompt="Please optimize these reasoning paths and display the optimization results \n Relations path:"+relation
    prompt="""
    Please optimize the path length for paths longer than 10 based on the given paths, with the following requirements
    1.Redundancy Removal: Eliminating duplicate or semantically similar nodes to streamline paths.
        How to do: Remove duplicate nodes or words with similar meanings.
            • E.g.: "A→B→B→C" → Simplify to "A→B→C"
            • E.g.: Merge synonyms ("happy→joyful→pleased" → Unify as "happy")
            Target: Reduces path length and avoids redundancy.
    2.Structural Adjustment:Reordering entities to enhance reasoning clarity.
        How to do: Reorder nodes to follow logical sequences (e.g., time order, cause-effect).
            • E.g.: "rain→wet ground→bring umbrella" → Adjust to "rain→bring umbrella→wet ground"
            Target: Improves coherence and readability.
    3.Path Reconstruction:Merging sub-paths to retain key information while ensuring coherence.
        How to do: Merge sub-paths, keeping only essential nodes.
            • E.g.: "study→review→exam→pass exam→celebrate" → Simplify to "study→exam→celebrate"
            Target: Preserves key information while shortening the path.
    """+"\nPlease optimize these inference paths with lengths exceeding 10 according to the above requirements and display the optimization results \n Relations path:"+relation
    return prompt


def kganswerprompt(args,relation,element):
    prompt_suffix_for_csqa='''Please carefully consider the above requirements then give the only answer choice as (A)or(B)or(C)or(D)or(E). \nTherefore the answer is : '''
    prompt_suffix_for_strategyqa='''Please carefully consider the above requirements then give the only answer choice as yes or no. \nTherefore the answer is : '''
    prompt_suffix_for_gsm8k='''Please carefully consider the above requirements then Provide corresponding explanations after answering correctly  \nTherefore the answer is : '''
    prompt_suffix_for_logiqa='''Please carefully consider the above requirements then give the only answer choice as (A)or(B)or(C)or(D). \nTherefore the answer is : '''
    prompt_suffix_for_openquestion="\nYou first answer the question, then output the explanation, with the answer starting with Therefore the answer is :"
    prompt=("Based on the reasoning paths, please answer the given question . \nReasoning Paths:\n"+relation+"\nQuestion:"+element+"\n"+prompt_suffix_for_csqa)
    #Here are some examples:\n"+example+
    return prompt

def Dual_threshold_Filtering(args,high_relation,low_relation,middle_relation,element):
    prompt_suffix="Now there are high score triples and low score triples here respectively. Please analyze the sentence based on the high score triples and low score triples, and determine whether to extract some triples with intermediate scores and put them into the high score triples.\n"
    prompt=(prompt_suffix+"there are high score triples.\n"+high_relation+"\nthere are low score triples.\n"+low_relation+"\nthere are middle score triples.\n"+middle_relation+"\nPlease extract the important middle score triplets according to the previous requirements.Every relationship stated return as a triple: (E_A, E_B, Relation),don't take the score")
    return prompt