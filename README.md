# CamFollower
Simulation of a Cam and Follower mechanism.

The graph plots the displacement with angle for the mechanism on one side. On the other, the shapes of cam and followers are plotted along with path of the follower.

To use the program, modify the Data.txt file in the same folder as CamFollower.py. The name and location of the file must not be changed.
To define the case. You must first have a line with character '#'. This indicates the start of a new case.
In the next line you have to define Rb and Rf. You have to put character "|" after each value. The values must be in a particular order.
From this line you can start defining the segment motions.The format is as below for each case:

![5](https://user-images.githubusercontent.com/60822455/208420926-3139a2e0-4674-44a6-9cb9-1c4c43dc2b15.PNG)

Make sure that the lines are in ascending order. angle_end of one line must be equal to angle_start of the next one. The sum of rise displacements must be equal
to sum of return displacements. Otherwise, the cam profile wont be a closed curve.
Although not necessary, but it is advisable to have rise motions at the start, a dwell after the rise and finally return motions.
Also try to not have large displacements in small angle ranges. As, this can result in impossible meshes, that go inside the cam profile.
You can modify WIDTH and HEIGHT in CamFollower.py to change the width and height of turtle window

You have to wait until the drawing for once case is confirmed after which you have to press "Enter" with command line in focus to move onto the next case.

curve_type is the type of motion curve from 'Constant Accelaration', 'Simple Harmonic' or 'Cyclodial Motion'
segment_type is the displacement type from rise, dwell and return

Sample Outputs:

![1](https://user-images.githubusercontent.com/60822455/208420276-f65fd51c-391a-4d71-aaf5-6df71c4d68c1.PNG)

![2](https://user-images.githubusercontent.com/60822455/208420283-c6628b8a-3488-41de-8467-d2ae489748ee.PNG)

![3](https://user-images.githubusercontent.com/60822455/208420285-5234f5a5-83bb-49b1-8513-ec0b1d30824c.PNG)

![4](https://user-images.githubusercontent.com/60822455/208420288-186e61b4-7a17-479d-89c2-afac028f94d8.PNG)
