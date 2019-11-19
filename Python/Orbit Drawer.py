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
graphSize = AU*10
graphDim = [-graphSize, graphSize, -graphSize, graphSize]
graphScale = 1000000
graph.figure(figsize=(6,6))
graph.axis(graphDim)

#Initialise Bodies and Spacecraft
spc = simu.Spacecraft(name="Cassini", vel = [0,0], pos = [AU-1*10**9,0], color="black", closest = [], startBody= "Earth", final = True, closeTime = [], closeVel = [])
bodies = simu.returnBodyList()

#Set initial conditions for orbit
timeStep = 3600
totalTime = 3600*24*365
startDate = datetime.datetime(1996,3,18,0,0,0).replace(tzinfo=utc)
dvInf =27206.49 

targetBody = "Mars"
targetBodyNum = simu.findTarget(bodies,targetBody)

#Simulation run
print("Running...")
simu.simulation(bodies,spc,totalTime,dvInf,timeStep,startDate)
simu.drawPosDone(bodies,spc)
print("Done, loading graph")

#Write outputs to file and save graph
outputFile = open("Outputs/BestFound.txt", "w")
apo = simu.returnLocation()
outputFile.write("Launch DV:" + str(dvInf))
outputFile.write("\nStart Date:" + str(startDate))
totalTimeDate = spc.closeTime[targetBodyNum] - startDate
outputFile.write("\nTotal Flight Time:" + str(totalTimeDate))
outputFile.write("\nLocation Pos:" + str(apo.pos))
outputFile.write("\nLocation Rad:" + str(((math.sqrt(apo.pos[0]**2+apo.pos[1]**2))/AU)))
outputFile.write("\nLocation Time:" + str(apo.date))
outputFile.write("\nLocation Vel:" + str(apo.vel))
outputFile.write("\nLocation Ang:" + str(apo.velAng))
outputFile.write("\nLocation Body Ang:" + str(apo.bodyVelAng))
outputFile.write("\n")
count = 0
outputFile.write("\nSpacecraft Closest Approaches")
outputFile.write("\n")
for space in spc.closest:
    outputFile.write("\nBody: " + bodies[count].name + "   Closest: " + str(round((spc.closest[count]/bodies[count].SOI),2)) + " Body SOI")
    outputFile.write("\nTime of closest approach: " +str(spc.closeTime[count]))
    outputFile.write("\n")
    count += 1

outputFile.close()
graph.savefig("Outputs\graph.png")
print("Graph saved")
input()
