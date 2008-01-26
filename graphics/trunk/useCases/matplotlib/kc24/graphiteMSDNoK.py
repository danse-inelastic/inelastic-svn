
# this example uses matplotlib to print msd plots for hydrogen
# and potassium in K-intercalated graphite 
from graphics.Matplotlib import pylab
pl = pylab()

def getPlotData(name):
    '''extracts data from file.plot'''
    f=file(name,'r')
    lines=f.readlines()
    f.close()
    xAxis=[];yAxis=[]
    for l in lines:
        if len(l)==0: continue
        if l[0]=='#': continue
        x,y=l.split()
        xAxis.append(float(x));yAxis.append(float(y))
    return xAxis,yAxis

x0,y0=getPlotData('MSD_dlpolyGraphite6x3sup90K50ps.plot')
x1,y1=getPlotData('MSD_dlpolyGraphite6x3sup70K50ps.plot')
x2,y2=getPlotData('MSD_dlpolyGraphite6x3sup35K50ps.plot')
x3,y3=getPlotData('MSD_dlpolyGraphite6x3sup10K50ps.plot')

lines=pl.plot(x0,y0,'k-',x1,y1,'k-.',x2,y2,'y--',x3,y3,'c--',linewidth=2.0)
pl.axis([0, 50, 0, 500])
#setp(lines, linewidth=2.0)
#pl.xticklabels(fontsize=20)
#pl.yticklabels(fontsize=20)
x=pl.xlabel('Time (ps)')
x.set_fontsize(18)
y=pl.ylabel('MSD (squared angstroms)')
#y=pl.ylabel(r'$\rm{MSD (}Ang^2\rm{)}$')
y.set_fontsize(18)
l=pl.legend(('90 K','70 K','35 K','10 K') )
pl.legend.pad=0.5
pl.legend.axespad=1.0
legText=l.get_texts()
for t in legText:
    t.set_fontsize(16)
#pl.title('hydrognen')
#pl.show()


#pl.savefig('/home/jbk/tex/graphiteKH2/msdNoK.eps',dpi=600)
pl.savefig('/home/jbk/tex/graphiteKH2/msdNoK.tiff')
pl.savefig('msdNoK.png')
