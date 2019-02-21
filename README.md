# About 
MagPyLib is an open-source Python library for calculating magnetic fields from permanent magnets and current distributions. It provides an intuitive class structure to **quickly generate, group, manipulate and visualize magnet assemblies and current distributions.**

The advantage of the **analytical approach** is the computation speed which can be in the sub millisecond range. This is easily **_five orders of magnitude faster_ when compared to FEM-based numerical calculations**. This makes MagPyLib highly efficient when dealing with multivariate global optimization problems that often appear in Magnetic System Design.

---
### Dependencies: 
_Python3.2+_, _Numpy_, _Matplotlib_

---
### Local Installation Instructions:
- Create virtual environment:
```bash
$ conda create -n packCondaTest 
```
- Activate:

```bash
$ conda activate packCondaTest
```

- Install the generated library for the environment:


```bash
(packCondaTest) /magpylib$  pip install .
```

The library is now in the packCondaTest environment.

### Examples:

The example program below shows how two permanent magnets are created and geometrically manipulated. They are grouped in a single collection and the system geometry is shown using a supplied method. The total magnetic field that is generated by the collection is calculated on a grid in the xz-plane and is displayed using matplotlib.


Field Plot           |  System Plot
:-------------------------:|:-------------------------:
![](https://magpy752453052.files.wordpress.com/2018/11/fieldplot2.png)  |  ![](https://magpy752453052.files.wordpress.com/2018/11/systemplot.png )



---

```Python
# imports
import numpy as np
import matplotlib.pyplot as plt
import magpylib as magpy

# create magnets
magnet1 = magpy.PermanentMagnet(typ=’box’,mag=[0,0,600],dim=[3,3,3],pos=[-4,0,3])
magnet2 = magpy.PermanentMagnet(typ=’cylinder’, mag=[0,0,500], dim=[3,5], pos=[0,0,0])

# manipulate magnets
magnet1.rotate([-4,0,3],[0,45,0])
magnet2.moveBy([5,0,-4])

# collect magnets
pmc = magpy.Collection()
pmc.addSource(magnet1)
pmc.addSource(magnet2)

# display system geometry
pmc.displaySystem()

# calculate B-fields on a grid
xs = np.linspace(-10,10,20)
zs = np.linspace(-10,10,20)
Bs = np.array([[pmc.getB([x,0,z]) for x in xs] for z in zs])

# display fields using matplotlib
fig, ax = plt.subplots()
X,Y = np.meshgrid(xs,zs)
U,V = Bs[:,:,0], Bs[:,:,2]
ax.streamplot(X, Y, U, V, color=np.log(U**2+V**2), density=1.5)
plt.show() 
```
