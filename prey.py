"""Takeoff-hover-land for one CF. Useful to validate hardware config."""

#from _typeshed import Self
from pycrazyswarm import Crazyswarm


TAKEOFF_DURATION = 2.0
HOVER_DURATION = 2.0
G01_DURATION = 2.0

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    cf_prey = swarm.allcfs.crazyflies[0]
    cf_predator = swarm.allcfs.crazyflies[1]

    cf_prey.takeoff(targetHeight=0.5, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)

    #make prey use go_to service to travel to corner
    #for first move
    cf_prey.goTo(goal=[0.0,0.0,0.5], yaw=0.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION)

    #################################################
    #Make Prey takeoff in air as well.
    cf_predator.takeoff(targetHeight=1.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + HOVER_DURATION)
    print('In AIR')

    #Get location of prey
    prey_postion = []
    prey_position = cf_prey.position()
    #print('!!!!GOT LOCATION!!!!')

    #Go to location
    cf_predator.goTo(goal=[prey_position[0],prey_position[1],1.0], yaw=0.0, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION)

    #land
    cf_prey.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)
    #end land

     #land
    cf_predator.land(targetHeight=0.04, duration=2.5)
    timeHelper.sleep(2.5)
    #end land


if __name__ == "__main__":
    main()
    