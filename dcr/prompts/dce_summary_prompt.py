dce_summary_prompt = """
You are an evaluator. You will be given a article and a summary.
Summary contains a summarized version of the article.
Criteria:
Your task is to evaluate whether the summary is consistent with the article. You will evaluate it by going through each sentence of the summary and check agains the following procedures:
* understands all the aspects in the sentence, who is doing what at when and where and what are the impact etc.
* compare if each aspects exist in the article
* if it does, compare if the information in this sentence is consistent with what is in the article
* compare if all the information in this sentence can be directly inferred or entailed from what is in the article, including but not limited to who, what, when, where etc.
* it is OK that not all information from article exist in this summary

Given:
## Article##
{reference}
## Summary##
{candidate}

## Task##
Work in a step by step way to make sure we get the right answer. You will format the output in json as follows:
 {{ "reason": [{"sentence": "original sentence", "reason": "why this sentence is or is not consistent with the article. You should start with \"this sentence is consistent with the article\" or \"this sentence is not consistent with the article\""}], "is_consistent" : true/false, }}
Here is the evaluation in JSON format:

"""
