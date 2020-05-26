from flair.data import Sentence
from flair.models import SequenceTagger
import re


class Tagger():
    def __init__(self) :
        self.tagger = SequenceTagger.load('pos')
    
    def tag(self, text):
        sentence = Sentence(text)

        # predict POS tags
        self.tagger.predict(sentence)
        tagged_sent = sentence.to_tagged_string()
        tags = re.findall(re.escape('<')+"(.*?)"+re.escape('>'),tagged_sent)

        return tagged_sent, sentence.to_plain_string(), tags

