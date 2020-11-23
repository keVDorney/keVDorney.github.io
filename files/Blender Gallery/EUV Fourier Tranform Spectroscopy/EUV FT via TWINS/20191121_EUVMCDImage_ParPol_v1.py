import os, sys, glob
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import BlBuW_colormap as bbw
import colorsys

############ COMMENTS ##############
''' Computing images for rendering a movie of the FT part of TFS.
'''

# Set fontsize of ticklabels globally for 128 dpi display.
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
####################################

####### SECTION STATEMENTS #########
Sinusoid  = False # If TRUE, toggles an intensity grating on top of the Gaussian beam.
MultiS    = False # IF TRUE, computes intensity grating assuming multiple harmonics.
FSinusoid = True # IF True, toggles a section of code where we fake it til' we make it.
ShowPlots = False # Toggles plt.show() on/off in a global fashion.
Testing   = False # Toggles a section of code for testing porpoises.
####################################

######## "GLOBAL" PARAMETERS #######

####################################

######### HELPER FUNCTIONS #########
def _gaussian2D(x, y, ax, ay, cx, cy, wx, wy):
    return ax*np.exp(-((x-cx)**2/wx**2)) + ay*np.exp(-((y-cy)**2/wy**2))

def _gaussian(x, y, amp, width):
    return amp * np.exp(-((x**2+y**2)/width**2))

def _gaussianc(x, amp, width, center):
    return amp * np.exp(-(((x-center)**2)/width**2))

def _RGBcolors(N, sat=1.0, light=1.0):
    # Generates a len(N) list of RGB tuples evenly spaced across the RGB color spectrum.
    # N - Number of points.
    # sat - Saturation of HSV colors. 0.0 to 1.0
    # light - Lightness of HSV colors. 0.0 to 1.0

    HSV_tuples = [(x*1.0/N, sat, light) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

    return RGB_tuples
####################################

########### BEGIN CODE #############

# Make figure.
fig, ax = plt.subplots(1, 1, figsize=(3, 3), dpi=128)
fig.subplots_adjust(left=0, right=1.0, bottom=0, top=1.0)

# Create Gaussian background.
c, r = np.arange(-250, 251, 1), np.arange(-250, 251, 1)
X, Y = np.meshgrid(c, r)
# G = _gaussian2D(X, Y, 1, 1, 0, 0, 10, 10)
G   = _gaussian(X, Y, 1, 250)
G   = G  / np.max(G)
d0  = 235
lam = (1239/55)*1e-3
L   = 120*1e4
harm = 7
nharms = 3

if Sinusoid == True:
    if MultiS == True:
        S = np.zeros(shape=np.shape(G))
        for n in np.arange(0, 2*nharms+2, 2):
            lam = (1239/(790/(harm+n)))*1e-3
            print(harm+n)
            top = 2*np.pi*X*d0
            bot = L*lam
            print(2*np.pi*d0*100/bot)
            # G = G*np.cos(top/bot)
            # S = S + G*np.cos(top/bot)
            S = S + G*np.cos(X*(n+1)/10)
            # S = S + (np.sin(X*(n+1))/np.sin(X))**2
            # S = S + (np.cos(X*(n+1)/10))
            print(np.max(S))


    else:
        S = G + 0.1 * np.sin(X/6)**2
    G = G / np.max(G)

if FSinusoid == True:

    c, r = np.arange(-250, 251, 1), np.arange(-250, 251, 1)
    X, Y = np.meshgrid(c, r)
    # G = _gaussian2D(X, Y, 1, 1, 0, 0, 10, 10)
    # G   = _gaussian(X, Y, 1, 150)

    # Now, create a fake signal ontop of the beam spot.
    # plt.ion()
    # plt.show()
    for ii in range(100):

        if ii == 0:
            sig = (_gaussianc(c, 1, 20, -500+(6*(49+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -400+(6*(49+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -300+(6*(49+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -200+(6*(49+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -100+(6*(49+1))) * np.cos(c/3) )
        elif ii < 20:
            sig = (_gaussianc(c, 1, 20, -500+(6*((49-ii*3)+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -400+(6*((49-ii*3)+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -300+(6*((49-ii*3)+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -200+(6*((49-ii*3)+1))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -100+(6*((49-ii*3)+1))) * np.cos(c/3) )
            print(49-ii*3+1)
        else:
            sig = (_gaussianc(c, 1, 20, -500+(9*(ii-27))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -400+(9*(ii-27))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -300+(9*(ii-27))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -200+(9*(ii-27))) * np.cos(c/3)
            + _gaussianc(c, 1, 20, -100+(9*(ii-27))) * np.cos(c/3) )

        sigs = (sig/7) / np.max(sig/7)
        S = G + sig/7

        ax.pcolormesh(X, Y, np.abs(S)**2, vmax=1.1, vmin=0.0, cmap=bbw.cm)
        # ax.imshow(np.abs(S)**2, vmax=1.1, vmin=0, cmap=bbw.cm, aspect='auto')
        ax.set_ylim(-250, 250)
        ax.set_xlim(-250, 250)
        # ax.plot(c, sig)
        plt.axis('off')

        # plt.draw()
        # fig.canvas.start_event_loop(0.1)

        print('Saving step %i of %i'%(ii+1, 100))
        numstep = str(ii+1).zfill(6)
        fig.savefig('./Image Frames/Step_' + numstep + '.png', dpi=200)

        # clear the axis and redraw.
        ax.clear()
        plt.draw()

# fig.savefig('./GaussianBeam_Modulated_FullGrating.png', dpi=200)

if Testing == True:

    tfig, tax = plt.subplots(1,1, figsize=(4,3), dpi=128)

    r, c = np.shape(S)
    lo = np.sum(S, axis=0)
    lo = lo / np.max(lo)

    tax.plot(lo)
####################################
if ShowPlots == True:
    plt.show()
