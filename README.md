# DCR-Consistency: Evaluating and Improving Generation Consistency of Large Language Models via a Divide-Conquer-Reasoning Approach
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)
[![License](https://img.shields.io/github/license/intuit/email-decomposer)](https://raw.githubusercontent.com/intuit/email-decomposer/master/LICENSE)
[![codecov](https://codecov.io/gh/intuit-ai-research/DCR-consistency/graph/badge.svg?token=IHBA2755W3)](https://codecov.io/gh/intuit-ai-research/DCR-consistency)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### 🤔 What is DCR-Consistency
DCR-Consistency is a novel framework that uses LLM agents to detect and mitigate inconsistencies, or in other words hallucinations. It takes advantage of LLM's power in semantic understanding while circumventing known pitfalls such as relatively poor performance in math. Given a `reference` as the ground truth and a `candidate` to evaluate, it will output a numeric score between [-1, 1] indicating its consistency and a list of `reasons` about why this score is generated. Based on such `reasons`, it can also improve the `candidate` and mitigate detected inconsistencies. More details can be found in [our paper](_add_paper_url_)


### 🤖 Installation

      * python >= 3.9
      * Clone this repo and install with

```
pip install . 
```

DCR-Consistency can be installed directly from pip(coming soon!)
```
pip install dcr-consistency
```

### 🚀 Quickstart
The easiest way to start is to play with the example in `examples/example.py`

* Install the package with steps above
* Install the necessary packages with command below (example use additional dependencies such as openai):
```
pip install -r examples/requirements_example.txt
```
* update the `api_key` variable with your apikey.
* run the example with
```
python examples/example.py
```


### 📃 Usage
#### Evaluation
```
res = evaluate(_your_LLM_, _your_model_config_, data, worker_count=5)
```
The `data` depends on the prompt used. By default each item should be a dict containing fields `id`, `reference` and `candidate`. The returned item will be the original data passed in joined with the columns below:

| column  | meaning   |
|-------------|:------------|
|  id | Unique Identifier for each row | 
|  score | Final consistency score of the row | 
| dce_reasons | Reasons for the final score given by DCE| 
| amc_reasons | Reasons for scoring of each sentence given by AMC | 
|  dce_raw | Raw data from DCE | 
| amc_raw | Raw data from AMC | 
|  decision | Consistency decision based on DCE | 

#### Inconsistency Mitigation
```
res = improve(_your_LLM_, _your_model_config_, data, worker_count=5)
```

The `data` depends on the prompt used. By default each item should be a dict containing fields `id`, `article` and `sentences`. `article` is the reference. `sentences` is a list illustrating whether each sentence is or is not consistent compared to the reference and the reasons. The returned item will be the original data passed in joined with the columns below:

| column  | meaning   |
|-------------|:------------|
|  id | Unique Identifier for each row | 
|  improved_version | The improved version where inconsistency is mitigated | 
| rai_raw | Raw data from RAI| 

### 👏Contributing

See [CONTRIBUTING.md](https://github.com/intuit-ai-research/DCR-consistency/blob/main/CONTRIBUTING.md).



### 💁Citation 

```
@inproceedings{zhang2023sac3,
      title={A Divide-Conquer-Reasoning Approach to Consistency Evaluation and Improvement in Blackbox Large Language Models},
      author={Wendi Cui, Jiaxin Zhang, Zhuohang Li, Damien Lopez, Kamalika Das, Bradley Malin, Sricharan Kumar},
      booktitle={NeurIPS 2023 Workshop on Socially Responsible Language Modelling Research},
      year={2023},
      primaryClass={cs.CL}
}
```
