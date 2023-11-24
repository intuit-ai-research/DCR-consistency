# DCR-Consistency
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)
[![License](https://img.shields.io/github/license/intuit/email-decomposer)](https://raw.githubusercontent.com/intuit/email-decomposer/master/LICENSE)
[![codecov](https://codecov.io/gh/intuit-ai-research/DCR-consistency/graph/badge.svg?token=IHBA2755W3)](https://codecov.io/gh/intuit-ai-research/DCR-consistency)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Inconsitency evalution and mitigation method described in the paper EVALUATING AND IMPROVING GENERATION CONSISTENCY OF LARGE LANGUAGE MODELS VIA A DIVIDE-CONQUER-REASONING APPROACH. It uses LLM as the method to detect and mitigate inconsistencies between a reference and a candidate. (TODO: add paper url)

## How to use
### Install 
(TODO: publish to pip)
```
pip install dcr-consistency
```
### Import
```
from dcr.evaluator import evaluate
from dcr.improver import improve
```

### Usage
#### Evaluation
```
res = evaluate(_your_LLM_, _your_model_config_, data, worker_count=5)
```
The `data` depends on the prompt used. By default each item should be a dict containting fields `id`, `reference` and `candidate`. The returned item will be the original data passed in joined with the columns below:

| column  | meaning   |
|-------------|:------------|
|  id | Unique Identifier for each row | 
|  score | Final consistency score of the row | 
| dce_reasons | Reaons for the final score given by DCE| 
| amc_reasons | Reaons for scoring of each sentence given by AMC | 
|  dce_raw | Raw data from DCE | 
| amc_raw | Raw data from AMC | 
|  decision | Consistency decision based on DCE | 

#### Inconsitency Mitigation
```
res = improve(_your_LLM_, _your_model_config_, data, worker_count=5)
```

The `data` depends on the prompt used. By default each item should be a dict containting fields `id`, `article` and `sentences`. `article` is the reference. `sentences` is a list illustrating whether each sentence is or is not consistent compared to the reference and the reasons. The returned item will be the original data passed in joined with the columns below:

| column  | meaning   |
|-------------|:------------|
|  id | Unique Identifier for each row | 
|  improved_version | The improved version where inconsistency is mitigated | 
| rai_raw | Raw data from RAI| 

### Contributing

See [CONTRIBUTING.md](https://github.com/intuit-ai-research/DCR-consistency/blob/main/CONTRIBUTING.md).



### Citation 

```
@inproceedings{zhang2023sac3,
      title={A Divide-Conquer-Reasoning Approach to Consistency Evaluation and Improvement in Blackbox Large Language Models},
      author={Wendi Cui, Jiaxin Zhang, Zhuohang Li, Damien Lopez, Kamalika Das, Bradley Malin, Sricharan Kumar},
      booktitle={NeurIPS 2023 Workshop on Socially Responsible Language Modelling Research},
      year={2023},
      primaryClass={cs.CL}
}
```
