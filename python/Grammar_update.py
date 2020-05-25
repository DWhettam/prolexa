import sys; sys.version
import re
from nltk.stem import WordNetLemmatizer

sys.path.append("../python")
from POS_tagger import Tagger

PROLEXA_PATH = "../prolog/"

def isplural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural, lemma

def tag(text) :
    tagged_sent, sent, tags = Tagger().tag(text)
    return tags

def update_rules(text):
    tags = tag(text)
    print(tags)
    text = text.split(' ')
    start = ''
    end = ''
    f = open(PROLEXA_PATH + "prolexa_grammar.pl", "r")
    lines = f.readlines()
    f.close()
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
                if not (re.match(r"determiner\([a-z],X=>B,X=>H,\[\(H:-B\)\]\)(.*)", det_line)):
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
                plural, _ = isplural(input_word)
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
                if not (re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
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
                plural, lemma = isplural(input_word)
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
                if not (re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
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
                plural, lemma = isplural(input_word)
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
                if not (re.match(r"pred\((.*)[1],\[(.*)\]\)\.", noun_line)):
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
                plural, lemma = isplural(input_word)
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
                new_line = "proper_noun(s,{}) --> [{}].".format(input_word, input_word)
                lines.insert(det_idx, new_line)

    f = open(PROLEXA_PATH + "prolexa_grammar.pl", "w")
    lines = "".join(lines)
    f.write(lines)
    f.close()