import sys; sys.version
import re
from nltk.stem import WordNetLemmatizer

sys.path.append("../python")
from POS_tagger import Tagger

PROLEXA_PATH = "../prolog/"


def reset_grammar() :
    lines = get_prolog_grammar(PROLEXA_PATH, original=True)
    write_new_grammar(PROLEXA_PATH, lines)


def lemmatise(word) :
    wnl = WordNetLemmatizer()
    
    return wnl.lemmatize(word, 'n')


def is_plural(word):
    lemma = lemmatise(word)
    plural = True if word is not lemma else False
    return plural, lemma


def handle_utterance_str(text) :
    if text[0] != "'" and text[0] != '"' :
        text = f'"{text}"'
    
    text = text.replace('"', '\"')
    text = text.replace("'", '\"')
    
    return "handle_utterance(1,{},Output)".format(text)


def standardised_query(pl, text) :
    text = contractions.fix(text)
    text = lemmatise(text)
    _, _, tags = tagger.tag(text)
    tags = standardise_tags(tags)
    #return escape_and_call_prolexa(pl, text)
    return tags, text


# for queries, not knowledge loading
def standardise_tags(tags) :
    std = []
    for tag in tags :
        if POS.VERB.value in tag :
            std.append( POS.VERB.value)
        if POS.ADVERB.value in tag :
            std.append( POS.ADVERB.value)
        if POS.ADJECTIVE.value in tag :
            std.append( POS.ADJECTIVE.value)
        if POS.NOUN.value in tag and tag != POS.PROPNOUN.value :
            std.append( POS.NOUN.value)
        if tag == POS.PROPNOUN.value :
            std.append(POS.PROPNOUN.value)
    return std
    

def get_tags(tagger, text) :
    _, _, tags = tagger.tag(text)
    tags = standardise_tags(tags)
    return tags


def get_prolog_grammar(path, original=False) :
    if original :
        file = "prolexa_grammar_base.pl"
    else :
        file = "prolexa_grammar.pl"
    
    f = open(path + file, "r")
    lines = f.readlines()
    f.close()
    
    return lines


def write_new_grammar(path, lines) :
    f = open(path + "prolexa_grammar.pl", "w")
    lines = "".join(lines)
    f.write(lines)
    f.close()
    
    
def handle_determiner(text, tags) :
    start = '--> ['
    end = ']'
    exists = False
    input_word = text[tags.index('DT')]
    for det_idx, det_line in enumerate(lines[idx:]):                                                
        if not(re.match(r"determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)", det_line)):
            det_idx = det_idx + idx   
            if tags:
                tags.remove('DT')
            if text:
                text.remove(input_word)
            break
        line_word = (det_line.split(start))[1].split(end)[0]  
        if input_word == line_word:                    
            exists = True
            if tags:
                tags.remove('DT')
            if text:
                text.remove(input_word)
            break 

    if not exists:
        plural, _ = is_plural(input_word)
        if plural:
            new_line = "determiner(p,X=>B,X=>H,[(H:-B)]) --> [{}].\n".format(input_word) 
        else:
            new_line = "determiner(s,X=>B,X=>H,[(H:-B)]) --> [{}].\n".format(input_word) 
        lines.insert(det_idx, new_line)


