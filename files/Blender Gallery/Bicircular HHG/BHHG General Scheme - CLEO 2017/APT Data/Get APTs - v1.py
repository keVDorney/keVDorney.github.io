from __future__ import division
from __future__ import print_function
import numpy as np
import scipy as sp
from scipy import signal

### Extracting the data for the APTs presented in the 2017 CLEO talk.
Testing = False
Save = True

# Get the files containing the spectra.
ArDir = '/Users/keV_Dawg/Desktop/CU Boulder Ph D Shite (aka life)/Research/KApteyn Murnane Group/Circular Polarization HHG/Blue_Red Intensity Ratio Stuffs/Raw Datas/Figures and Data for Paper/Carlos - Theory/Time Frequency Analysis/Ar_Propag_2e14_Full/'

ArF1 = 'HHGonaxisXY_1.txt'
ArF2 = 'HHGonaxisXY_5.txt'
ArF3 = 'HHGonaxisXY_9.txt'
ArF4 = 'HHGonaxisXY_14.txt'
ArF5 = 'HHGonaxisXY_18.txt'

# Necessary constants.
omega = 0.057
t_period = 2 * np.pi / omega

# Now, calculate the APT from the spectra.
def GetAPTs(filename, ti1=0, ti2=1, pval=100, pad=False, interpol=False, norm=False):

    print('Generating Pulse Train From File:')
    print(filename)
    print('\n')

    ## Spectral arrays.
    Specx = np.zeros(shape=2048, dtype=complex)
    Specy = np.zeros(shape=2048, dtype=complex)
    ndt = 2048

    # Unpack the datas.
    Horder, xp, ixp, yp, iyp = np.genfromtxt(filename, unpack=True)

    # Get x and y spectral components.
    specx = xp + 1j*ixp
    specy = yp + 1j*iyp

    # Shift the spectra.
    Specx[:1024] = specx
    Specy[:1024] = specy

    for idx, energy in enumerate(Horder):
        if energy < 12.0:
            Specx[idx] = 0
            Specy[idx] = 0
        if energy > 45:
            Specx[idx] = 0
            Specy[idx] = 0

    if pad==True:

        # Try zero padding hard core before ifft.
        Specx = np.pad(Specx, (pval, pval), 'constant', constant_values=(0,0))
        Specy = np.pad(Specy, (pval, pval), 'constant', constant_values=(0,0))

        # Get the padded fields.
        Ex = np.fft.ifft(Specx)
        Ey = np.fft.ifft(Specy)

    else:
        # Get the fields.
        Ex = np.fft.ifft(Specx)
        Ey = np.fft.ifft(Specy)

    # Shift the fields to center them at t=0.
    fl = len(Ex)/2
    Ex = np.hstack((Ex[-fl:], Ex[:-fl]))
    Ey = np.hstack((Ey[-fl:], Ey[:-fl]))

    # Now, get the real part of the fields.
    Ex = np.real(Ex)
    Ey = np.real(Ey)

    if interpol == True:
        # Try interpolating.
        Ex = signal.resample(Ex, len(Ex)*3)
        Ey = signal.resample(Ey, len(Ey)*3)

    # Create the time array.
    dw = Horder[2] - Horder[1] # Frequency step size.
    wmax = (Horder[-1] + dw) * omega # Max frequency.
    t = np.linspace(0, len(Ex), len(Ex)) * np.pi / wmax # Time array.
    dt = t[2] - t[1]
    tmax = t[-1] + dt

    tplot = (t-tmax/2) / t_period

    if norm == True:
        Ex = Ex / np.max(np.abs(Ex))
        Ey = Ey / np.max(np.abs(Ey))

    # for idx, stuff in enumerate(Ex):
    #     print(idx, tplot[idx], np.sqrt(stuff**2 + Ey[idx]**2))

    # Truncate arrays to a single cycle of the IR field.
    tind = ((tplot>=ti1)&(tplot<=ti2))

    tplot = tplot[tind]
    Ex = Ex[tind]
    Ey = Ey[tind]

    # # Try padding the arrays for asthetics.
    # tpre = np.linspace(tplot[0], tplot[0]-0.25, 50)
    # tpost = np.linspace(tplot[-1], tplot[-1]+0.25, 50)
    # tplot = np.concatenate((tpre, tplot, tpost))
    # Ex = np.pad(Ex, (50, 50), 'constant', constant_values=(Ex[0], Ex[-1]))
    # Ey = np.pad(Ey, (50, 50), 'constant', constant_values=(Ey[0], Ey[-1]))

    return tplot, Ex, Ey

