# Limelight 3A Python Pipeline with OpenCV
This was made for FTC Into The Deep in 2024-2025.

*normal_detect.py* contains code that, when run within Limelight 3A, runs contour detection and distinguishes between red samples (rectangular prisms), blue samples, and yellow samples based off color masks that, after rigorous fine-tuning in various environments, generally work, as well as a size limiting relative to a specifc camera height.
This script also identifies the orientation of the detected contour relative to the camera.

*quadrant_detect.py* achieves the same functions, but also returns a specific quadrant (of the camera's view) in which the detected contour resides.
*src* contains older files of development and some may not work completely.
