#projectile motion sim

#imports
import matplotlib.pyplot as plt
import numpy as np
import math

#variables
planetMass = 6*(10**24)
planetradius = 6.371*(10**6)
Gravconst = 6.67*(10**-11)
timestep = 1/8192

#functions + classes

def airdensity(alt):
    k = 0.2869
    if alt < 11000:
        pres = 101.29*((288.14 - 0.00649*alt)/288.08)**5.256
        t =  (15.04 - 0.00649*alt)+273.1
        p = pres/(k*t)
    elif alt < 25000:
        pres = 22.65*(math.e**(1.73-0.000157*alt))
        t = (-56.46)+273.1
        p = pres/(k*t)
    elif alt < 43000:
        pres = 2.488*((-131.21 + 0.00299*alt+273.1)/216.6)**(-11.388)
        t = (-131.21 + 0.00299*alt) +273.1
        p = pres/(t*k)
    else:
        p = 0
    
    #p = 1.1 * (e**(-alt*0.000111945))
    return p.real

def plotdata(arr,l):
    xvals = []
    yvals = []
    for i in range(len(arr)):
        xvals.append(arr[i][0])
        yvals.append(arr[i][1])
    plt.plot(np.array(xvals), np.array(yvals), label=l)
    

class projectile:
    def __init__(self, mass, xpos, ypos, resistance, gravtrue, initialvel, initialangle,name):
        self.mass = mass
        self.xpos = xpos
        self.ypos = ypos
        self.resistance = resistance
        self.gravtrue = gravtrue
        self.xvel = initialvel*math.cos(initialangle*math.pi/(180))
        self.yvel = initialvel*math.sin(initialangle*math.pi/(180))
        self.acc = [0,0]
        self.posdata = [[xpos, ypos]]
        self.veldata = []
        self.accdata = []
        self.name = name
        self.time = 0

    def grav1(self):
        r = planetradius + self.ypos
        accg = -planetMass*Gravconst/(r**2)
        return accg

    def grav2(self):
        return -9.8

    def collide(self,h):
        #print('height: ',h)
        if int(h) < 0:
            return True
        else:
            return False

    def resist(self):
        dcoeff = 0.04/self.mass
        p = airdensity(self.ypos)
        A = 0.04
        xdrag = -0.5*dcoeff*p*A*(self.xvel**2)*(abs(self.xvel)/self.xvel)
        ydrag = -0.5*dcoeff*p*A*(self.yvel**2)*(abs(self.yvel)/self.yvel)
        return [xdrag, ydrag]

    def position_update(self):
        self.time += timestep
        self.acc_update()
        accel = self.acc
        self.yvel += accel[1]*timestep
        self.xvel += accel[0]*timestep
        self.veldata.append([self.xvel,self.yvel,self.time])
        xdis = (timestep)*self.xvel + (accel[0]*(timestep**2))/2
        ydis = (timestep)*self.yvel + (accel[1]*(timestep**2))/2
        
        self.xpos += xdis
        self.ypos += ydis
        self.posdata.append([self.xpos,self.ypos])
        return self.collide(self.ypos)
        
    def acc_update(self):
        if self.gravtrue == True:
            gravac = (self.grav1())
        else:
            gravac = self.grav2()

        if self.resistance == True:
            dragac = self.resist()
        else:
            dragac = [0,0]
        jacc =  dragac[1] + gravac
        #print("acc vector: ", [dragac[0], jacc])
        self.acc = [dragac[0], jacc]
        self.accdata.append([dragac[0],jacc,self.time])                      

#mass, xpos, ypos, resistance, gravtrue, initialvel, initialangle,name        
cannon1 = projectile(20,0,0,False,True , 20, 30,"No Res, True Grav."  )
cannon2 = projectile(20,0,0,False,False, 20, 30,"No Res, False Grav." )
cannon3 = projectile(20,0,0,True ,True , 20, 30,"Air Res, True Grav." )
cannon4 = projectile(20,0,0,True ,False, 20, 30,"Air Res, False Grav.")
objarr = [cannon1,cannon2,cannon3,cannon4]
 

for k in objarr:
    end = False
    while end == False:
        if k.position_update() == True:
            end = True
            plotdata(k.posdata,k.name)
            
    
plt.legend(loc="upper right")
plt.title("Path trajectory")
plt.show()

for k in objarr:
    j = []
    h = []
    for i in range(len(k.veldata)-1):
        j.append([k.veldata[i][2], k.veldata[i][0]])
        h.append([k.veldata[i][2], k.veldata[i][1]])
    plotdata(j , f"xvel vs time : {k.name}")
    plotdata(j , f"yvel vs time : {k.name}")
plt.legend(loc="upper right")
plt.title ("XVelocity vs time")
plt.show()

for k in objarr:
    p = []
    o = []
    for i in range(len(k.accdata)-1):
        p.append([k.accdata[i][2], k.accdata[i][0]])
        o.append([k.accdata[i][2], k.accdata[i][1]])
    plotdata(p , f"xacc vs time :{k.name}")
    plotdata(o , f"yacc vs time :{k.name}")
plt.legend(loc="upper right")
plt.title("acceleration vs time")
plt.show() 
        








        
        
    
