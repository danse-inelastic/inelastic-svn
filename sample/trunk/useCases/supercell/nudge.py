name='aabbccGraphite.xyz'
f=file(name)
f2=file(name+'.nudged','w')

numAtoms=int(f.readline())
f.readline()
for i in range(numAtoms):
    at,x,y,z=f.readline().split()
    f2.write('  %s        %.5f        %.5f        %.5f\n' % (at,float(x)+0.02100,float(y)+0.00400,float(z)))
    