t1, Ex1, Ey1 = GetAPTs(ArDir+ArF1, ti1=0.5, ti2=6.50, interpol=True, norm=True)
t2, Ex2, Ey2 = GetAPTs(ArDir+ArF2, ti1=0.5, ti2=6.50, interpol=True, norm=True)
t3, Ex3, Ey3 = GetAPTs(ArDir+ArF3, ti1=0.360, ti2=6.360, interpol=True, norm=True)
t4, Ex4, Ey4 = GetAPTs(ArDir+ArF4, ti1=0.5, ti2=6.50, interpol=True, norm=True)
t5, Ex5, Ey5 = GetAPTs(ArDir+ArF5, ti1=0.5, ti2=6.50, interpol=True, norm=True)
# tl, Exl, Eyl = GetAPTs(ArDir+ArF5, ti1=0.5, ti2=6.50, interpol=True, norm=True)

# # Scale the time arrays by the interval.
# t1 = t1 / (3.040 + 3.180) * 2
# t2 = t2 / (3.040 + 3.180) * 2
# t3 = t3 / (3.360 + 3.640) * 2
# t4 = t4 / (3.040 + 3.180) * 2
# t5 = t5 / (3.360 + 3.640) * 2

# Save the 3D data arrays.
if Save == True:

    # Define the file names.
    fn1 = 'APT_0.1_long.txt'
    fn2 = 'APT_0.5_long.txt'
    fn3 = 'APT_1.0_long.txt'
    fn4 = 'APT_2.0_long.txt'
    fn5 = 'APT_4.0_long.txt'

    fn_long = 'APT_2.0_long.txt'

    out1 = open(fn1, 'w+')
    print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out1)
    for idx, stuff in enumerate(zip(t1, Ex1, Ey1)):
        print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out1)

    out2 = open(fn2, 'w+')
    print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out2)
    for idx, stuff in enumerate(zip(t2, Ex2, Ey2)):
        print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out2)

    out3 = open(fn3, 'w+')
    print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out3)
    for idx, stuff in enumerate(zip(t3, Ex3, Ey3)):
        print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out3)

    out4 = open(fn4, 'w+')
    print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out4)
    for idx, stuff in enumerate(zip(t4, Ex4, Ey4)):
        print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out4)

    out5 = open(fn5, 'w+')
    print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out5)
    for idx, stuff in enumerate(zip(t5, Ex5, Ey5)):
        print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out5)

    # out_long = open(fn_long, 'w+')
    # print('Time (fs)', 'Ex (arb. u.)', 'Ey (arb. u.)', sep='\t', end='\n', file=out_long)
    # for idx, stuff in enumerate(zip(tl, Exl, Eyl)):
    #     print(stuff[0], stuff[1], stuff[2], sep='\t', end='\n', file=out_long)

if Testing == True:

    import matplotlib
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import axes3d

    # Set fontsize of tick labels.
    matplotlib.rcParams['xtick.labelsize'] = 6
    matplotlib.rcParams['ytick.labelsize'] = 6

    fig = plt.figure(figsize=(5, 2), dpi=200)
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    ax1 = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')
    ax3 = fig.add_subplot(223, projection='3d')
    ax4 = fig.add_subplot(224, projection='3d')


    ax1.plot(t1, Ey1, Ex1, c='g', lw=1)
    ax2.plot(t2, Ey2, Ex2, c='m', lw=1)
    ax3.plot(t5, Ey5, Ex5, c='r', lw=1)
    ax4.plot(tl, Eyl, Exl, c='r', lw=1)
    # ax2.plot(t2, Ey2, Ex2, c='b', lw=1, label='%3.1f pad'%(100/len(Ex1)))
    # ax3.plot(t3, Ey3, Ex3, c='g', lw=1, label='%3.1f pad'%(200/len(Ex1)))
    # ax4.plot(t4, Ey4, Ex4, c='m', lw=1, label='%3.1f pad'%(500/len(Ex1)))

    ax1.view_init(elev=30, azim=-120) # Viewing angle.
    ax2.view_init(elev=30, azim=-120) # Viewing angle.
    ax3.view_init(elev=30, azim=-120) # Viewing angle.
    ax4.view_init(elev=30, azim=-120) # Viewing angle.

    plt.show()

# if Create == True:
#
#     import bpy
#
#     def make_APT(x, y, z, bevel_obj='Path', name=''):
#
#         # Create the curve data block.
#         cData = bpy.data.curves.new(name, type='CURVE')
#         cData.dimensions = '3D'
#         cData.resolution_u = 2
#
#         coords = np.vstack((x, y, z)).transpose()
#
#         # Map the coordinates to a spline function. For smoothness.
#         polyline = cData.splines.new('POLY')
#         polyline.points.add(len(coords-1))
#
#         for i, coord in enumerate(coords):
#             x, y, z = coord
#             polyline.points[i].co = (x, y, z, 1)
#
#         # actually create the stupid object.
#         cOBJ = bpy.data.objects.new(name, cData)
#
#         # Attach it to the scene.
#         scn = bpy.context.scene
#         scn.objects.link(cOBJ)
#         scn.objects.active = cOBJ
#         cOBJ.select = True
#
#         bpy.context.object.data.bevel_object = bpy.data.objects[bevel_obj]
#
#     make_APT(t1*10, Ex1, Ey1, name='APT 0.1')
#     make_APT(t2*10, Ex2, Ey2, name='APT 2.0')
