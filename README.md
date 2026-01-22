# Autonomous Vacuum Robot

## Project Overview
Our goal for this project is to create an autonomous vacuum that can clean in any environment it is placed in, similar to and inspired by a Roomba. This entails the robot being able to:
* **Detect and avoid obstacles** it cannot clear, such as toys or certain furniture.
* **Detect accessible obstacles** it can go under and clean, like table chairs.
* **Map surroundings** using 2D-LIDAR to create a map and localize itself.
* **Clean effectively** using a vacuum box mounted underneath to collect debris.

The robot moves in a spiral manner, starting in the center and working its way through the space while avoiding obstacles. It uses two wheels as its effectors and performs avoidance pivots when it encounters walls.



https://github.com/user-attachments/assets/4401f4f9-d8f4-4791-b624-1d4e83f0e665


https://github.com/user-attachments/assets/cff132df-c4f4-40fb-ab70-eb8857d36190




## Usage

To start the autonomous routine, run the following command:
```bash
python move.py


