import matplotlib.pyplot as graph
import math
from astropy import constants as const
from skyfield.api import Loader, utc
from datetime import datetime, timedelta
import os
clear = lambda: os.system('cls')

#Needed for skyfield data to be loadable
load = Loader('~/skyfield-data')
ts = load.timescale()
bodiesData = load("de421.bsp")

#Constants
G = const.G.value
AU = const.au.value
GMSun = const.GM_sun.value
pi = math.pi
close = AU*50

class location():
    def __init__(self, pos, vel, velAng,bodyVelAng, date):
        self.pos = []
        self.vel = vel
        self.velAng = velAng
        self.bodyVelAng = bodyVelAng
        self.date = date
        
#Class for saved trajectories
class trajectoryInfo(object):
    def __init__(self,startDate,launchDV, timeforJourney, closestApp, closestAppTime, appVel, apo):
        self.startDate = startDate
        self.launchDV = launchDV
        self.timeforJourney = timeforJourney
        self.closestApp = closestApp
        self.closestAppTime = closestAppTime
        self.appVel = appVel
        self.apo = apo
#Class for bodies, eg sun and planets
class Body():
    def __init__(self, name, pos, ang, orbrad, rad, mass, SOI, fixed, color):
        self.name = name	
        self.pos = [0,0]
        self.orbrad = orbrad
        self.fixed = fixed
        self.rad = rad
        self.color = color
        self.mass = mass
        self.ang = ang
        self.SOI = SOI*self.rad
        if orbrad != 0:
            self.pos[0] = self.orbrad*math.cos(math.radians(self.ang))
            self.pos[1] = self.orbrad*math.sin(math.radians(self.ang))
            self.orbvel = math.sqrt(GMSun/orbrad)
            self.orbper = math.sqrt((4*pi**2*orbrad**3)/(GMSun))
            self.stepAng = 360/self.orbper		

#Class for the spacecraft                  
class Spacecraft(object):
    def __init__(self, name, vel, pos, color, closest, startBody, final, closeTime, closeVel):
        self.name = name
        self.vel = vel
        self. pos = pos
        self.color = color	
        self.closest = closest
        self.startBody = startBody
        self.final = final
        self.closeTime = closeTime
        self.closeVel = closeVel

#Initialise solar system bodies and create lists of bodies
sun = Body(name="Sun",pos=[0,0],orbrad=0,ang = 0, rad=const.R_sun.value,mass=const.M_sun.value,SOI = 1, fixed=True, color = "Yellow")
venus = Body(name="Venus",pos=[0,0],orbrad=AU*0.7233, ang = 0, rad=const.R_earth.value*0.9488,mass=const.M_earth.value*0.815, SOI = 102, fixed=False, color = "green")
earth = Body(name="Earth",pos=[0,0],orbrad=AU, ang = 0, rad=const.R_earth.value,mass=const.M_earth.value, SOI = 145, fixed=False, color = "blue")
mars = Body(name="Mars",pos=[0,0],orbrad=AU*1.5237, ang = 0,  rad=const.R_earth.value*0.53,mass=const.M_earth.value*0.107, SOI = 170, fixed=False, color = "red")
jupiter = Body(name="Jupiter",pos=[0,0],orbrad=AU*5.2044, ang = 0,  rad=const.R_earth.value*11.209,mass=const.M_earth.value*317.8, SOI = 687, fixed=False, color = "#f48641")
saturn = Body(name="Saturn",pos=[0,0],orbrad=AU*9.5826, ang = 0,  rad=const.R_earth.value*9.449,mass=const.M_earth.value*95.159, SOI = 1025, fixed=False, color = "#f4dc42")
uranus = Body(name="Uranus",pos=[0,0],orbrad=AU*19.2184, ang = 0,  rad=const.R_earth.value*4.007,mass=const.M_earth.value*14.536, SOI = 51.8, fixed=False, color = "#42ebf4")
neptune = Body(name="Neptune",pos=[0,0],orbrad=AU*30.11, ang = 0,  rad=const.R_earth.value*3.883,mass=const.M_earth.value*17.147, SOI = 86.8, fixed=False, color = "#4153f4")

              
              
sunSky = bodiesData["sun"]
venusSky = bodiesData["VENUS BARYCENTER"]
earthSky = bodiesData["EARTH BARYCENTER"]
marsSky = bodiesData["MARS BARYCENTER"]
jupiterSky = bodiesData["JUPITER BARYCENTER"]
saturnSky = bodiesData["SATURN BARYCENTER"]
uranusSky = bodiesData["URANUS BARYCENTER"]
neptuneSky = bodiesData["NEPTUNE BARYCENTER"]

bodies = [sun,venus,earth,mars, jupiter, saturn, uranus, neptune]
bodiesSky = [sunSky,venusSky,earthSky,marsSky, jupiterSky, saturnSky, uranusSky, neptuneSky]    
apo = location([0,0],0,0,0,datetime(1997,11,8,0,0,0).replace(tzinfo=utc))

#Draw position of planets on graph
def drawPos(bodies,spc):  
    for body in bodies:
        place = graph.Circle(body.pos, radius=body.rad*10, color=body.color)
        graph.gca().add_patch(place)
    x = spc.pos[0]
    y = spc.pos[1]    
    place1 = graph.Circle((x,y), radius=200000000, color=spc.color)
    graph.gca().add_patch(place1)

#Draw final position of planets on graph
def drawPosDone(bodies, spc):
    for body in bodies:
        if body.name != "Sun":
            place = graph.Circle(body.pos, radius=body.rad*500, color=body.color)
            graph.gca().add_patch(place)
        x = spc.pos[0]
        y = spc.pos[1]    
        place1 = graph.Circle((x,y), radius=bodies[2].rad*500, color=spc.color)
        graph.gca().add_patch(place1)

