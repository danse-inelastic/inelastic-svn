
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

x1,y1=getPlotData('MSD_dlpolyGraphite6x3sup70K50ps.plot')
x2,y2=getPlotData('MSD_dlpolyGraphite6x3sup35K50ps.plot')
x3,y3=getPlotData('MSD_dlpolyGraphite6x3sup10K50ps.plot')
x4,y4=getPlotData('MSD_dlpolyGraphite6x3sup70K50psK.plot')
x5,y5=getPlotData('MSD_dlpolyGraphite6x3sup35K50psK.plot')
x6,y6=getPlotData('MSD_dlpolyGraphite6x3sup10K50psK.plot')

pl.subplot(121)
pl.plot(x1,y1,'k-',x2,y2,'y--',x3,y3,'c--')
pl.axis([0, 50, 0, 260])
pl.xlabel('Time (ps)')
pl.ylabel(r'$\rm{MSD}\,\,\,(\AA^2)$')
pl.legend(('70 K','35 K','10 K') )
pl.legend.pad=0.5
pl.legend.axespad=1.0
pl.title('Hydrogen')

pl.subplot(122)
pl.plot(x4,y4,'k-',x5,y5,'y--',x6,y6,'c--')
pl.axis([0, 50, 0, 260])
pl.xlabel('Time (ps)')
pl.title('Potassium')
pl.legend(('70 K','35 K','10 K') )
pl.legend.pad=0.5
#pl.show()


#pl.savefig('/home/brandon/tex/graphiteKH2/msd.eps',dpi=600)
pl.savefig('/home/brandon/tex/graphiteKH2/msd.png')
