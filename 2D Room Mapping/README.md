This project spawned from a topic I studied at University. 

The process which I am attempting to follow is as follows:

- Create the ghost of a room hidden from the actual mapping algorithm.
- Simulate a distance sensor; send a ray out and if a boundary is overlapped, return a distance. If no boundary is found, return some known, fixed value.
- Using the returned distance and the angle of the sensor, calculate the location of the point and store it in memory.
- After a number of samples, build a shape out of these points, showing the best estimate of what the mapped room is.

This is how I would *like* the program to function, but of course there will be issues. I can already foresee a query of "how do we connect the points together?" How will it be decided which order to connect the points, and how will a cohesive shape be generated?

---
