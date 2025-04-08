import torch
import time
import os
import json
from transformers import LlamaTokenizer, LlamaForCausalLM, AutoConfig
from transformers import AutoModelForCausalLM, AutoTokenizer,GenerationConfig
# from peft import PeftModel


def model_init(args):
    model_path = args.model_path # Replace to your model path
    # add_state_model_dir = "" # Option for PEFT
    #device = torch.device("cuda:3")
    # adapter_len = 32
    # config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, adapter_len = adapter_len)
    tokenizer = AutoTokenizer.from_pretrained(model_path, legacy=False)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,# config = config, 
        torch_dtype=torch.float16,
        #pad_token_id=tokenizer.eos_token_id,
        do_sample=True,
        device_map='auto'
    )#.to(device)
    model=model.eval()
    return model, tokenizer #device 'sequential' "balanced_low_0"

def predict(args, prompt, model, tokenizer):
    # add_state_dict = torch.load(os.path.join(add_state_model_dir, "pytorch_model.bin"))
    # model.load_state_dict(add_state_dict, strict=False)
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda:0')
   # inputs = model.prepare_inputs_for_generation(inputs)
    generation_config = GenerationConfig(
    max_new_tokens=256,  # 生成文本的最大长度
    do_sample=True,    # 控制生成的随机性
    temperature=args.temperature,
    pad_token_id=tokenizer.eos_token_id)#
    generate_ids = model.generate(**inputs,max_new_tokens=256, temperature=args.temperature,pad_token_id=tokenizer.eos_token_id)
    #print(generate_ids)
    #max_length=512
    #max_new_tokens=256
    generate_ids = generate_ids[0][len(inputs["input_ids"][0]):-1]
    infer_res = tokenizer.decode(generate_ids)
    #print(infer_res)
    return infer_res

def predict128(args, prompt, model, tokenizer):
    # add_state_dict = torch.load(os.path.join(add_state_model_dir, "pytorch_model.bin"))
    # model.load_state_dict(add_state_dict, strict=False)
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda:0')
    #print(inputs)
    #inputs = model.prepare_inputs_for_generation(inputs)
    generation_config = GenerationConfig(
    max_new_tokens=128,  # 生成文本的最大长度
    do_sample=True,    # 控制生成的随机性
    temperature=args.temperature,
    pad_token_id=tokenizer.eos_token_id)# generation_config=generation_config
    generate_ids = model.generate(**inputs,max_new_tokens=128, temperature=args.temperature,pad_token_id=tokenizer.eos_token_id)
    # print('***************')
    # print(len(inputs["input_ids"][0]))
    # print(generate_ids)
    #max_length=512
    #max_new_tokens=256
    generate_ids = generate_ids[0][len(inputs["input_ids"][0]):-1]
    #print(generate_ids)
    infer_res = tokenizer.decode(generate_ids)
    #print(infer_res)
    return infer_res

def predict12(args, prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt").to('cuda:0')

    # 打印输入数据，确保没有问题
    print("Inputs:", inputs)

    # 生成配置直接传递给 generate
    generate_ids = model.generate(
        **inputs,
        max_length=inputs["input_ids"].shape[1] + 128,  # 确保生成最多128个 token
        do_sample=True,
        temperature=args.temperature,
        top_p=0.9,  # 控制生成多样性
        top_k=50,   # 控制候选 token 数量
        pad_token_id=tokenizer.eos_token_id
    )

    # 检查生成的 ids
    print("Generated IDs:", generate_ids)

    # 获取生成结果的长度
    generated_length = generate_ids.size(1)
    input_length = len(inputs["input_ids"][0])

    # 切片操作：去除输入部分并去掉最后的结束符
    if generated_length > input_length:
        generate_ids = generate_ids[0][input_length:-1]
    else:
        generate_ids = generate_ids[0][input_length:]

    # 打印生成的 token IDs
    print("Final Generated IDs:", generate_ids)

    # 解码生成的 token IDs
    infer_res = tokenizer.decode(generate_ids, skip_special_tokens=True)
    print("Decoded Result:", infer_res)

    return infer_res

        # #新的法子
    # # 获取生成结果的长度
    # generated_length = generate_ids.size(1)

    # # 获取输入的 token 长度
    # input_length = len(inputs["input_ids"][0])

    # # 确保生成的长度大于输入的长度，然后进行切片
    # if generated_length > input_length:
    #     # 切掉输入部分并去除最后的结束符
    #     generate_ids = generate_ids[0][input_length:-1]
    #     print('--------')
    # else:
    #     # 如果生成的长度小于或等于输入的长度，直接使用原始生成内容
    #     generate_ids = generate_ids[0][input_length:]
    #     print('ssssssssss')

    # # 打印生成的 ids（可用于调试）
    # print(generate_ids)

    # # 解码生成的 ids
    # infer_res = tokenizer.decode(generate_ids, skip_special_tokens=True)
    #####################