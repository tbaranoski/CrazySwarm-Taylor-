This read.me provides the instructions neccessary to get ROS running on the crazyflie VM and utilizing ROS with multiple Crazyflies. 
Flow decks must be used on the CF when using this code in the current configuration.
The read.me is meant to be a step by step instruction on how to familiarize one self with Crazyflie ROS avoiding problems that I had encountered.
Developer: Taylor Baranoski

## Getting Started

```sh
lsb_release -a
```
Confirm the version on VM is Ubuntutu 20.04

## Installing ROS

Follow th elink below to install ROS Noetic
http://wiki.ros.org/noetic/Installation/Ubuntu
In step 1.4, Make sure to Install the "Desktop-Full Install" when choosing package

## Installing Crazyswarm Repository
The Crazyswarm repository is a repository manageged by a third part (Not bitcraze) that is essentially a container for running ROS on multiple crazyflies.
There is a whole website dedicated to the installing the repository, how to use it...etc
https://crazyswarm.readthedocs.io/en/latest/

Start on the installation tab and make sure the "Pyhsical Robots and simultion" tab is selected. Go through the listed instructions.
For Part 3, installing the dependencies, you must follow the github page below in order to installthe gcc compiler:

https://github.com/ilg-archived/arm-none-eabi-gcc/releases/tag/v8.2.1-1.7
Use xpm to install. Follow the README.md on the github

## Configuration + Simulation Tutorial
It is important to source ROS every new terminal you open. To do this go to crazyswarm base folder and type:
```sh
source ros_ws/devel/setup.bash
```
Follow the configuration tab on https://crazyswarm.readthedocs.io/en/latest/ to configure the radio and crazyflies.
First crazyflie should have the address:0xE7E7E7E701
Second Crazyflie should be: 0xE7E7E7E702
Second Crazyflie should be: 0xE7E7E7E703 
...etc

The crazyflies must be on the same channel. This can be set up in the crazyflie client.

Now go to tutorial tab and try the test scrip in simulation mode.

## Edit Crazyswarm Code to Work without Positioning System
If the flow decks are being used, the launch file must be replaced.
```sh
cd crazyswarm
cd ros_ws
cd src
cd crazyswarm
cd launch
rm hover_swarm.launch
git clone https://github.com/tbaranoski/Flow_Deck_Positioning/blob/main/hover_swarm.launch
```
## Configuring Controller and Enabling Controller Permissions
You can use an XBOX or Playstation controller.
Figure out the name of the USB device using the following link/tutorial:
http://wiki.ros.org/joy/Tutorials/ConfiguringALinuxJoystick

Edit hover_swarm.launch line 3,
change JsX to the appropriate name for the controller.

## Run the Example: hover_swarm.launch
```sh
source ros_ws/devel/setup.bash
roslaunch crazyswarm hover_swarm.launch
```
Press 'start' / 'chanmge view' button on controller to mkae crazyflie take off
Press 'change view button' / 'back' to make crazyflie land.

## Familiarize Yourself with ROS
It is reccomended for the next steps to go through tutorials on ROS basics using following link:
http://wiki.ros.org/ROS/Tutorials
Go through all 21 begginer tutorials.

## Running ROS services on command line
```sh
source ros_ws/devel/setup.bash
roslaunch crazyswarm hover_swarm.launch
```

In a new terminal, while the original hover_swarm is running:
```sh
source ros_ws/devel/setup.bash
rosservice list
```
This shows a list of services.
To run /takeoff service
```sh
rosservice call /cf1/takeoff '{groupMask: 0, height: .5, duration: { secs: 3, nsecs: 5}'}
```
To run land
```sh
rosservice call /cf1/land '{groupMask: 0, height: .05, duration: { secs: 3, nsecs: 5}'}
```

To learn more how to use ROS services in the coommand line visit:
http://wiki.ros.org/rosservice#rosservice_list

## Running Go_To service in command line
go_to service is used to go to a specific coordinate. The syntax is tricky because the goal must be enetered in YAML format.
Example:
```sh
rosservice call /cf1/go_to '{groupMask: 0, relative: false, goal: {x: 2.0, y: 2.3, z: 2.8}, yaw: 0.0, duration: { secs: 4, nsecs: 5}'}
```

## Set up Multiple Crazylfies
Make sure the second crazyflie has address: 0xE7E7E7E702
Make sure the second crazyflie has same channel as CF #1.

Edit allCrazyflies.YAML and add ID(last two digits of address) and channel info for second crazyflie. Make saure both crazyflies are setup on the same channel.
To enable both crazyflies:
```sh
cd crazyswarm
source ros_ws/devel/setup.bash
cd ros_ws
cd src
cd crazyswarm
cd scripts
python3 chooser.py
```
Check mark both CF. Now both CF are set up.
 
 ## Importing my Python custom Script
 The custom script aims to implement ROS service functionality with a predator and prey example.
 ```sh
cd crazyswarm
source ros_ws/devel/setup.bash
cd ros_ws
cd src
cd crazyswarm
cd scripts
git clone https://github.com/tbaranoski/CrazySwarm-Taylor-/blob/main/prey.py
```
Now Run it by following below:

```sh
cd
cd crazyswarm
source ros_ws/devel/setup.bash
hover_swarm.launch
```

Now in another terminal:
```sh
cd crazyswarm
source ros_ws/devel/setup.bash
cd ros_ws
cd src
cd crazyswarm
cd scripts
python3 prey.py
```
## Understanding prey.py
prey.py uses ros services takeoff, land, and go_to. In order to properlly call them with proper arguments and syntax you must find the internal functions. The internal functions are located:

GO to file explorer. The path is:
 ```sh
cd crazyswarm
source ros_ws/devel/setup.bash
cd ros_ws
cd src
cd crazyswarm
cd scripts
cd pycrazyswarm
```
Then open file: crazyflie.py. Here you will see the function names and paramter for the ROS functions within the crazyflie class.

## Problem with prey.py
The position() function in ROS does not appear to be working  when just using the flow deck. My guess is that an absolute positioning system is needed instaed of an estimated positioning system (Flow deck is estimation).
The position function returns 0,0,0 for all the coordinates. This should be explored further as a work around or solution might be able to be found. 
For reference this is line 33 in prey.py:
```sh
prey_position = cf_prey.position()
```

This is where my research left off.
