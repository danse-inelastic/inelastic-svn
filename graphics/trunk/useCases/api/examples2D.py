#!/usr/bin/env python

import glob, os, time
from graphics.numpytools import *
from scipy import linspace
from graphics.utils import *
from graphics.BackendModule import backend

#import sys
#backend = os.environ.get('easyviz_backend','vtk_') # vtk backend default
#legal_backends = 'vtk_ gnuplot_ pyx_ blt_'.split()
#if len(sys.argv) > 1:
#    if not sys.argv[1] in legal_backends:
#        print "no such backend as %s, using default (vtk_)" % sys.argv[1]
#    else:
#        backend = sys.argv[1]
#        sys.argv = sys.argv[:1] + sys.argv[2:]
#try:
#    exec('from graphics.%s import *' % backend)
#except:
#    print 'could not import backend %s' % backend
#    sys.exit(1)
from graphics.VtkBackend import *
#from graphics.MatplotlibBackend import *

def _test_figure():
    x=seq(-2,2,.1)
    plot(x**2, title="Plotting into figure 1: plot(x**2)")
    #f1=gcf()
    next(False, prompt, pause, psplot)
    
    figure(2)
    plot(x,x**3,'r', title="Plotting into figure 2: plot(x,x**3,'r')")
    #f2=gcf()
    next(False, prompt, pause, psplot)

    figure(1)
    plot(x,x,'r', title="Plotting into figure 1: plot(x,x)")

def _test_legend():
    x=seq(-2,2,.2)
    colors = 'r g b c m y k'.split()
    hold('on')
    for i in range(len(colors)):
        plot(x,x+i,'%s'%colors[i],legend='x+%d'%i)


def next(clear_figure=False, prompt='next plot', pause=0,
         save_hardcopy=False):
    if save_hardcopy:
        global hardcopy_counter
        hardcopy(filename='tmp_easyviz_plot%03d.ps' % hardcopy_counter,
                 color=True, fontname='Helvetica', fontsize=18)
        hardcopy_counter += 1
    if prompt:
        raw_input(prompt)
    if pause:
        time.sleep(pause)
    if clear_figure:
        clf()

def get_data(step=.1):
    x = seq(-2,2,step)
    xx,yy = meshgrid(x,x)
    zz = peaks(xx,yy)
    return xx,yy,zz    

def _tests(clear_figure, prompt, pause, psplot):

    _test_figure(); next(clear_figure, prompt, pause, psplot)
    
    if backend in ['vtk','matplotlib']:
        # why is the streamribbon object still present in ax.plotitems???
        #gca()._prop['plotitems'] = []
        _test_legend(); next(clear_figure, prompt, pause, psplot)
    
if __name__ == '__main__':
    # command-line arguments: n screenplot flash psplot
    # screenplot: show plots on the screen?
    # flash: drop prompt between plots and clf, everything goes into one plot
    # psplot: make hardcopy of each plot?

    # 1 0 1 1 gives execution in batch without user interaction
    
    import sys
    global hardcopy_counter, clear_figure, prompt, pause, psplot, screenplot
    try: n = int(sys.argv[1])
    except: n = 1
    try: screenplot = bool(int(sys.argv[2]))
    except: screenplot = True
    try: flash = bool(int(sys.argv[3]))
    except: flash = True
    try: psplot = bool(int(sys.argv[4]))
    except: psplot = True

    hardcopy_counter = 0
    if flash:
        # let all plots flash on the screen with 1 s pause
        clear_figure = False
        prompt = ''
        pause = 2
    else:
        # press return for each plot on the screen
        clear_figure = False
        prompt = 'next test'
        pause = 0
    #_tests(clear_figure, prompt, pause, psplot)
    _tests(True, prompt, pause, psplot)
