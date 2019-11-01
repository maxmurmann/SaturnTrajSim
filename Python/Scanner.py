import math
from astropy import constants as const
import Simulator as simu
import datetime
from skyfield.api import utc
import xlsxwriter
import os
clear = lambda: os.system('cls')

G = const.G.value
AU = const.au.value
GMSun = const.GM_sun.value
pi = math.pi

resetDate = datetime.datetime(1990,1,1,0,0,0).replace(tzinfo=utc)
spc = simu.Spacecraft(name="Cassini", vel = [0,0], pos = [AU-1*10**9,0], color="black", closest = [], startBody= "Earth", final = False, closeTime = [], closeVel = [])
spcFinal = simu.Spacecraft(name="CassiniOpt", vel = [0,0], pos = [AU-1*10**9,0], color="black", closest = [], startBody= "Earth",  final = True, closeTime = [], closeVel = [])
spcReset = simu.Spacecraft(name="Cassini", vel = [0,0], pos = [AU-1*10**9,0], color="black", closest = [], startBody= "Earth", final = False, closeTime = [], closeVel = [])
bodies = simu.returnBodyList()

finalTrajectories = []

targetDistance = 100

timeStep = 3600
totalTime = 3600*24*365*15

stepStartDate = datetime.timedelta(days=1)
startDate = datetime.datetime(1977,8,2,0,0,0).replace(tzinfo=utc)
endDate = datetime.datetime(1977,8,2,0,0,0).replace(tzinfo=utc)
currentDate = startDate

stepDV = 100

dvStart = 34000
dvEnd = 36000

currentDV = dvStart

targetBody = "Neptune"

for body in bodies:
    spcFinal.closest.append(AU*50)

currentCalc = 0
totalCalc = ((endDate+stepStartDate-startDate)/stepStartDate) + ((dvEnd-dvStart)/stepDV)*((endDate+stepStartDate-startDate)/stepStartDate)
targetBodyNum = simu.findTarget(bodies, targetBody)


startapproxtime= datetime.datetime.now()
simu.simulation(bodies,spc, totalTime, currentDV, timeStep, currentDate)
endapproxtime = datetime.datetime.now()

approxTimePerCalc = endapproxtime-startapproxtime
approxTime = totalCalc*approxTimePerCalc

print("Total Calculations: " + str(totalCalc))
print("Approx time: " + str(approxTime))
input("Ensure Excel is closed, and press enter to continue")

startTime = datetime.datetime.now()
farEnough = True
bodyCountClose = 0
foundCount = 0

while currentDate <= endDate:
    currentDV = dvStart
    while currentDV <= dvEnd:
        currentCalc += 1
        #clear()
        print(str(round((currentCalc*100/totalCalc),2))+"%")      
        simu.simulation(bodies,spc, totalTime, currentDV, timeStep, currentDate)
        farEnough = True   
        bodyCountClose = 0
        for closer in spc.closest:
            if closer < bodies[bodyCountClose].rad*1.2 and bodyCountClose != targetBodyNum:
                farEnough = False
            bodyCountClose += 1
        if spc.closest[targetBodyNum] < bodies[targetBodyNum].SOI*targetDistance and farEnough == True:
            finalTrajectories.append(simu.trajectoryInfo(currentDate,currentDV,0,(spc.closest[targetBodyNum]/bodies[targetBodyNum].SOI),spc.closeTime[targetBodyNum],(spc.closeVel[targetBodyNum]-bodies[targetBodyNum].orbvel),simu.returnLocation()))            
            foundCount +=1
        currentDV += stepDV
    currentDate += stepStartDate

finishTime = datetime.datetime.now()
finishTime = finishTime-startTime
try:
    workbook = xlsxwriter.Workbook("Outputs/trajectories.xlsx")
except:
    input("Close Excel")
    workbook = xlsxwriter.Workbook("Outputs/trajectories.xlsx")

worksheet = workbook.add_worksheet()
worksheet.write(0,0,"Traj")
worksheet.write(0,1,"Launch Date")
worksheet.write(0,2,"Launch DV")
worksheet.write(0,3,"Closest App")
worksheet.write(0,4,"App Time")
worksheet.write(0,5,"App Vel")
worksheet.write(0,6,"Total Time")
worksheet.write(0,7,"Apo Time")
worksheet.write(0,9,"Closest Trajectory")
worksheet.write(0,10,"Total Calculations")
worksheet.write(0,11,"Estimated Time")
worksheet.write(0,12,"Total Time Taken")

try:
    closestTraj = finalTrajectories[0]
except IOError:
    input("No trj Found")
countTraj = 0
row = 1
count = 1

for final in finalTrajectories:
    if closestTraj.closestApp > final.closestApp:
        closestTraj = final
        countTraj = count
    worksheet.write(row,0,count)
    worksheet.write(row,1,str(final.startDate))
    worksheet.write(row,2,final.launchDV)
    worksheet.write(row,3,final.closestApp)
    worksheet.write(row,4,str(final.closestAppTime))
    worksheet.write(row,5,final.appVel)
    totalTimeDate = final.closestAppTime - startDate
    worksheet.write(row,6,str(totalTimeDate))
    worksheet.write(row,7,str(final.apo.date))

    count +=1
    row+=1
string = 'internal:Sheet1!A'+str(countTraj+1)
worksheet.write_url(1,9,string)
worksheet.write(1,9,countTraj)
worksheet.write(1,10,currentCalc)
worksheet.write(1,11,str(approxTime))
worksheet.write(1,12,str(finishTime))
chart = workbook.add_chart({'type': 'line'})
chart.add_series({'values': ["Sheet1",1,3,row,3]})
worksheet.insert_chart(3,9,chart)
workbook.close()
print("Done")
input()


