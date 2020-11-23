from __future__ import division, print_function
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

############ COMMENTS ##############
''' Just a simple schematic showing the Kerr Lensing effect.
'''

# Set fontsize of ticklabels globally for 128 dpi display.
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
####################################

####### SECTION STATEMENTS #########
ShowPlots = True # Toggles plt.show() on/off in a global fashion.
####################################

######## "GLOBAL" PARAMETERS #######

####################################

######### HELPER FUNCTIONS #########
def _gaussian(x, center, width, amp=1):
    return amp*np.exp(-(x-center)**2/width**2)

def _gaussian2D(x, y, cx, cy, wx, wy, amp=1):
    return amp*np.exp(-(x-cx)**2/wx**2 - ((y-cy)/wy)**2)

####################################

########### BEGIN CODE #############

x  = np.linspace(-1e2, 1e2, 1e3)

y1 = 1e-5*x**2 + 0.75
y2 = -1e-5*x**2 + 0.25

y11 =  5e-6*(x-100)**2 + 0.65
y21 = -5e-6*(x-100)**2 + 0.35

# Make figure.
fig, ax = plt.subplots(1, 1, figsize=(6, 3), dpi=128)
fig.subplots_adjust(left=0, bottom=0, right=1, top=1)

axpos = ax.get_position()
ax2   = fig.add_axes([axpos.x1-0.20, 0.65, 0.20, axpos.y1-0.65])

# Make the media.
X, Y = np.meshgrid(x, np.linspace(0, 1, 1e3))
G    = _gaussian(Y, 0.6, 0.2)
G2   = _gaussian2D(X, Y, 0, 0.5, 50, 0.25)
G[G<0.2] = 0.2
G2[G2<0.2] = 0.2

ax.imshow(G,   aspect='auto', vmin=0, vmax=1, cmap='Reds', extent=[-1e2, 1e2, 0, 1.2])
ax2.imshow(G2, aspect='auto', vmin=0, vmax=1, cmap='Reds', extent=[-1e2, 1e2, 0, 1.2])


x1 = (np.abs(x + 50)).argmin()
x2 = (np.abs(x - 50)).argmin()

ax.fill_between(x[:x1],  np.ones(shape=len(x[:x1]))*1.2, facecolor='w', edgecolor='none')
ax.fill_between(x[x2:],  np.ones(shape=len(x[x2:]))*1.2, facecolor='w', edgecolor='none')

ax.plot(x, y1,  c='r', lw=2.0, alpha=0.5)
ax.plot(x, y2,  c='r', lw=2.0, alpha=0.5)

ax.plot(x, y11,  c='r', lw=2.0)
ax.plot(x, y21,  c='r', lw=2.0)

ax.set_ylim(0, 1.2)
ax.set_xlim(-1e2, 1e2)
ax.tick_params(axis='both', which='both', left=False, labelleft=False, bottom=False, labelbottom=False, top=False, right=False)

ax.annotate(r'$\mathsf{n_{2}\sim0}$', xy=(0.05, 0.9),  xycoords='axes fraction', fontsize=16, color='k')
ax.annotate(r'$\mathsf{n_{2}>0}$',    xy=(0.45, 0.9),  xycoords='axes fraction', fontsize=16, color='k')
ax.annotate('    CW\nEmission',       xy=(0.05, 0.45), xycoords='axes fraction', fontsize=16, color='r', alpha=0.5)
ax.annotate('  Pulsed\nEmission',     xy=(0.80, 0.35), xycoords='axes fraction', fontsize=14, color='r')


ax2.tick_params(axis='both', which='both', left=False, labelleft=False, bottom=False, labelbottom=False, top=False, right=False)
ax2.set_xlabel('X Plane', fontsize=8)
ax2.set_ylabel('Y Plane', fontsize=8)

# fig.savefig('./n2Schematic_v1.png', dpi=400)
####################################
if ShowPlots == True:
    plt.show()
