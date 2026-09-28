#orbittracking
import math
import numpy as np
import matplotlib.pyplot as plt
import time

#constants
rocketMass = float(input("Mass of rocket(kg): "))
initalAngle = math.pi * float(input("Angle of lauch from the horizontal(deg): "))/180
initialForce = float(input("Magnitude of takeoff force(N): "))
planetMass = 6*(10**24)
planetRadius = 6.371*(10**6)
dcoeff = 0.5
timestep = 1/128
Gravconst = 6.67*(10**-11)
#p = 1.192
a = math.pi

#timeStep = float(input("Physics Frames/second: "))

#functions + classes

def absolute(vect):
    return math.sqrt(vect[0]**2 + vect[1]**2)

def airdensity(alt):
    alt = alt - planetRadius
    if alt < 11000:
        p = 101.29*((291.14 - 0.00649*alt)/288.08)**5.526
    elif alt < 25000 and alt >= 11000:
        p = 22.65*math.e**(1.73-0.000157*alt)
    else:
        p = 2.488*((141.89 - 0.00299*alt)/216.6)**(-11.388)
    return p        
        
def plotdata(arr):
    xvals = []
    yvals = []
    for i in range(len(arr)):
        xvals.append(arr[i][0])
        yvals.append(arr[i][1])
    plt.plot(np.array(xvals), np.array(yvals),'o')

class Rocket:
    def __init__(self, posx, posy, forcex, forcey, mass):
        self.pos = [posx, posy]
        self.force = [forcex, forcey]
        self.mass = mass
        self.vel = [0,0]
        self.time = 0
        self.poslog = [[0, posy]]
        self.gravlog = [[-1*Gravconst*planetMass*mass/((posx**2 + posy**2))*(posx/(math.sqrt(posx**2 + posy**2))), -Gravconst*planetMass*mass/((posx**2 + posy**2))*(posy/(math.sqrt(posx**2 + posy**2))), 0]]
        self.forcelog = [[forcex, forcey, 0]]
        self.vellog = [[0,0,0]]
        self.stage_update = False

    def failCheck(self):
        if (math.sqrt(self.positionx**2 + self.positiony**2)) < planetRadius:
            print("Crash landing on earth")
            return True
        elif Gravconst*planetMass/((self.positionx**2 + self.positiony**2)) < 0.05:
            print("Rocket Has gone too far")
            return True
        else:
            return False

    def gravforce(self):
        Gravityforce = -Gravconst*planetMass*self.mass/((self.pos[0]**2 + self.pos[1]**2))
        igravityforce = Gravityforce*(self.pos[0]/(math.sqrt(self.pos[0]**2 + self.pos[1]**2)))
        jgravityforce = Gravityforce*(self.pos[1]/(math.sqrt(self.pos[0]**2 + self.pos[1]**2)))
        return [igravityforce, jgravityforce]

    def resistance(self):
        dcoeff = 1.27/self.mass
        p = airdensity(math.sqrt(self.pos[0]**2 + self.pos[1]**2))
        A = 0.0311
        xdrag = -0.5*dcoeff*p*A*(self.vel[0]**2)**(abs(self.vel[1])/self.vel[0])
        ydrag = -0.5*dcoeff*p*A*(self.vel[1]**2)*(abs(self.vel[1])/self.vel[0])
        return [xdrag, ydrag]
        

    def forcesum(self, forcearray):
        force = [0,0]
        for vector in (forcearray):
            force[0] += (vector[0])
            force[1] += (vector[1])
        self.forcelog.append([force[0], force[1], self.time])
        self.force = force
    
    def vel_update(self):
        oldvel = self.vel
        currvel = [self.vel[0]+self.force[0]*timestep/self.mass , self.vel[1]+self.force[1]*timestep/self.mass]
        idiff = (currvel[0]**2 - oldvel[0]**2)/2*self.force[0]
        jdiff = (currvel[1]**2 - oldvel[1]**2)/2*self.force[1]
        self.vel = currvel
        self.vellog.append([currvel[0], currvel[1], self.time])
        return [idiff,jdiff]
        
    def positionupdate(self):
        self.time += timestep
        self.forcesum([self.gravforce(), self.resistance()])
        displacement = self.velupdate()

        self.pos[0] += displacement[0]
        self.pos[1] += displacement[1]
        
        if math.sqrt(self.positionx**2 + self.positiony**2) > planetRadius + 100000 and self.stage_update == False:
            self.mass = 0.3
            self.stage_update = True
            
        return self.failCheck()

def rocketinit(var1, var2):
    KSP1 = Rocket(0 , planetRadius + var1, var2*math.cos(initalAngle) , var2*math.sin(initalAngle), rocketMass) #posx, posy, forcex, forcey, mass
    end = False
    endloop = 0
    while KSP1.positionupdate() == False:
        
        if endloop %10000 == 0:
            match input("Would you like to end the sim(Y/N): "):
                case "Y":
                    end = True
                case "N":
                    pass
                case _:
                    pass
    plotdata(KSP1.positionlog)
    #plotdata(KSP1.gravlog)
    #plotdataKSP1.forcelog)

#plot gravity

plt.show()

#plot force

#plot planet
figure, ax = plt.subplots()
planet = plt.Circle( (0, 0 ),planetRadius ,fill = False )

ax.add_patch(planet)

plt.show()
time.sleep(240)

        
