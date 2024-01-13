PROMPT_NAME_FORMATTER = """
请将提供的名字，在保留原有含义的情况下，改写成{{ length }}个{{ language }}以内的新名字，使得更易读易懂，且不包含任何特殊字符，可以保留数字。

原名字：{{ name }}

返回格式：
{'new_name': [new name]}

"""
