## 6/7/2021
- I've made an additional Lab that uses simplifies Madgwick estimation for gyro data to display movement for the left upper arm with the ADL data. Based on S1-Drill data, the algorithm used is somewhat accurate but doesn't estimate the *initial global position* of the arm, so the movements are not realistic. 
    - The full Madgwick algorithm uses magnetometer and accelerometer data to estimate global position but I'm still learning the implementation.
- I found [one online sensor integration library called micropython-fusion](https://github.com/micropython-IMU/micropython-fusion) (MIT license) that uses the Madgwick method from 6/5 and have imported it into the sample-test-data folder of the repo. I then modified an example test script to make `sample-test-data/micropython-fusion-master/fusiontest_opportunity.py`, which makes a file of (w,x,y,z) orientation quaternions that can then be animated using `graph-animate-transf.py`.
    - I tried the generated data with the left upper arm and compared it to the quaternion data, and they agree qualitatively but are a bit different in detail. I think this is definitely a good enough algorithm to faithfully display the data to the client so they can see what's going on in the dataset and whether there's any major errors.
    - The library designed mainly for a specific type of hardware called MicroPython, but as long as you pass in a custom function for time intervals between sensor readings, you can use it for any accelerometer+gyro+magnetometer data.
    - Everything is hard-coded in the current version of the script I made. The directory structure is also not great. I would also like to move away from python files with dashes in their names since they are harder to import.
- Using a package for computation makes me ask a big question. Where should the transformation from sensor data to quaternions take place: On the client's machine in JS, or on the Linux server with Python/JS/C++/C? I like the idea of moving the computation off of the client's machine, but I don't yet know how that is done.
- Estimating gravity direction allows us to estimate the sensor's pitch, which helps place it in the global frame. I can estimate gravity direction in a data file by taking the average acceleration over a long time, but I don't really trust this because gravity direction is affected by orientation.
- I should probably do something about the bloat in the number of python files in this folder, but this is probably normal for a scratch pad repo. I could make it cleaner with some object-oriented system for classes that turn data files into quaternion arrays, but I'll only do that if Python code could potentially be used directly.

## 6/5/2021
- [This paper](http://vigir.missouri.edu/~gdesouza/Research/Conference_CDs/RehabWeekZ%C3%BCrich/icorr/papers/Madgwick_Estimation%20of%20IMU%20and%20MARG%20orientation%20using%20a%20gradient%20descent%20algorithm_ICORR2011.pdf) has one proposal for integrating gyro data accurately and links to a bunch of other potential methods. Since the gyro data I'm curretnly making is (i) quite exaggerated and (ii) depends on the ordering when I compose the rotations about individual axes together, I'm still looking to new methods.
    - There's a C++ implementation [here](https://github.com/arduino-libraries/MadgwickAHRS/blob/master/src/MadgwickAHRS.cpp), and it optionally involves magnetometer and accelerometer data also.
    - It's constrasted from a 'Kalman filter' which I need to look into because it seems to be pretty ubiquitous in sensor fusion.

## 6/4/2021
- Correction to myself on how coordinates work for OPPORTUNITY: the y-axis represents local sensor LEFT, not local sensor right. I can tell by the diagram on page 10 of the manual.

## 6/3/2021
- I decided to look at using the gyro data. There are three data points, gyroX, gyroY, and gyroZ, and based on some general reasearch and information from the more recent Xsens manual (not the one linked on the OPPORTUNITY website) it seems that these represent the rotation about the local x, y and z axes.
- Using this information I created a composition of three quaternions and applied them at each time interval, so that I could estimate the orientation by simulating each recorded angular velocity.
    - Since this is basically Euler's method for integrating, I probably have an expected error on the order of h^2 where h is the time step, which means things could get out of hand very quickly.
- I got my current results with the command `python graph-gyro-data.py data-samples/S1-Drill.dat --offset 53 --maxlines 500` using the new Python program. Compare them to the animated results for the same bone (RUA) to see what is the same and what is different.
    - It seems that the magnitude of the movements is off by a significant margin compared to the quaternions. However, We still see the bouncy movement in an arc around the body, AND there's that odd loop at the top of the path in both versions. Really promising.

## 6/2/2021
- I'm looking at possible datasets for extending the project. The main source is the UCI machine learning dataset repository, and Karen and Charlotte [already sorted](https://docs.google.com/spreadsheets/d/17MQfr9Dy6LU3BbPSYQeYLCg20x13Vyc8chQxOFLT3xQ/edit#gid=0) the major HAR ones by citation.
    1. [Human Activity Recognition Using Smartphones Data Set](https://archive.ics.uci.edu/ml/datasets/human+activity+recognition+using+smartphones)
    - It has no quaternions but it does have lots of accelerometer data and data about the angle between gravity and the Samsung smartphone basis vectors. This is hard to apply to the model because it [just has one sensor](https://www.youtube.com/watch?v=XOEN9W05_4A) which indicates where the torso is facing--no joints. We probably want something with a relationship between limbs and body.
    2. [WISDM Smartphone and Smartwatch Activity and Biometrics Dataset Data Set](https://archive.ics.uci.edu/ml/datasets/WISDM+Smartphone+and+Smartwatch+Activity+and+Biometrics+Dataset+#)
    - There are two sensors: one on the dominant wrist (a smart watch) and one on the body (a phone). This means that we have some relationship between limb and body, but things will look very distorted when the arm is bent because we can't tell how the segments of limbs are oriented.
    3. Kasteren dataset
    - I haven't fully looked into this one since it's harder to get documentation on what sensors are involved. The download requires me to run a MATLAB script to view it so I may try that later on.
    - [One MDPI paper](https://www.mdpi.com/1424-8220/20/9/2702/htm) states that Kasteren is just environmental sensors.
- Since Karen and Charlotte already listed which datasets have a skeleton, I'm going to proceed starting with those ones.
- It's best to find ones that have quaternions, data on the per-joint level, and also ones that use Xsens sensors would be especially great since we have some experience on how they work.
    1. Cornell Activity Datasets CAD-60
    - This one is super promising because it reports orientation of joints all over the body, in rotation matrix form. Sadly the links to it don't seem to be working, so it might have been taken down.
    2. [CASAS HAR datasets](http://casas.wsu.edu/datasets/)
    - The first one on the list uses ambient motion sensors instead of sensors on the target's body.
    - Item 18 on the list has wearable accelerometers on the right hip, dominant wrist, non-dominant upper arm, dominant ankle, and non-dominant thigh.
    3. [Daily and Sports Activities Data Set](https://archive.ics.uci.edu/ml/datasets/daily+and+sports+activities)
    - It has one unit each for torso, arm and leg. There is accelerometer data, gyro data and magnetometer data. The documentation is fairly sparse but I will look at papers about it.
    - [The paper introducing this dataset](http://kilyos.ee.bilkent.edu.tr/~billur/publ_list/cj14.pdf) shows that it also uses Xsens sensors which is very good news. There's also figures showing where they are on the body.


- Update on notes from two days ago: Sophie and I agree on all this and she has implemented it (indepenently) with the actual dataset. It turns out you can treat almost all of the bone the same way.

## 5/31/2021
- I recycled the functions from the python animator into a quick tester for quaternion transformations to see what set of transformations will get from sensor space to three.js space.
    - For quaternion **q = (w,x,y,z) = (1/2, -1/2, -1/2, -1/2)** and vector **v** in OPPORTUNITY space, **qv(q^-1)** is the corresponding vector in THREE space. This agrees with what Jonathan said and is demonstrated quickly by `../sample-test-data/utils/quat-operations.py`.
    - By OPPORTUNITY space, I mean that x points toward the camera, y points to camera right, and z points up. By THREE space, I mean that x points toward camera right, y points up, and z points toward the camera.
    - When I use this transformation in Sophie's lab from today (which is really promising) it does NOT cause the orientations of bones to be **qv**. I haven't tried it yet with one bone at a time. 
    - This probably has to do with the parent-child connection between bone orientations, but I thought that was accounted for because we're using global-to-local translation and the bones are manipulated in topological order (parent before child).
- I've just pulled Jonathan's log from 5/30/2021 and read it for the first time, and it looks like he has already used a similar quaternion to transform the coordinates and has done a bunch of tests, so I need to catch up with that.
- He used both pre- and post-multiplication to transform from OPPORUNITY global to THREE, based on the following snippet:
    ```js
          /* Transform our coordinate system */
          q.premultiply(new THREE.Quaternion(0.5, 0.5, 0.5, 0.5));
          q.multiply(new THREE.Quaternion(0.5, 0.5, 0.5, -0.5));
        
          /* Rotate the back to the correct initial position */
          q.premultiply(new THREE.Quaternion(-0.707, 0, 0, 0.707));
    ```
    - I should probably ask about this. Since we're multiplying two quaternions, we can just use the hamiltonian product of (0.5,0.5,0.5,-0.5) and **q** without having to both pre- and post-multiply.
- Last thought: What we should do is get in a situation where every bone is aligned along the x-axis. Then we know how to transform that into what was measured in the dataset--we just apply two quaternions.
- I just put this to the test in a new 'Sam 5/31' lab using the generated data which makes the bone go in a cone shape pointing toward positive x. As long as I first point the bone along the x-axis, I can then apply the transformation that points the local x-axis where I want it to go. The transformations for LUA are as follows:
    - Rotate 90 degrees CW (-270 CCW) along the z-axis, to get the arm pointing in the x-axis
    - Rotate 90 degrees CCW along the x-axis, to get the top of the arm pointing in the y-axis
        - The composite of these is **q**= (w,x,y,z) = (0.5, 0.5, 0.5, -0.5), or a 120-degree rotation CCW about (1, 1, -1).
    - Apply the quaternion from the dataset
    - Rotate 120 degrees CCW about (1,1,1), to switch basis between the OPPORTUNITY global space and that of THREE.js.
- If we can come up with transformations to point the bone in the positive x direction, we can then reliably apply OPPORTUNITY data. This is kind of punting the problem, though, since we still need to know how to point a bone in a direction. Every bone has its own default direction, and I'm not sure where it is written. Jonathan or Sophie might know.
    - Using the quaternion (0, 0, 0, 1) on every relevant shows that their default directions are all along the positive y axis, so that's convenient. However we at least have to use different quaternions for determining the correct 'up' direction for the arms.
    - A big challenge here is managing parents and children. We need to make sure that we can control the DIRECTION of a parent bone and child bone independently (but their positions should be tied together based on the orientation of the parent).
        - The strategy here is that for every quaternion applied to the parent, the opposite should be applied to every child. Is this already done by the ripple thing?

## 5/30/2021
- I modified the file to use labelled command line arguments with optional flags.  I can still  produce the same output using `python graph-animate-transf.py data-samples/S1-Drill.dat --o 59 --max 2000 --float`.

## 5/29/2021 
- I've changed my mind about the transformations based on page 17 and page 20 of the [manual](http://www.opportunity-project.eu/system/files/MTi_and_MTx_User_Manual_and_Technical_Documentation.pdf). It says that the sensor coordinate system *S* is described **in  reference to** a world coordinate system *G*, and the rotation matrix uses the coordinates of the basis vectors of *S* in *G*-space as its columns, so the transformation must be from *G* to *S*.
- I just tried out the visualizer from testing custom data, with the right upper arm data from subject 1's drill run. It's really promising and I posted it on slack and saved it. I used the following command: `python graph-animate-transf.py data-samples/S1-Drill.dat 59 float 2000`. I really need to clean up this program because it is legitimately very useful.

## 5/28/2021
- Putting logs in reverse order of date now so that adding a new entry doesn't require scrolling all the way through the log.
- What have I promised for the meeting today? What do I plan on working on between now and Tuesday?
    - I will modify the code for generating/visualizing sample data so that the quaternions represent transformations **from local to global** space. Right now they are the other way around.
    - I will look into what we are missing between THREE.js space and OPPORTUNITY space in order to accurately transform an orientation from global opportunity space to global THREE space.
        - The best candidate for this transformation is a rotation around (1,1,1) of 120 degrees.
    - I will work with someone else to test out ideas for that.
    - I want to put some of the actual datset through the python visualizer to see how coherent the data is. It should give us a hint about what the orientation is supposed to look like on the webserver.
    - I briefly mentioned the idea of automatically pulling on the server whenever there's a push to master. If I want to look further into that, there's [a PHP solution from stack overflow](https://stackoverflow.com/questions/10542158/how-do-you-do-an-automatic-git-pull-on-remote-server/18053061).

## 5/27/2021
- I decided to go back to making sample data, since now I have more understanding of the format of OPPORTUNITY data.
    - A flaw with the previous format was that I didn't know what was represented by the 'twist' (w) component. 
- This time, I'm using a target 'up' and target 'forward' direction to construct a rotation matrix, which then gets transformed to a quaternion and put in (w,x,y,z) format like in the xSens readings in the dataset.
    - The procedure for generating the data is in [generate-reference-transf.py](../sample-test-data/generate-reference-transf.py) in the `generate_data_new()` function.
- The only good data right now is in [the sample data folder](../sample-test-data/data-samples/circle-with-up-control.txt). It has the same motion as last week, but with the extra constraint that local 'up' is always tangent to the circle.
- There's also a really ugly coded [python program](../sample-test-data/graph-animate-transf.py) which animates the (approximate) position, direction and orientation of the sensor given a file with quaternions in (w x y z) form. I'm considering trying it on some of the actual OPPORTUNITY dataset soon.
    - The program takes the text file you want to read as a command line argument.
- Now that I trust the data that has been generated, I want to see it on the model. When I use it directly, there are some strange effects, but the location of the arm definitely agrees with the expected location of the y (right) axis in sensor space.

## 5/25/2021
- I know that I can use the technique from Stack Overflow that Jonathan referenced in order to get the quaternion for pointing the x-axis in a specific direction, but how do I also control roll (model z-axis)? 
- I know how to do it with a rotation matrix: Know where the new 'forward' (x) and 'up' (z) axes will be, take their normalized cross product as y, and use these basis vectors as the columns of a rotation matrix. How do I express this rotation matrix as a quaternion?
- According to [this](http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/) which is a website referenced in THREE.js documentation, there is a formula to do this, so I just might use it.

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
- I looked at Jonathan's notes on his attempts to use S4-ADL4.dat with the three.js model. I agree that we need to pre-apply a transform to get from global opportunity space *G* to three.js space *T*. What keeps confusing me is that we have two transformations from *G* but we need a chain of transformations from *G* to *S* to *T* or something similar (*S* is local space after a quaternion from the datset is applied). 
    - If we assume North = (1, 0, 0), we might just be able to (i) apply the quaternion from the opportunity dataset and (ii) swap the z and y coordinates and be done.
    - A given quaternion is just a rotation about an axis, where the axis has a North component, West component, and Up component, and we know the definition of these components in both coordinate systems *G* and *T*.

## 5/23/2021
- Having a small issue with pushing to git on a new branch. Git reports that I don't have permission, which is similar to when my SSH key is not configured. I'm making a small change to this repo to see if there's any issues pushing to this one.
- I downloaded the OPPORTUNITY 'challenge' dataset. It looks like the objective was to classify the activity for each section.
    - The legend for column labels in the challenge datset does NOT include any quaternion values, just 'gyro', 'magnetic' and 'acceleration'.
- I've made kind of a breakthrough in what to make of the quaternions because the website for the opportunity dataset as a [Q&A](http://www.opportunity-project.eu/node/53.html) section which links the manual for the sensors used. The quaternion represents the transformation from global coordinates to local coordinates.
![transformation](alignment-info.png)
- The quaternions are represented as (cos(alpha/2), **n**sin(alpha/2)) where **n** is the axis of rotation. Thus, the identity quaternion (1, 0, 0, 0) means that the front of the sensor (the part that the wire is NOT sticking out of, which faces *down* the arm) is pointed toward local magnetic north. Since the state of a bone is determined by shoulder position and bone orientation, that's enough info to know where to point the bone, IFF we assume a direction for magnetic north.

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
