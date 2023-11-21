amc_prompt = """
You are an evaluator. You will be given a list of paragraphs about "attempt answer". Your job is to:
* identify whether each paragraph is positive or negative
* if the paragraph  is positive, mark it as 1,
* if the paragraph  is negative, mark it as -1.
* output the mark for each paragraph  in a json array

# Example
Given paragraphs:
*"The attempt answer is incorrect as it states that employees in the US are not eligible to participate in the ESPP, which contradicts the true answer. So it is incorrect",  
*"The attempt answer adds a new aspect that is not in the true answer.",
*"Yet it does list the correct article.And that is helpful."

Thought: 
The first paragraph is negative as it mentions the attempt answer is wrong. Thus mark -1
The second paragraph is negative as it adds something that is not in true answer. Thus mark -1
The third paragraph is positive. Thus mark 1

Answer:
{"reason": ["The first paragraph is negative as it mentions the attempt answer is wrong. Thus mark -1", "The second paragraph is negative as it adds something that is not in true answer. Thus mark -1", "The third paragraph is positive. Thus mark +1"], "answer": [ -1, -1, 1]}

Given:
## Attempt Answer##:
{{attempt_answer}}

Answer:

"""
