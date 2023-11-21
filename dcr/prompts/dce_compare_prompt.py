dce_compare_prompt = """
You are an evaluator. You will be given a true answer and an attempt answer.
True answer is the ground truth answer. Attempt answer is the answer you want to evaluate.
Criteria:
Your task is to evaluate whether the attempt answer is consistent with the true answer. You will evaluate it by:
* listing all the aspects in the attempt answer
* compare if each aspects exist in the true answer
* if it does, compare if the information in attempt answer is consistent with what is in the true answer
* it is OK that not all information from true answer exist in attempt answer
* it is OK that attempt answer provides additional information that does not exist in the true answer
* it is OK that attempt answer are citing different sources, articles, websites than the true answer
Given:
## True Answer##
{reference}
## Attempt Answer##
{candidate}

## Task##
Work in a step by step way to make sure we get the right answer. You will format the output in json as follows:
 {{"reason": [{"sentence": "original sentence", "reason": "why this sentence is or is not consistent with the true answer"}],  "is_consistent" : true/false}}
Here is the evaluation in JSON format:

"""
