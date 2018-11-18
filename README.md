# MDEC's The Grand Challenge - KL

This is my team's winning submission for MDEC's The Grand Challenge 2018 KL hackathon.

We are [Team Mavericks](https://team-mavericks.github.io/), and we were given a problem statement to solve within 2.5 days. It involves coming up with a practical implementation to save up energy costs in parking lots. The basic idea is to automatically dim or turn off the lights when there are no cars or humans around, potentially saving costs in many parking lots (especially ones with low activity).

Our implementation makes use of cameras as a form of wide-range motion sensors. By subtracting previous frames, we are able to detect whether a moving object is within a predetermined proximity, triggering the activation of lights in that corresponding area. 
