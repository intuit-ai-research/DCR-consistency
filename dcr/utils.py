from math import ceil


def get_final_prompt(prompt, **input_values):
    for key in input_values:
        if isinstance(input_values[key], str):
            prompt = prompt.replace(f"{{{key}}}", input_values[key])
    return prompt


def divide_input(input_list, worker_count):
    l = len(input_list)
    stride = ceil(l / worker_count)
    input_divided = [
        input_list[i * stride : (i + 1) * stride] for i in range(0, worker_count)
    ]
    return input_divided
