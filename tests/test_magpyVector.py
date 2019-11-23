#%% MAIN

import numpy as np
from magpylib.source.magnet import Box
from magpylib import getBv
from magpylib.math import axisFromAngles
from magpylib.math import angleAxisRotationV_priv

def test_magpyVector():
 
    # calculate the B-field for the 3axis joystick system with
    # vector and non-vecor code + compare

    #base geometry
    displM = 3
    dCoT = 0
    gap = 1
    a,b,c = 4,4,4
    Mx, My,Mz = 0,1000,0

    mag = [Mx,My,Mz]
    dim = [a,b,c]
    posM = [displM,0,c/2+gap]
    posS = [0,0,0]
    anch = [0,0,gap+c+dCoT]

    Nphi = 3
    Npsi = 33
    Nth = 11
    NN = Nphi*Npsi*Nth
    PHI = np.linspace(0,360,Nphi+1)[:-1]
    PSI = np.linspace(0,360,Npsi)
    TH = np.linspace(0,10,Nth)

    # magpylib classic:
    def getB(phi,th,psi):
        pm = Box(mag=mag,dim=dim,pos=posM)
        axis = axisFromAngles([psi,90])    
        pm.rotate(phi,[0,0,1],anchor=[0,0,0])    
        pm.rotate(th,axis,anchor=anch)
        return pm.getB(posS)

    Bc = np.array([[[getB(phi,th,psi) for phi in PHI] for psi in PSI] for th in TH])

    # magpylib vector
    MAG = np.array([mag]*NN)
    DIM = np.array([dim]*NN)
    POSo = np.array([posS]*NN)
    POSm = np.array([posM]*NN)

    ANG1 = np.array(list(PHI)*(Npsi*Nth))
    AX1 = np.array([[0,0,1]]*NN)
    ANCH1 = np.array([anch]*NN)

    ANG2 = np.array([a for a in TH for _ in range(Nphi*Npsi)])
    angles = np.array([a for a in PSI for _ in range(Nphi)]*Nth)
    AX2 = angleAxisRotationV_priv(angles,np.array([[0,0,1]]*NN),np.array([[1,0,0]]*NN))  
    ANCH2 = np.array([anch]*NN)

    Bv = getBv('box',MAG,DIM,POSo,POSm,[ANG1,ANG2],[AX1,AX2],[ANCH1,ANCH2])
    Bv = Bv.reshape([Nth,Npsi,Nphi,3])

    # load pre-calculated data
    B3 = np.load('test_data.npy')

    assert np.amax(Bv-Bc) < 1e-10, "bad magpylib vector"
    assert np.amax(Bv-B3) < 1e-10, "bad magpylib vector"