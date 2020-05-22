from pyswip import Prolog


def handle_utterance_str(text) :
    if text[0] != "'" and text[0] != '"' :
        text = f'"{text}"'
    
    text = text.replace('"', '\"')
    text = text.replace("'", '\"')
    
    return "handle_utterance(1,{},Output)".format(text)


def escape_and_call_prolexa(prolog, text) :
    libPrefix = "prolexa:"
    
    return prolog.query(libPrefix + handle_utterance_str(text))