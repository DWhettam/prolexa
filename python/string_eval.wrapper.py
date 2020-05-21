## String eval methods

from pyswip import Prolog

pl = Prolog()
pl.assertz("father(michael,john)")
pl.assertz("father(michael,gina)")
pl = Prolog()

for soln in pl.query("father(X,Y)"):
    print(soln["X"], "is the father of", soln["Y"])

# michael is the father of john
# michael is the father of gina

childrenOfMichael = pl.query("father(michael,X)")
print( list(childrenOfMichael) )