#Find initial positions of bodies at a given date, from skyfield API
def findBodyPos(body,currentDate, bodyNum):
    timeNow = ts.utc(currentDate)
    bodyPos = bodiesSky[bodyNum].at(timeNow).position.km*1000
    xSky = bodyPos[0]
    ySky = bodyPos[1]
    dSky = math.sqrt(xSky**2+ySky**2)
    body.ang = math.degrees(math.acos(xSky/dSky))
    if ySky < 0:
        body.ang = -body.ang
    initX = body.orbrad*math.cos(math.radians(body.ang))
    initY = body.orbrad*math.sin(math.radians(body.ang))
    return [initX,initY]

#Set up simulator first positions, setting planet and spacecraft initial locations
def initialSim(bodies, currentDate,spc,currentDV):
    countStepBody=0   
    spc.closest.clear()
    spc.closeTime.clear()
    spc.closeVel.clear()
    apo = location([0,0],0,0,0,datetime(1997,11,8,0,0,0).replace(tzinfo=utc))
    for body in bodies:
        spc.closest.append(close)
        spc.closeTime.append(datetime(1997,10,15,0,0,0).replace(tzinfo=utc))
        spc.closeVel.append(0)
        if not body.fixed:   
            body.pos = findBodyPos(body, currentDate, countStepBody)
            if spc.startBody == body.name:                            
                spc.pos[0] = body.pos[0] - body.SOI*math.sin(math.radians(90-body.ang))
                spc.pos[1] = body.pos[1] - body.SOI*math.cos(math.radians(90-body.ang))
                spcvelAng = body.ang + 90 
                if spc.pos[1] < 0:
                    spcvelAng = -spcvelAng
                velX = currentDV*math.cos(math.radians(spcvelAng)) 
                velY = currentDV*math.sin(math.radians(spcvelAng)) 
                spc.vel[0] = velX 
                spc.vel[1] = velY
            if spc.startBody == "DSM":
                spc.pos[0] = 91894034111.96698
                spc.pos[1] = 232145539946.29926
                spcD = (math.sqrt(spc.pos[0]**2+spc.pos[1]**2))
                spcvelAng = math.degrees(math.acos(spc.pos[0]/spcD))
                velX = currentDV*math.cos(math.radians(spcvelAng+90)) 
                velY = currentDV*math.sin(math.radians(spcvelAng+90)) 
                spc.vel[0] = velX 
                spc.vel[1] = velY
          
        countStepBody+=1

#Step spacecraft through one timestep   
def stepSpacecraft(bodies,spc, timeStep, currentDate,time):
    totForceX = totForceY = 0
    count = 0
    for body in bodies:
        dx = body.pos[0]-spc.pos[0]
        dy = body.pos[1]-spc.pos[1]
        dtotan=abs(dy)/abs(dx)
        gravAngle = math.atan(dtotan)    
        d = math.sqrt((dx)**2+(dy)**2)
        f = (G*body.mass)/(d**2)
        fx = math.cos(gravAngle) * f
        fy = math.sin(gravAngle) * f  
        if dx <= 0 and dy <= 0:
            fx = -fx
            fy = -fy
        elif dx > 0 and dy <= 0:
            fy = -fy
        elif dx<0 and dy>=0:
            fx= -fx     
        if spc.closest[count] > d:
            spc.closest[count] = d
            spc.closeTime[count] = currentDate+timedelta(seconds=time)
            spc.closeVel[count] = math.sqrt((spc.vel[0])**2+(spc.vel[1])**2)
                
        count += 1
        totForceX += fx
        totForceY += fy
    spc.vel[0] += totForceX * timeStep
    spc.vel[1] += totForceY * timeStep
    spc.pos[0] += spc.vel[0] * timeStep
    spc.pos[1] += spc.vel[1] * timeStep

#Step planets through one time step        
def stepPlanet(bodies, timeStep):
    for body in bodies:
        if body.fixed is False:
            angle = body.ang + body.stepAng*timeStep
            x = body.orbrad*math.cos(math.radians(angle))
            y = body.orbrad*math.sin(math.radians(angle))
            body.pos = [x,y]
            body.ang = angle

#Simulation looper, runs through from given initial date to end date.	
def simulation(bodies,spc,totalTime,currentDV, timeStep, currentDate):
    time = 0
    farRad = 0
    initialSim(bodies,currentDate,spc,currentDV)
    while time < totalTime:
        spc.foundClose = False
        stepPlanet(bodies,timeStep) 
        stepSpacecraft(bodies,spc,timeStep,currentDate,time)       
        if spc.final == True:
            drawPos(bodies,spc)
            spcD = (math.sqrt(spc.pos[0]**2+spc.pos[1]**2))
            if spcD>farRad:
                apo.date = currentDate+timedelta(seconds=time)
                apo.pos = spc.pos
                apo.vel = spc.vel
                #apo.vel = math.sqrt(spc.vel[0]**2+spc.vel[1]**2)
                apo.velAng = math.degrees(math.tan(spc.vel[0]/spc.vel[1]))
                apo.bodyVelAng = bodies[5].ang
                farRad = spcD
        time += timeStep

#Returns target number in list of planets
def findTarget(bodies, target):
    countTarget = 0
    for body in bodies:
        if body.name == target:
            return countTarget
        countTarget += 1

#Returns list of bodies, used to get list for use when simulator.py is called in other programs               
def returnBodyList():
    return bodies

def returnLocation():
    return apo
    
        
        
