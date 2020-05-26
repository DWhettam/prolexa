from cmd import Cmd
from pyswip import Prolog
import meta_grammar as meta
import os 
import warnings
warnings.filterwarnings("ignore")


if os.getcwd().split("/")[-1] != "python" :
    os.chdir("python/")

    
pl = Prolog()

class ProlexaPlus(Cmd) :
    intro = "Hello! I'm ProlexaPlus! Tell me anything, ask me anything."
    prompt = "pp: "
    file = None
    
    def default(self, input_): 
        firstAnswer = meta.standardised_query(pl, input_)[0]['Output']
        print( firstAnswer )
        



if __name__ == "__main__":
    meta.reset_grammar()
    ProlexaPlus().cmdloop()