## 5/22/2021
- I'm having trouble running the React server locally. Viewport.js tries to open an HTML file and parse it as JSON, then produces an exception, and I don't get past the model loading screen. Is there some package I need to  make sure to install? I already ran `npm install` and that allowed me to boot up the server locally in the first place with `npm start`.
- I've looked at the interpretation of the generated dataset in GenerateData.js and it seems to make a figure-8 pattern instead of a circle like it should. Additionally, it seems to be inaccurate on the very first time step.
    - The first time step should have the arm angled upward and centered front-to-back, but it seems not to be angled horizontally.
    - The twist on the upper arm should be constant such that the shoulder always faces upward but that is not happening right now.
    - The stack overflow page says we should use the size of the hypoteneuse between the arm vector and the target vector plus the dot product. ~~However, since both vectors are normalized, the hypoteneuse length should be sqrt(2) rather than 1, right?~~ You use the square root of the product of the lengths of the two vectors, which in this case is 1.
- I'm still not decided on whether the data interpreted by the visualizer should be in axis-angle form or standard orientation quaternion form. The best one is whichever requires the fewest calculations per frame (if the computation time there is important compared to other per-frame operations).
- It's also possible that we're making a figure 8 because the data actually makes a figure 8 instead of a circle. I am going to graph the points to verify that they correctly make a circle.
    - I've used graph-example-data.py to verify that output.txt traces out a circle in the plane orthogonal to v_out.
- It seems that the data does trace out a circle -- the vector pointing out of the top of the shoulder makes a circle on the horizontal plane, which makes sense since the shoulder is the 'direction' of the right upper arm.
- I mapped out how each axis vector causes the model's RUA to behave:

| Vector | Arm direction | Shoulder direction |
|---|---|---|
| (1, 0, 0) | up | back |
| (0, 1, 0) | down, out | back|
| (0, 0, 1) | out | up |

- This is super confusing and I'm trying to figure out the justification--maybe the shoulder isn't involved like I think it is, but when I use the back of the upper arm as a reference point, it also has a habit of pointing in the same direction twice.
- I'm going to give it a try using the arm position as my guide, but that doesn't really work because I don't have three linearly independent arm positions. None of them point forward or backward, so how can a mixture of them do so?
- I tried using the cross product and w from stack overflow in the generated data implementation and making a quaternion using THREE's `setFromAxisAngle` function, but that did not change anything. The implication is that the cross product handles the axis-angle aspect of setting the quaternion's x,y,z values. 
- Next idea: Judging by the scene from the fall semester's project, positive x is the left-hand side from the model's perspective (so the right arm points in direction (-1,0,0)) which means that we might want to calculate the rotation from (-1,0,0) to the relevant vector.
    - The result is that the arm is rotated 90 degrees toward the back along the sagittal plane. (90 degrees counterclockwise about (1,0,0)).
- At the moment I am very confused as to how to reliably move the arm in the z-axis if the three unit vectors produce arm locations that are not all linearly dependent. My next plan is to look into lookAt matrices and making quaternions from them, since that is the hack that kind of works in [some earlier tests](https://github.com/jpiland16/hmv-scratchpad/tree/master/sam-lookat-notes).

## 5/23/2021
- Having a small issue with pushing to git on a new branch. Git reports that I don't have permission, which is similar to when my SSH key is not configured. I'm making a small change to this repo to see if there's any issues pushing to this one.
- I downloaded the OPPORTUNITY 'challenge' dataset. It looks like the objective was to classify the activity for each section.
    - The legend for column labels in the challenge datset does NOT include any quaternion values, just 'gyro', 'magnetic' and 'acceleration'.
- I've made kind of a breakthrough in what to make of the quaternions because the website for the opportunity dataset as a [Q&A](http://www.opportunity-project.eu/node/53.html) section which links the manual for the sensors used. The quaternion represents the transformation from global coordinates to local coordinates.
![transformation](alignment-info.png)
- The quaternions are represented as (cos(alpha/2), **n**sin(alpha/2)) where **n** is the axis of rotation. Thus, the identity quaternion (1, 0, 0, 0) means that the front of the sensor (the part that the wire is NOT sticking out of, which faces *down* the arm) is pointed toward local magnetic north. Since the state of a bone is determined by shoulder position and bone orientation, that's enough info to know where to point the bone, IFF we assume a direction for magnetic north.

## 5/24/2021
- So if we have global data, our problem is that we don't really know which way the person is facing at t=0, we just know the global positions of each sensor.
- If we have local data, our problem is that we don't know the initial positions of the joints.
- Now that Jonathan's figured out and fixed the tiny issue that was preventing proper transformation of the arm, I can make a better table of what basis vector corresponds to what global arm heading.

| Vector | Arm direction | Shoulder direction |
|---|---|---|
| (1, 0, 0) | forward | in |
| (0, 1, 0) | up | back|
| (0, 0, 1) | out | up |

- the great news is that these form an easily understandable basis, and that the transformation quaternions used in GeneratedData.js are the same type of transformation as what is represented by the quaternion in the OPPORTUNITY dataset
    - so we need to transform from our xyz to opportunity's global xyz then to new orientation. There's also the 'local-to-global' transformation on the three.js side of things.
- the confusing news is that it seems we have x and z mixed up compared to what I expected.
    - that's only because of the 90 degree rotation about the y axis that jonathan implemented in order to account for ME using the wrong vectors for FORWARD and OUT when I generated the data.
    - I can fix it just by switching out the vectors used in generate-example-data.py
    