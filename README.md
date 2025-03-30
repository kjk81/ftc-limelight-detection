# Limelight 3A Python Pipeline with OpenCV
This was made for FTC Into The Deep in 2024-2025, specifically Aspire Team 1885!

*normal_detect.py* contains code that, when run within Limelight 3A, runs contour detection and distinguishes between red samples (rectangular prisms), blue samples, and yellow samples based off color masks that, after rigorous fine-tuning in various environments, generally work, as well as a size limitation relative to a specifc camera height.
This script also identifies the orientation of the detected contour relative to the camera.

*quadrant_detect.py* achieves the same functions, but also returns a specific quadrant (of the camera's view) in which the detected contour resides.
*src* contains older files of development and some may not work completely.

I employed Python OpenCV, as well as NumPy!

The hardest part of this project was figuring out how to distinguish multiple touching objects of the same color because color masks don't help in such a scenario - rather, size restrictions do.
After testing various size limitations, as well as specifying the size ranges that might include multiple samples (not a single one), the script can completely distinguish a set of multiple touching objects and single objects, but because of the harsh limits needed for sizing and the fact that some touching objects, if parallel to one another, take up less space, it becomes increasingly difficult and some sort of edge detection algorithm must take place in order to further differentiate.

# Further Action To Be Taken
The case of two same-color, touching, and parallel objects can be fixed through the implementation of some sort of edge detection algorithm and potentially more masks that artificially create space between the two.
The problem can also be completely ignored (in my case) because two parallel objects hold the same orientation, so there's no need to differentiate them unless trying to obtain position.

I hope that in the future I can come back and solve it, but for now, have a look!