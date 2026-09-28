#drop test

#imports
from  matplotlib.pyplot import plot, show, legend, scatter, title
import numpy as np

#variables
planetMass = 6*(10**24)
planetRadius = 6.371*(10**6)
Gravconst = 6.67*(10**-11)
timestep = 1/2048
dcoeff = 0.4
#p = 1.292
A = 0.25*3.141592
e = 2.718281

#classes/functions

def airdensity(alt):
    
    k = 0.2869
    if alt < 11000:
        pres = 101.29*((288.14 - 0.00649*alt)/288.08)**5.256
        t =  (15.04 - 0.00649*alt)+273.1
        p = pres/(k*t)
    elif alt < 25000:
        pres = 22.65*(e**(1.73-0.000157*alt))
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
    scatter(np.array(xvals), np.array(yvals),s=4, marker='*',label=l)

class projectile:
    def __init__(self,mass, vel, height, resistance , gravtrue, name):
        self.pos = height
        self.mass = mass
        self.vel = vel
        self.acc = 0
        self.time = 0
        self.res = resistance
        self.gravtrue = gravtrue
        self.posdata = [[0,height]]
        self.accdata = []
        self.veldata = []
        self.name = name

    def collide(self):
        if self.pos.real <= 0 :
            print(self.time,self.pos, self.vel,self.acc)
            return True
        
        else:
            return False

    def grav1(self):
        g = -planetMass*Gravconst/(self.pos+planetRadius)**2
        return g
    
    def resistance(self):
        airp = airdensity(self.pos.real)
        drag = -0.5*dcoeff*airp*A*(self.vel**2)/self.mass
        return drag

    def acc_update(self):
        if self.gravtrue == True:
            grav = self.grav1()
        elif self.gravtrue == False:
            grav = -9.8

        if self.res == True:
            drag = -self.resistance()
        else:
            drag = 0
        acc = drag + grav
        self.accdata.append([self.time,(acc.real)])
        self.acc = acc.real       

    def vel_update(self):
        oldvel = self.vel.real
        currvel = self.vel.real + self.acc*timestep
        self.veldata.append([self.time,abs(currvel)])
        self.vel = currvel
        return (oldvel)
        

    def pos_update(self):
        self.time += timestep
        self.acc_update()
        diff = self.vel_update()*timestep - self.acc*(timestep**2)/2
        displacement = diff.real
        self.posdata.append([self.time,self.pos+displacement])
        self.pos += displacement
        #print(self.pos,self.vel,self.acc,displacement)
        return self.collide()
'''   
ball1 = projectile(400,0,50000, True,False, "res + nograv")        #mass, vel, height, resistance , gravtrue
ball2 = projectile(400,0,50000,True,True, "res + grav")
ball3 = projectile(400,0,50000,False,False, "nores + nograv")
ball4 = projectile(400,0,50000,False,True, "nores, grav")
objarr = [ball1,ball2,ball3,ball4]
'''


objarr = []
for i in range(1,11):
    ball = projectile(98, 0 , 10000*i , True, True, f"{10000*i}m")
    objarr.append(ball)
'''   

for k in objarr:
    end = False
    while end == False:
        if k.pos_update() == True:
            end = True
            plotdata(k.posdata,k.name)
legend(loc="upper right")
title("Position vs time")
show()

for k in objarr:
    plotdata(k.veldata, k.name)
legend(loc="upper left")
title("Velocity vs Time")
show()

for k in objarr:
    plotdata(k.accdata, k.name)
legend(loc="upper left")
title("Acceleration vs Time")
show()

for k in objarr:
    j = []
    for i in range(len(k.posdata)-1):
        j.append([k.posdata[i][1], k.veldata[i][1]])
    plotdata(j , k.name)
legend(loc="upper right")
title ("Velocity vs position")
show()

for k in objarr:
    p = []
    for i in range(len(k.posdata)-1):
        p.append([k.posdata[i][1], k.accdata[i][1]])
    plotdata(p , k.name)
legend(loc="upper right")
title("acceleration vs position")
show() 

'''
p=[]
for k in range(len(objarr)):
    p.append([objarr[k].time, 10000*(k+1)])

plotdata(p, "Time of flight")
show()

        
        
        
