
# this example uses matplotlib to print msd plots for hydrogen
# and potassium in K-intercalated graphite 
from pylab import *

#def f(t):
#    s1 = cos(2*pi*t)
#    e1 = exp(-t)
#    return multiply(s1,e1)

def line1(x):
    return 1.48016 - 108.212*x
def line2(x):
    return -3.66886 - 3.62623*x
tData=array([0.4, 0.2, 0.133333, 0.1, 0.0666667, 0.0571429, 0.05, 0.04, \
       0.0333333, 0.0285714, 0.0222222, 0.0142857, 0.0111111])
dData=array([-5.04705, -4.57569, -4.01732, -4.17176, -4.0862, -3.7889, -3.64719, \
-3.16885, -2.09907, -1.10854, -0.939989, -0.0563887, 0.0735621])

#print 'got here',tData,dData
#plot(tData, dData)
plot(tData, dData, 'bo', tData, line1(tData),'b-', tData, line2(tData),'b-',linewidth=2.0)
axis([-0.05, 0.5, -5.4, 0.2])
#legend(('90 K','70 K','35 K','10 K') )

x=xlabel('1/T (1/K)')
x.set_fontsize(18)
y=ylabel('D (Ang^2 /invcm)')
y.set_fontsize(18)
xlabels = getp(gca(), 'xticklabels')
setp(xlabels, fontsize=20)
ylabels = getp(gca(), 'yticklabels')
setp(ylabels, fontsize=20)

#show()

savefig('/home/jbk/tex/graphiteKH2/diffusionConstantVsT.png',dpi=300)
#pl.savefig('/home/brandon/tex/graphiteKH2/msdNoK.png')
#pl.savefig('msdNoK.png')
