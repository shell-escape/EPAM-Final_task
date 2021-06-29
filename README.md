<h3 align="center">Simulation of a robot moving across a field.</h3>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This is an interactive console application that accepts a simple set of commands to control a robot (a point on the field) within a certain field of arbitrary size. A field is a rectangle that contains empty points, bariers (points that a robot cannot pass) and walls (added automatically around the field). You can specify the size of the field (not considering the walls) and the probability for barriers using command line arguments. Then you can control the robot with simple commands like 'left', 'right', etc. (see 'Usage' section below).


<!-- GETTING STARTED -->
## Installation

1. Clone the repo:
   ```sh
   git clone https://github.com/shell-escape/EPAM-Final_task.git
   ```
2. Install required packages:
   ```sh
   pip install -r requirements
   ```
3. Add the project directory to PYTHONPATH. Example for Linux:
   ```sh
   export PYTHONPATH=$PYTHONPATH:path/to/project/directory
   ```
   
<!-- USAGE EXAMPLES -->
## Usage

There is an example how to run this application:
   ```sh
   python3 main.py --n_rows=10 --n_cosl=10 --p=0.2 --radius=3 --logfile=./file.json
   ```

Command line arguments explanation:
* **n_rows**: the number of rows in a generated field.
* **n_cols**: the number of columns in a generated field.
* **p**: the probability that a cell will be a barrier. Shoul be in [0, 1] range.
* **radius**: the radius the robot can see.
* **logfile**: the path to the json file to store the movement information. Default is "./robot_path.json".

The robot has a direction: 'up', 'down', 'left' and 'right'.

The robot starts at the closest available point to the center with 'up' direction.

The following command are available:
* **left**: moves the robot to the left cell (if possible).
* **right**: moves the robot to the right cell (if possible).
* **up**: moves the robot to the upper cell (if possible).
* **down**: moves the robot to the bottom cell (if possible).
* **turn_left**: turns the robot counterclockwise.
* **turn_right**: turns the robot clockwise.
* **turn_back**: turns the robot 180 degrees.
* **save**: saves movement history to a json file specified by 'logfile' command line argument.
* **look**: to print the field in robot's light radius specified by 'radius' command line argument.

After each move or turn, the robot reports about its position.

'look' command will display an ascii 'picture' like this:

![image](https://user-images.githubusercontent.com/77696343/123671147-a0adff00-d846-11eb-8c79-5b212ad09be3.png)

Green point is the robot. Orange points are points that the robot can see. '.' is an empty space, '+' is a barier, 'x' is a wall. The direction of the robot is displayed with '^' for 'up', '>' for 'right', '<' for 'left' and '=' for 'down'.
