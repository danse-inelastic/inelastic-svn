
# this example uses matplotlib to print msd plots for hydrogen
# and potassium in K-intercalated graphite 
from pylab import *
from numpy import *

#def f(t):
#    s1 = cos(2*pi*t)
#    e1 = exp(-t)
#    return multiply(s1,e1)

def line1(x):
    return 1.42746 - 106.498*x
def line2(x):
    return -3.66886 - 3.62623*x
tData=array([0.4, 0.2, 0.133333, 0.1, 0.0666667, 0.0571429, 0.05, 0.04, \
       0.0333333, 0.0285714, 0.0222222, 0.0142857, 0.0111111, 0.00833333, 0.00714286])
dData=array([0.00642828286859, 0.0102991941666, 0.0180010589427, 0.0154250125336, 0.0168029103438, 0.0226204282544, 0.0260643951607, 0.042051928911, 0.122570219603, 
 0.330040589947, 0.390631979844, 0.945171714087, 1.07633542493, 1.71587262385, 1.83457323925])
            

#print 'got here',tData,dData
#plot(tData, dData)
plot(tData, log(dData), 'bo', tData, line1(tData),'b-', tData, line2(tData),'b-',linewidth=2.0)
axis([-0.05, 0.5, -5.4, 0.2])
#legend(('90 K','70 K','35 K','10 K') )

x=xlabel('1/T (1/K)')
x.set_fontsize(18)
y=ylabel('D (Ang^2 / ps)')
y.set_fontsize(18)
xlabels = getp(gca(), 'xticklabels')
setp(xlabels, fontsize=20)
ylabels = getp(gca(), 'yticklabels')
setp(ylabels, fontsize=20)

show()

savefig('/home/jbk/tex/graphiteKH2/diffusionConstantVsT.png',dpi=300)
#pl.savefig('/home/brandon/tex/graphiteKH2/msdNoK.png')
#pl.savefig('msdNoK.png')
