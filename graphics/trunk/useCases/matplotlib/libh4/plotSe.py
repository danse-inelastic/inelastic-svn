# this example uses matplotlib to plot se for hydrogen
from pylab import plot,array,savefig,xlabel,ylabel,legend,show
from os import sep
workingDirectory='/home/jbk/DANSE/inelastic/graphics/trunk/useCases/matplotlib/libh4'
#q,e,sqe,sqerr = cp.load(open("sqe.pkl",'r'))

fpure=file('Neat_LiBH4.dat')
fdesorbed=file('Desorbed_LiBH4.dat')
scale=2000
pure=[]
desorbed=[]
for line in fpure.readlines():
    parts=line.split()
    if parts!=[]:
        pure.append([float(parts[0]), float(parts[1])+8*scale])
    
for line in fdesorbed.readlines():
    parts=line.split()
    if parts!=[]:
        desorbed.append([float(parts[0]), float(parts[1])+10*scale])

fortho=file('orthorhombic/VASP.csv')
forthoCpmd=file('orthorhombic/CPMD.csv')
fhex=file('hexagonal/VASP.csv')
fborane=file('Li2B12H12/VASP.csv')
ortho=[]
orthoCpmd=[]
hex=[]
borane=[]

for line in (fortho.readlines())[3:]:
    parts=line.split(',')
    if parts!=[]:
        # the factor below converts from cm-1 to meV
        ortho.append([0.1240*float(parts[0]),scale*float(parts[9])+6*scale])
for line in (forthoCpmd.readlines())[3:]:
    parts=line.split(',')
    if parts!=[]:
        # the factor below converts from cm-1 to meV
        orthoCpmd.append([0.1240*float(parts[0]),scale*float(parts[9])+6*scale])
for line in (fhex.readlines())[3:]:
    parts=line.split(',')
    if parts!=[]:
        # the factor below converts from cm-1 to meV
        hex.append([0.1240*float(parts[0]),scale*float(parts[9])+4*scale])
for line in (fborane.readlines())[3:]:
    parts=line.split(',')
    if parts!=[]:
        # the factor below converts from cm-1 to meV
        borane.append([0.1240*float(parts[0]),scale*float(parts[9])+2*scale])


pure = array(pure)
desorbed=array(desorbed)
ortho=array(ortho)
orthoCpmd=array(orthoCpmd)
hex=array(hex)
borane=array(borane)

plot(pure[:,0], pure[:,1], desorbed[:,0], desorbed[:,1], ortho[:,0], ortho[:,1], hex[:,0], hex[:,1], borane[:,0], borane[:,1], linewidth=2.0)
legend(('pure','30% H2 desorbed','orthorhombic','hexagonal','Li2B12H12'))
#plot(pure[:,0], pure[:,1], desorbed[:,0], desorbed[:,1], linewidth=2.0)
#axis([0, 200,0,15000])
#legend(('90 K','70 K','35 K','10 K') )

x=xlabel('E (meV)')
x.set_fontsize(18)
y=ylabel('S(Q,E) (arbitrary units)')
y.set_fontsize(18)

show()
savefig(workingDirectory+sep+'vasp.png',dpi=300)


plot(pure[:,0], pure[:,1], orthoCpmd[:,0], orthoCpmd[:,1], linewidth=2.0)
legend(('pure','cpmd'))
#plot(pure[:,0], pure[:,1], desorbed[:,0], desorbed[:,1], linewidth=2.0)
#axis([0, 200,0,15000])
#legend(('90 K','70 K','35 K','10 K') )

x=xlabel('E (meV)')
x.set_fontsize(18)
y=ylabel('S(Q,E) (arbitrary units)')
y.set_fontsize(18)

show()
savefig(workingDirectory+sep+'cpmd.png',dpi=300)

