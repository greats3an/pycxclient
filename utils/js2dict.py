'''
# Js2Dict Module

    Turns js varaibles into dictionaries
'''
import re,json
regex = r"(?:var|^)([^=!\n]*)(?:=)([^=].*)"

def js2dict(js):
    result = {}
    for matches in re.finditer(regex,js):
        key,value = matches.groups()
        key,value=key.strip(),value.strip()
        result[key] = value[:-1] if value[-1:] == ';' else value
    return result