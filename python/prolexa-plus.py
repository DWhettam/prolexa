# Adapted from Paul Brown's
# http://www.paulbrownmagic.com/blog/quick_gui.html

from argparse import ArgumentParser
from pyswip import Prolog
import meta_grammar as meta

swipl = Prolog()
swipl.consult("../prolog/prolexa.pl")



def main():
    meta.reset_grammar()
    parser = ArgumentParser(description="Hello! I'm ProlexaPlus! Tell me anything, ask me anything.")
    parser.add_argument("-o", "--input", required=True)
    args = parser.parse_args()
    print(meta.escape_and_call_prolexa(args.input))

if __name__ == "__main__":
    main()