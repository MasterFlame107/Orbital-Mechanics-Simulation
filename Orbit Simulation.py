#Orbit Simulation
'''
dx = v*dt = v*dt + a*dt^2 /2
dv = a*dt
a = F/m

things to add:
- air resistance around earth
- the moon
- multiple simulations at once
'''

#imports
import math
import numpy as np
import matplotlib.pyplot as plt


#Constants
timeStep = 1/128   #s   gap between physics step
gravConst = 6.67*(10**(-11))  #(m^3 / kg*s^2)

#Objects
class Planet:
    def __init__(self,mass,radius):
        self.mass = mass #Scalar kg
        self.radius = radius #Scalar m

class Satellite:
    def __init__(self,mass,position,velocity):
        self.mass = mass #Scalar kg
        self.pos = position #Vector [x , y]
        self.velocity = velocity #Vector [Vx , Vy]
        self.acc = [0 , 0] #Vector[ax , ay]
        
    def calcForce(self,planet):#calculating gravity
        dcoeff = 0.50 #Drag coeff; sphere(0.47) ,cone(0.50) ,cube(1.05) ,angledCube(0.85) ,streamlinedBody(0.04)
        p = airdensity((self.pos[0]**2 + self.pos[1]**2)**(1/2) - planet.radius)
        A = 0.04 #Cross sectional surface area
        forceVect = [-self.pos[0]*gravConst*self.mass*planet.mass/((self.pos[0]**2 + self.pos[1]**2)**(3/2)) -0.5*dcoeff*p*A*(self.velocity[0]**2 + self.velocity[1]**2)*(self.velocity[0]),
                     -self.pos[1]*gravConst*self.mass*planet.mass/((self.pos[0]**2 + self.pos[1]**2)**(3/2)) -0.5* dcoeff*p*A*(self.velocity[0]**2 + self.velocity[1]**2)*(self.velocity[1])]
        return forceVect #Vector [Fx , Fy]
    
    def moveUpdate(self,planet):
        Force = self.calcForce(planet)
        acceleration = [Force[0]/self.mass , Force[1]/self.mass]
        newVelocity = [self.velocity[0] + acceleration[0]*timeStep , self.velocity[1] + acceleration[1]*timeStep]
        newPosition = [self.pos[0]+ self.velocity[0]*timeStep + acceleration[0]*(timeStep**2)/2 , self.pos[1]+self.velocity[1]*timeStep + acceleration[1]*(timeStep**2)/2]
        self.acc = acceleration
        self.velocity = newVelocity
        self.pos = newPosition
        
    def crashCheck(self,planet):
        if (self.pos[0]**2 + self.pos[1]**2)**(1/2) < planet.radius:
            return True
        else: return False
        
    def escapeCheck(self,planet):
        if (self.pos[0]**2 + self.pos[1]**2)**(1/2) > planet.radius*(10**4):
                    return True
        else: return False

#Variables
dataRecord = [[],[],[],[],[],[]] #dataRecords is [positionX ,positionY ,radius ,velocity(Mag.) ,acceleration(Mag.),time]
Time = 0 #global time :-)
Rocket = Satellite(100,[0,6.371*(10**6) +335000],[10000,2000])
Earth = Planet(6*(10**24) , 6.371*(10**6))

#functions; execution, data recording and visualisation        
def recordData(sat,time,dataRecords): 
    #satellite class , global time var , dataRecords is [positionX ,positionY ,radius ,velocity(Mag.) ,acceleration(Mag.),time]
    #each record is of the form rec = [[valuesArray],[timeArray]] where each value correspponds to the time of the same index
    dataRecords[0].append(sat.pos[0])
    dataRecords[1].append(sat.pos[1])
    dataRecords[2].append((sat.pos[1]**2 + sat.pos[0]**2)**(1/2))
    dataRecords[3].append((sat.velocity[1]**2 + sat.velocity[0]**2)**(1/2))
    dataRecords[4].append((sat.acc[1]**2 + sat.acc[0]**2)**(1/2))
    dataRecords[5].append(time)
def airdensity(alt):
    k = 0.2869
    if alt < 11000:
        pres = 101.29 * ((288.14 - 0.00649 * alt) / 288.08) ** 5.256
        t = (15.04 - 0.00649 * alt) + 273.1
        p = pres / (k * t)
    elif alt < 25000:
        pres = 22.65 * (math.e ** (1.73 - 0.000157 * alt))
        t = (-56.46) + 273.1
        p = pres / (k * t)
    elif alt < 43000:
        pres = 2.488 * ((-131.21 + 0.00299 * alt + 273.1) / 216.6) ** (-11.388)
        t = (-131.21 + 0.00299 * alt) + 273.1
        p = pres / (t * k)
    else:
        p = 0
    return p
def createGraphs(dataRecs,planet):
    plt.plot(np.array(dataRecs[0]),np.array(dataRecs[1]))
    plt.plot(np.array(list(map(lambda x: planet.radius*math.cos(x*math.pi), np.linspace(0,2)))),np.array(list(map(lambda x: planet.radius*math.sin(x*math.pi), np.linspace(0,2)))))
    plt.title("Rocket path")
    plt.show()

    plt.title("R,V,A vs time")
    plt.subplot(3, 1, 1)
    plt.plot(np.array(dataRecs[5]),np.array(dataRecs[2]))
    plt.subplot(3, 1, 2)
    plt.plot(np.array(dataRecs[5]),np.array(dataRecs[3]))
    plt.subplot(3, 1, 3)
    plt.plot(np.array(dataRecs[5]),np.array(dataRecs[4]))
    plt.show()

keepLoop = True
while keepLoop == True: #execution loop (check every 30)
    print(f"Loop {Time}")
    for step in range(0 , int(36000/timeStep)):
        recordData(Rocket,Time,dataRecord)
        Rocket.moveUpdate(Earth)
        Time += timeStep
        if Rocket.crashCheck(Earth) == True:
            print("Rocket Crashed")
            keepLoop = False
            break
        elif Rocket.escapeCheck(Earth) == True:
            print("Rocket Escaped")
            keepLoop = False
            break
    if input("Do you want to keep s(t)imulating?(T/F) ") == False:
        keepLoop = False
    createGraphs(dataRecord,Earth)
    #print(dataRecord)
createGraphs(dataRecord,Earth)
    
    