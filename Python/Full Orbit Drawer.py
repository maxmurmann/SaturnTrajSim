import matplotlib.pyplot as graph
from astropy import constants as const
from skyfield.api import utc
import math
import datetime
import Simulator as simu

#Constants
G = const.G.value
AU = const.au.value
GMSun = const.GM_sun.value
pi = math.pi

#Initialise graph
graphSize = AU*2
graphDim = [-graphSize, graphSize, -graphSize, graphSize]
graphScale = 1000000
graph.figure(figsize=(6,6))
graph.axis(graphDim)

#Initialise Bodies and Spacecraft
spc = simu.Spacecraft(name="Cassini", vel = [0,0], pos = [AU-1*10**9,0], color="black", closest = [], startBody= "Earth", final = True, closeTime = [], closeVel = [])
bodies = simu.returnBodyList()

#Set initial conditions for orbit
timeStep = 3600
totalTime = 3600*24*389
targetBody = "Mars"
targetBodyNum = simu.findTarget(bodies,targetBody)

startDate = datetime.datetime(1996,3,18,0,0,0).replace(tzinfo=utc)
dvInf =27206.49

#Simulation run
print("Running 1...")
simu.simulation(bodies,spc,totalTime,dvInf,timeStep,startDate)
x = spc.pos[0]
y = spc.pos[1]    
place1 = graph.Circle((x,y), radius=bodies[2].rad*500, color="#cb42f4")
graph.gca().add_patch(place1)
print("Running 2...")
totalTime = 3600*24*1660
startDate = datetime.datetime(1998,12,2,2,0,0).replace(tzinfo=utc)
#Flyby DV
dvInf =16896.95
#Slow DV
#dvInf = 16896.972
spc.startBody = "DSM"
simu.simulation(bodies,spc,totalTime,dvInf,timeStep,startDate)

simu.drawPosDone(bodies,spc)
print("Done, loading graph")
graph.savefig("Outputs\graph2.png")
print("Graph saved")
print("Burn: " + str(17706.369381370117-dvInf))
input()