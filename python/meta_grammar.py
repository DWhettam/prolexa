import sys; sys.version
import re, string
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')
import contractions
from enum import Enum

sys.path.append("../python")
from POS_tagger import Tagger

PROLEXA_PATH = "../prolog/"

tagger = Tagger()


PROLOG_DET_REGEX = r"determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)"
PROLOG_DET = "determiner(p,X=>B,X=>H,[(H:-B)]) --> [{}].\n"


# PartsOfSpeech
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
class POS(Enum) :
    DETERMINER = "DT"
    ADVERB = "RB"
    PROPNOUN = "NNP"
    PROPNOUN_2 = "PROPN"
    NOUN = "NN"
    VERB = "VB"
    ADJECTIVE = "JJ"
    PREPOSITION = "IN"
    COORD = "CC"
    CARDINAL = "CD"
    EXISTENTIAL = "EX"
    FOREIGN = "FW"
    LISTITEM = "LS"
    MODAL = "MD"
    PREDET = "PDT"
    POSSESS = "POS"
    PRONOUN = "PRP"
    POSSPRONOUN = "PRP$"
    PARTICLE = "RP"
    SYMBOL = "SYM"
    TO = "TO"
    INTERJECTION = "UH"
    WHDET = "WDT"
    WHPRONOUN = "WP"
    WHADVERB = "WRB"


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


def remove_punctuation(s) :
    return s.translate(str.maketrans('', '', string.punctuation))


def standardised_query(pl, text) :
    text = remove_punctuation(text)
    text = contractions.fix(text)
    text = lemmatise(text)

    return escape_and_call_prolexa(pl, text)


# for queries, not knowledge loading
def standardise_tags(tags) :
    std = []
    for tag in tags :
        if POS.DETERMINER.value in tag :
            std.append( POS.DETERMINER.value)
        elif POS.VERB.value in tag :
            std.append( POS.VERB.value)
        elif POS.ADVERB.value in tag :
            std.append( POS.ADVERB.value)
        elif POS.ADJECTIVE.value in tag :
            std.append( POS.ADJECTIVE.value)
        elif POS.NOUN.value in tag and tag != POS.PROPNOUN.value :
            std.append( POS.NOUN.value)
        else :
            std.append(tag)
    
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


def escape_and_call_prolexa(pl, text) :
    libPrefix = "prolexa:"
    update_rules(tagger, text)
    pl.consult(PROLEXA_PATH + "prolexa.pl")
    generator = pl.query(libPrefix + handle_utterance_str(text))
    
    return list(generator)

        
def handle_noun(lines, i, text, tags) :
    nn = POS.NOUN.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(nn)]
    _, input_word = is_plural(input_word)
    text[tags.index(nn)] = input_word
    
    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
            noun_idx = noun_idx + i   
            if tags:
                tags.remove(nn)
            if text:
                text.remove(input_word)
            break
        
        line_word = (noun_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            if (re.match(r"pred\((.*)[1](.*)n\/(.*)\]\)\.", noun_line)):
                exists = True
                if tags:
                    tags.remove(nn)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = noun_line[:insert_idx] + ',n/' + input_word + noun_line[insert_idx:]
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(nn)
                if text:
                    text.remove(input_word)
                break

    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[n/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)
    
    return lines


def handle_adjective(lines, i, text, tags) :
    a = POS.ADJECTIVE.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(a)]
    _, input_word = is_plural(input_word)
    text[tags.index(a)] = input_word
    
    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
            noun_idx = noun_idx + i   
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
                    tags.remove(a)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = noun_line[:insert_idx] + ',a/' + input_word + noun_line[insert_idx:]
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(a)
                if text:
                    text.remove(input_word)
                break

    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[a/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)

    return lines


def handle_verb(lines, i, text, tags) :
    v = POS.VERB.value
    start = 'pred('
    end = ', '
    exists = False
    new_line = ''
    input_word = text[tags.index(v)]
    _, input_word = is_plural(input_word)
    text[tags.index(v)] = input_word
    
    for noun_idx, noun_line in enumerate(lines[i:]):
        if not(re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
            noun_idx = noun_idx + i   
            if tags:
                tags.remove(v)
            if text:
                text.remove(input_word)
            break
        
        line_word = (noun_line.split(start))[1].split(end)[0]
        if input_word == line_word:
            if (re.match(r"pred\((.*)[1](.*)v\/(.*)\]\)\.", noun_line)):
                exists = True
                if tags:
                    tags.remove(v)
                if text:
                    text.remove(input_word)
                break
            else:
                noun_idx = noun_idx + i
                insert_idx = noun_line.index(']).')
                new_line = noun_line[:insert_idx] + ',v/' + input_word + noun_line[insert_idx:]
                lines[noun_idx] = new_line
                exists = True
                if tags:
                    tags.remove(v)
                if text:
                    text.remove(input_word)
                break
    
    if not exists:
        if new_line == '':
            new_line = 'pred(' + input_word + ', 1,[v/' + input_word + ']).\n'
        lines.insert(noun_idx, new_line)
        
    return lines


def handle_proper_noun(lines, i, text, tags) :
    prop = POS.PROPNOUN.value
    start = '--> ['
    end = ']'
    exists = False
    input_word = text[tags.index(prop)]
    for det_idx, det_line in enumerate(lines[i:]):                                                
        if not(re.match(r"proper_noun\(s(.*) -->(.*)\]\.", det_line)):
            det_idx = det_idx + i   
            if tags:
                tags.remove(prop)
            if text:
                text.remove(input_word)
            break
        line_word = (det_line.split(start))[1].split(end)[0]  
        if input_word == line_word:                    
            exists = True
            if tags:
                tags.remove(prop)
            if text:
                text.remove(input_word)
            break 

    if not exists:             
        new_line = "proper_noun(s,{}) --> [{}].\n".format(input_word, input_word) 
        lines.insert(det_idx, new_line)      

    return lines


def update_rules(tagger, text):
    text = text.lower()
    tags = get_tags(tagger, text)
    # Handle extra whitespace
    text = ' '.join(text.split()) \
                .split(' ')
    start = ''
    end = ''
    lines = get_prolog_grammar(PROLEXA_PATH)
    
    for idx, line in enumerate(iter(lines)):
        if not text:
            break

        pred_match = r"pred\((.*)[1],\[(.*)\]\)\."
        
        if (POS.NOUN.value in tags) and re.match(pred_match, line):            
            lines = handle_noun(lines, idx, text, tags)
        
        if (POS.ADJECTIVE.value in tags) and re.match(pred_match, line): 
            lines = handle_adjective(lines, idx, text, tags)
                
        if (POS.VERB.value in tags) and re.match(pred_match, line):
            lines = handle_verb(lines, idx, text, tags)
        
        prop_match = r"proper_noun\(s(.*) -->(.*)\]\."
        
        if (POS.PROPNOUN.value in tags) and re.match(prop_match, line):
            lines = handle_proper_noun(lines, idx, text, tags)
    
    write_new_grammar(PROLEXA_PATH, lines)
