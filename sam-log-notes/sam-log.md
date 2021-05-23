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