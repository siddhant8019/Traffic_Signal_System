# Traffic Signal System
The Machine learning project focuses on the difficulties metropolitan cities face—the solution to the existing traffic systems uses cameras and technology.
## Innovation: 
  Developed an optimized system to manage traffic in overcrowded cities.
## Technology: 
  Utilized YoloV5, OpenCV, and custom algorithms for real-time traffic density analysis.
## Research:   
  Extensive research for an effective and optimized solution.
## Government Collaboration: 
  Partnered with the state government for practical implementation.
## Signal Timing Adjustment: 
  Dynamically adjusted signal timings based on real-time traffic conditions.
## Convenience Improvement: 
  Enhanced commuter convenience by reducing congestion.
## City Efficiency: 
  Improved overall city efficiency through better traffic management.

## Implementation Details
This project can be broken down into three modules:

1. Vehicle Detection Module - This module detects the number of vehicles in the image received as input from the camera. More specifically, it will provide as output the number of vehicles of each vehicle class such as car, bike, bus, truck, and rickshaw.

2. Signal Switching Algorithm - This algorithm updates all signals' red, green, and yellow times. These timers are set based on the count of vehicles of each class received from the vehicle detection module and several other factors such as the number of lanes, average speed of each class of vehicle, etc.

3. Simulation Module - A simulation is developed from scratch using the Pygame library to simulate traffic signals and vehicles moving across a traffic intersection.

# 😊For reference 

![Screenshot 1](vehicle-detection.png)
