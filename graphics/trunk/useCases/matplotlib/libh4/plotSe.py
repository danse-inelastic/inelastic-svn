# this example uses matplotlib to plot se for hydrogen
from pylab import plot,array,show
#from numpy import array
#import cPickle as cp
  
#q,e,sqe,sqerr = cp.load(open("sqe.pkl",'r'))

fpure=file('Neat_LiBH4.dat')
fdesorbed=file('Desorbed_LiBH4.dat')
pure=[]
desorbed=[]
for line in fpure.readlines():
    if line.split()!=[]:
        pure.append([float(x) for x in line.split()])
    
for line in fdesorbed.readlines():
    if line.split()!=[]:
        desorbed.append([float(x) for x in line.split()])

fortho=file('orthorhombic/VASP.csv')
fhex=file('hexagonal/VASP.csv')
fborane=file(')

#print pure[-2:]
#array(pure[-2:])
pure = array(pure)
desorbed=array(desorbed)
plot(pure[:,0], pure[:,1], desorbed[:,0], desorbed[:,1], linewidth=2.0)
#axis([-0.05, 50, 0, 9])
#legend(('90 K','70 K','35 K','10 K') )

#x=xlabel('E (meV)')
#x.set_fontsize(18)
#y=ylabel('S(Q,E) (arbitrary units)')
#y.set_fontsize(18)
#xlabels = getp(gca(), 'xticklabels')
#setp(xlabels, fontsize=20)
#ylabels = getp(gca(), 'yticklabels')
#setp(ylabels, fontsize=20)

show()

#savefig('/home/jbk/tex/graphiteKH2/plotSe.png',dpi=300)
#pl.savefig('/home/brandon/tex/graphiteKH2/msdNoK.png')
#pl.savefig('msdNoK.png')
