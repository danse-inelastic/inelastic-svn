twoAtomPotentialTypes={
'lennardJonesSigmaEpsilonGulp':{'mathematicalForm':"<html>E = "+G.epsilon+"(1/2("
                +G.sigma+"/r)<sup>12</sup> - 2("+G.sigma+"/r)<sup>6</sup>)</html>",
            'parameters':['epsilon','sigma'],
            'note':'from GULP documentation'},
'lennardJonesABGulp':{'mathematicalForm':"<html>E = A r<sup>-12</sup> - B r<sup>-6</sup></html>",
            'parameters':['A','B'],
            'note':'from GULP documentation when m = 12 and n = 6'},
'buckinghamGulp':{'mathematicalForm':"<html>E = A exp(-r/"+G.rho+") - C r<sup>-6</sup></html>",
            'parameters':['A','rho','C'],
            'note':'from GULP documentation'}, 
'harmonicGulp':{'mathematicalForm':"<html>E = 1/2 k<sub>2</sub>(r - r<sub>0</sub>)<sup>2</sup> "
            +"+ 1/6 k<sub>3</sub>(r - r<sub>0</sub>)<sup>3</sup> "
            + "+ 1/24 k<sub>4</sub>(r - r<sub>0</sub>)<sup>4</sup> "
            +"- C q<sub>i</sub>q<sub>j</sub>/r</html>",
            'parameters':['k2','r0','k3','k4','C'],
            'note':'from GULP documentation'},
'morseGulp':{'mathematicalForm':"<html>E = D{[1 - exp(-a(r - r<sub>0</sub>))]<sup>2</sup> - 1}</html>",
            'parameters':['D','a','r0'],
            'note':'from GULP documentation'}
}

threeAtomPotentialTypes={
'cosineGulp':{'mathematicalForm':"<html>E = k<sub>2</sub>(cos "+G.theta+" - cos "+G.theta
            +"<sub>0</sub>)<sup>2</sup></html>",'parameters':['k','theta0'],
            'note':'from GULP documentation'},
'threeBodyGulp':{'mathematicalForm':"<html>E = 1/2 k("+ G.theta + " - " + G.theta
            +"<sub>0</sub>)<sup>2</sup></html>",'parameters':['k','theta0'],
            'note':'from GULP documentation'}
}

fourAtomPotentialTypes={
'torsionGulp':{'mathematicalForm':"<html>E = k (1 + isign cos(n "
            +G.phi+" - "+G.phi+"<sub>0</sub>))", 'parameters':['k','isign','n'],
            'note':'from GULP documentation'},
'cosineGulp':{'mathematicalForm':"<html>E = k<sub>2</sub>(cos "+G.theta+" - cos "+G.theta
            +"<sub>0</sub>)<sup>2</sup></html>", 'parameters':['k2','theta0'],
            'note':'from GULP documentation'}
}