def update_rules(tagger, text):
    text = text.lower()
    tags = get_tags(tagger, text)
    print(tags)
    text = text.split(' ')
    start = ''
    end = ''
    lines = get_prolog_grammar(PROLEXA_PATH)
    myiter = iter(lines)
    
    for idx, line in enumerate(myiter):
        if not text:
            break
        
        if ('DT' in tags) and re.match(r"determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)", line):
            start = '--> ['
            end = ']'
            exists = False
            input_word = text[tags.index('DT')]
            for det_idx, det_line in enumerate(lines[idx:]):                                                
                if not(re.match(r"determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)", det_line)):
                    det_idx = det_idx + idx   
                    if tags:
                        tags.remove('DT')
                    if text:
                        text.remove(input_word)
                    break
                line_word = (det_line.split(start))[1].split(end)[0]  
                if input_word == line_word:                    
                    exists = True
                    if tags:
                        tags.remove('DT')
                    if text:
                        text.remove(input_word)
                    break 

            if not exists:
                plural, _ = is_plural(input_word)
                if plural:
                    new_line = "determiner(p,X=>B,X=>H,[(H:-B)]) --> [{}].\n".format(input_word) 
                else:
                    new_line = "determiner(s,X=>B,X=>H,[(H:-B)]) --> [{}].\n".format(input_word) 
                lines.insert(det_idx, new_line)

                    
        if ('NN' in tags) and re.match(r"pred\((.*)[1],\[(.*)\]\)\.", line): 
            start = 'pred('
            end = ', '
            exists = False
            new_line = ''
            input_word = text[tags.index('NN')]
            for noun_idx, noun_line in enumerate(lines[idx:]):
                if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
                    noun_idx = noun_idx + idx   
                    if tags:
                        tags.remove('NN')
                    if text:
                        text.remove(input_word)
                    break
                line_word = (noun_line.split(start))[1].split(end)[0]
                if input_word == line_word:
                    if (re.match(r"pred\((.*)[1](.*)n\/(.*)\]\)\.", noun_line)):
                        exists = True
                        if tags:
                            tags.remove('NN')
                        if text:
                            text.remove(input_word)
                        break
                    else:
                        noun_idx = noun_idx + idx
                        insert_idx = noun_line.index(']).')
                        new_line = noun_line[:insert_idx] + ',n/' + input_word + noun_line[insert_idx:]
                        lines[noun_idx] = new_line
                        exists = True
                        if tags:
                            tags.remove('NN')
                        if text:
                            text.remove(input_word)
                        break

            if not exists:
                plural, lemma = is_plural(input_word)
                if plural:
                    input_word = lemma
                if new_line == '':
                    new_line = 'pred(' + input_word + ', 1,[n/' + input_word + ']).\n'
                lines.insert(noun_idx, new_line)
                
                
        if ('JJ' in tags) and re.match(r"pred\((.*)[1],\[(.*)\]\)\.", line): 
            start = 'pred('
            end = ', '
            exists = False
            new_line = ''
            input_word = text[tags.index('JJ')]
            for noun_idx, noun_line in enumerate(lines[idx:]):
                if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
                    noun_idx = noun_idx + idx   
                    if tags:
                        tags.remove('JJ')
                    if text:
                        text.remove(input_word)
                    break
                line_word = (noun_line.split(start))[1].split(end)[0]
                if input_word == line_word:
                    if (re.match(r"pred\((.*)[1](.*)a\/(.*)\]\)\.", noun_line)):
                        exists = True
                        if tags:
                            tags.remove('JJ')
                        if text:
                            text.remove(input_word)
                        break
                    else:
                        noun_idx = noun_idx + idx
                        insert_idx = noun_line.index(']).')
                        new_line = noun_line[:insert_idx] + ',a/' + input_word + noun_line[insert_idx:]
                        lines[noun_idx] = new_line
                        exists = True
                        if tags:
                            tags.remove('JJ')
                        if text:
                            text.remove(input_word)
                        break

            if not exists:
                plural, lemma = is_plural(input_word)
                if plural:
                    input_word = lemma
                if new_line == '':
                    new_line = 'pred(' + input_word + ', 1,[a/' + input_word + ']).\n'
                lines.insert(noun_idx, new_line)
                
        if ('VB' in tags) and re.match(r"pred\((.*)[1],\[(.*)\]\)\.", line): 
            start = 'pred('
            end = ', '
            exists = False
            new_line = ''
            input_word = text[tags.index('VB')]
            for noun_idx, noun_line in enumerate(lines[idx:]):
                if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
                    noun_idx = noun_idx + idx   
                    if tags:
                        tags.remove('VB')
                    if text:
                        text.remove(input_word)
                    break
                line_word = (noun_line.split(start))[1].split(end)[0]
                if input_word == line_word:
                    if (re.match(r"pred\((.*)[1](.*)v\/(.*)\]\)\.", noun_line)):
                        exists = True
                        if tags:
                            tags.remove('VB')
                        if text:
                            text.remove(input_word)
                        break
                    else:
                        noun_idx = noun_idx + idx
                        insert_idx = noun_line.index(']).')
                        new_line = noun_line[:insert_idx] + ',v/' + input_word + noun_line[insert_idx:]
                        lines[noun_idx] = new_line
                        exists = True
                        if tags:
                            tags.remove('VB')
                        if text:
                            text.remove(input_word)
                        break
            if not exists:
                plural, lemma = is_plural(input_word)
                if plural:
                    input_word = lemma
                if new_line == '':
                    new_line = 'pred(' + input_word + ', 1,[v/' + input_word + ']).\n'
                lines.insert(noun_idx, new_line)
                        
        if ('NNP' in tags) and re.match(r"proper_noun\(s(.*) -->(.*)\]\.", line):
            start = '--> ['
            end = ']'
            exists = False
            input_word = text[tags.index('NNP')]
            for det_idx, det_line in enumerate(lines[idx:]):                                                
                if not(re.match(r"proper_noun\(s(.*) -->(.*)\]\.", det_line)):
                    det_idx = det_idx + idx   
                    if tags:
                        tags.remove('NNP')
                    if text:
                        text.remove(input_word)
                    break
                line_word = (det_line.split(start))[1].split(end)[0]  
                if input_word == line_word:                    
                    exists = True
                    if tags:
                        tags.remove('NNP')
                    if text:
                        text.remove(input_word)
                    break 

            if not exists:             
                new_line = "proper_noun(s,{}) --> [{}].\n".format(input_word, input_word) 
                lines.insert(det_idx, new_line)        
 
    print([line for line in lines if "Dan" in line])
    write_new_grammar(PROLEXA_PATH, lines)



def escape_and_call_prolexa(pl, text) :
    libPrefix = "prolexa:"
    update_rules(tagger, text)
    return ''
    
    #pl.consult(PROLEXA_PATH + "prolexa.pl")
    #return pl.query(libPrefix + handle_utterance_str(text))

