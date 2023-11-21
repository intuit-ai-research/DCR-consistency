rai_summary_prompt = """
You are a good writer. You will be given:
* an article
* a list of objects, each have two fields: sentence and reason
    ** sentence: These sentences are summaries for the given article. 
    ** reason: These are the reasons why the sentence is consistent with the article or not.

Your job is to re-write these sentences:
* if the sentence is consistent with the article, you can keep it as it is
* if the sentence is not consistent with the article, you can re-write it to make it consistent with the article based on the reasons given.

## Article##
{article}

## Sentences ##
{sentences}


## Task##
Work in a step by step way to make sure we get the right answer. You will format the output in json as follows:
[{"sentence": "original sentence", "improved_sentence": "improved sentence", "reason": "if it is improved, how it is improved. if not, say 'ALREADY CONSISTENT'"}]



"""
