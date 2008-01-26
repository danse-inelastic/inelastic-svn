from graphics.Matplotlib import pylab

publish=False

def twoColumnFile(name,format='float'):
    '''reads a two-column file and returns two variables with the values 
in the file

The format argument can be set to 'float', 'string', or 'int'.'''
    f=file(name,'r')
    lines=f.readlines()
    xCol=[];yCol=[]
    for line in lines:
        #ignore anything that is commented or that is not two strings
        if len(line)==0: continue
        if line[0]=='#': continue
        items=line.split()
        if len(items)!=2: continue
        x,y=items
        if format=='float':
            xCol.append(float(x));yCol.append(float(y))
        elif format=='string':
            xCol.append(x);yCol.append(y)
        elif format=='int':
            xCol.append(int(x));yCol.append(int(y))
    return xCol,yCol

x,y=twoColumnFile('MSD_dlpolyGraphite6x3sup70K50ps.plot')
pl = pylab()
pl.plot(x,y)
pl.xlabel('time (ps)')
pl.ylabel('distance (nm)')
pl.show()
if publish:
    pl.savefig('MSD_dlpolyGraphite6x3sup70K50ps.eps',dpi=600)
#eventually do the other two simulations and compare

x,y=twoColumnFile('DOS_dlpolyGraphite6x3sup70K50ps.plot')
pl.plot(x,y)
pl.xlabel('frequency (1/cm)')
pl.ylabel('counts (arbitrary units)')
pl.show()
if publish:
    pl.savefig('DOS_dlpolyGraphite6x3sup70K50ps.eps',dpi=600)
