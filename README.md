# Autonomous Vacuum Robot

## Project Overview
Our goal for this project is to create an autonomous vacuum that can clean in any environment it is placed in, similar to and inspired by a Roomba. This entails the robot being able to:
* **Detect and avoid obstacles** it cannot clear, such as toys or certain furniture.
* **Detect accessible obstacles** it can go under and clean, like table chairs.
* **Map surroundings** using 2D-LIDAR to create a map and localize itself.
* **Clean effectively** using a vacuum box mounted underneath to collect debris.

The robot moves in a spiral manner, starting in the center and working its way through the space while avoiding obstacles. It uses two wheels as its effectors and performs avoidance pivots when it encounters walls.

## Usage
To start the autonomous routine, run the following command:
```bash
python move.py
