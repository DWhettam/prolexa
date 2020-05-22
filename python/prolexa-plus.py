# Adapted from Paul Brown's
# http://www.paulbrownmagic.com/blog/quick_gui.html

from argparse import ArgumentParser
from pyswip import Prolog
from prolexa_pyswip import escape_and_call_prolexa

swipl = Prolog()
swipl.consult("../prolog/prolexa.pl")



def main():
    parser = ArgumentParser(description="Hello! I'm ProlexaPlus! Tell me anything, ask me anything.")
    parser.add_argument("-o", "--input", required=True)
    args = parser.parse_args()
    print(escape_and_call_prolexa(args.input))

if __name__ == "__main__":
    main()