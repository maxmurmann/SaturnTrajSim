# SaturnTrajSim
Simulation of the Trajectory of the Cassini Mission to Saturn and Beyond

This is a simulation built for my final year project, which can scan for and find interplanetary gravity assist trajectories for spacecraft. It allows a specific date and starting planet to be chose, and the system will scan through all available trajectories to find as many that get close to the target planet.

# Abstract

In 1997, the Cassini probe launched on a trajectory towards Saturn. It did not, however, fly directly there. It performed a series of gravity assists around planets to reach the necessary orbital energy to reach Saturn. This trajectory involved fly-bys of Venus twice, Earth and Jupiter. The aim of this report is to build a system which can reliably recreate the Cassini trajectory. This was done by creating a program which simulates the Solar System, and then simulates the forces on the Spacecraft at each point along its trajectory. The system then uses a trial and error method to find the optimal trajectory for reaching Saturn. The trajectory found was accurate to within a few days for most of the trajectory, with a bigger discrepancy at the end, with the final approach to Saturn being about a year ahead of Cassini. 

# Skyfield

The sktfield library in Python allows for the accurate positions of the planets to be found at any given date in history or any date in the future. This is what is used to place the planets in their respective locations.

# Original System

This system was originally built in Python. The basis of how it worked is it would find the positions of the planets at the specified start date using the Skyfield data, and then would put the planets on rails in circualar orbits around the sun. This meant the planetary locations were not 100% accurate to where they could have been, however the aim was a to build a trajectory finder as opposed to an accurate reprisentation of the solar system. 

The trajectory finder itself was just a brute force method, scanning through a large range of launch dates and initial trajectories and would pick out the combinations that would give the closest approach to the desired target. From the closest approaches, the 'optimal' trajectory would then be chosen by the user.

The main problem with this approach was the computational time required, with most trajectory scans taking hours to run, especially for the longer trajectories.

# Rewrite of original code

The original code for this project was a mess, with a lot of incositencies and odd bugs, which worked for the calculations necessary for the project, however it was not ideal to attempt any futher analysis. After discovering that the Skyfield API allowed for a range of dates to be inputted as opposed to having to query every time, I rebuilt the system to utilise this function, and cleaned up a lot of the maths with Numpy. This newer, better version of the visualiser also works in 3 dimensions allowing for more accuracy. Even with this extra dimension added, the simulation would run much faster and allow for faster computing times.

# Improved methods of scanning

Something I'd like to try and impliment going forwards is a quicker version of finding a trajectory. At the moment, it's only trying a brute force method which is taking a large amount of time. Using some kind of machine learning in this case might allow for the program to approach the desired trajectories much faster.

