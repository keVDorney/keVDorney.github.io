from __future__ import division, print_function
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

############ COMMENTS ##############
''' Making some pulses for the Wyvern figure.

    v2 - Difference in pulse train vs. single pulse.
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
def _gaussian(x, amp, cent, width):
    return amp*np.exp(-((x-cent)/width)**2)
####################################

########### BEGIN CODE #############

t = np.linspace(-1e3, 1e3, 1e3)

cents = np.arange(-7.5e2, 1e3, 2.5e2)
Gs    = []
Gtot  = np.zeros(shape=len(t))
for cdx, ci in enumerate(cents):
    print(ci)
    gi = _gaussian(t, 20, ci, 40)
    Gtot = Gtot + gi
    Gs.append(gi)

G = _gaussian(t, 20, 0, 40)


X, Y = np.meshgrid(t, np.linspace(0, 40, 1e3))
F = np.sin(X/40-0.25)

# Make figure.
fig, ax = plt.subplots(2, 1, figsize=(3, 4), dpi=128)
fig.subplots_adjust(left=0.11, bottom=0.10, right=0.95, top=0.96)


ax[0].imshow(F, cmap='rainbow', aspect='auto', extent=[-1e3, 1e3, 0, 40], zorder=0)
for gdx, ggi in enumerate(Gs):
    ax[0].plot(t, ggi, c='r', lw=1.0)
ax[0].fill_between(t, Gtot, 100, facecolor='w', edgecolor='none', zorder=2)

ax[1].imshow(F, cmap='rainbow', aspect='auto', extent=[-1e3, 1e3, 0, 40], zorder=0)
ax[1].plot(t, G, c='r', lw=2.0, zorder=1)
ax[1].fill_between(t, G, 100, facecolor='w', edgecolor='none', zorder=2)

for axi in ax:
    axi.set_xlim(-1e3, 1e3)
    axi.set_ylim(0, 40)
    axi.set_ylabel('Pulse Energy (nJ)', fontsize=12, labelpad=4)
    axi.tick_params(axis='both', which='both', labelleft=False, left=False)
ax[1].set_xlabel('Time (ps)', fontsize=12, labelpad=2)


# fig.savefig('./PulseTrainCompare_v1.png', dpi=400)

####################################
if ShowPlots == True:
    plt.show()
