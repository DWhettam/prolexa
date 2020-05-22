from flair.data import Sentence
from flair.models import SequenceTagger
import re


class Tagger():
    def tag(self, text):
        tagger = SequenceTagger.load('pos')

        sentence = Sentence(text)

        # predict POS tags
        tagger.predict(sentence)
        tagged_sent = sentence.to_tagged_string()
        tags = re.findall(re.escape('<')+"(.*?)"+re.escape('>'),tagged_sent)

        return tagged_sent, sentence.to_plain_string(), tags

