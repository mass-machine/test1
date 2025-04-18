import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--max_length_cot", type=int, default=256,
        help="maximum length of output tokens by model for reasoning extraction"
    )
    parser.add_argument(
        "--max_length_direct", type=int, default=32,
        help="maximum length of output tokens by model for answer extraction"
    )
    parser.add_argument(
        "--limit_dataset_size", type=int, default=0,
        help="whether to limit test dataset size. if 0, the dataset size is unlimited and we use all the samples in the dataset for testing."
    )
    parser.add_argument(
        "--api_time_interval", type=float, default=2.0, help=""
    )
    parser.add_argument(
        "--temperature", type=float, default=0, help=""
    )
    parser.add_argument(
        '--dataset', default='CommonsenseQA',
        help="dataset",
        choices=["2WikimhQA", "gsm8k", "hotpotQA", "logiQA", "AddSub", "SingleEq", "CommonsenseQA", "StrategyQA","AuQA"]
    )
    parser.add_argument(
        "--type_list_file", default="./src/format/entity_type_list.txt", type=str, help='file path'
    )
    parser.add_argument(
        "--datapath", default=None, type=str, help='file path'
    )
    parser.add_argument(
        "--api_key", default="", type = str, help='gpt api_key'
    )
    parser.add_argument(
        "--prompt_id", default='324', help='string'
    )
    parser.add_argument(
        "--infer_num", default='5', help='string'
    )
    parser.add_argument(
        "--engine", default="llama3-8b", help="llama2-7b, llama2-13b, llama-7b,",
        choices=["llama2-7b", "llama2-13b", "llama-7b","llama3-8b","Mistral-7b","llama3-70b"]
    )
    parser.add_argument(
        "--model_path", default='./LLM-Research/Meta-Llama-3-8B-Instruct', help="your local model path"
    )
    parser.add_argument(
        "--test_start", default='0', help='string, number'
    )
    parser.add_argument(
        "--test_end", default='full', help='string, number'
    )
    parser.add_argument(
        "--SC", default=True, type=bool, help="self consistency"
    )
    parser.add_argument(
        '--answer_extracting_prompt', default='The answer is', type=str
    )
    parsed_args = parser.parse_args()
    return parsed_args


args = parse_arguments()
