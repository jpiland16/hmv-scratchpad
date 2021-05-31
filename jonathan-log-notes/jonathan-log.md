---
tags: [hmv-scratchpad]
title: jonathan-log
created: '2021-05-24T17:36:41.689Z'
modified: '2021-05-31T12:57:17.018Z'
---

Note: all quaternions in these notes will be given in XYZW format.

## 5/31/2021

 - Made the assumption that there were a limited (24) number of initial positions for the back - 8 along each axis. Found quaternions for each orientation and stored them in an array, as shown below. (The colored numbers correspond to array indices.) 

 <img src="./bodyRotations.png">

 > Note: When describing orientation in three dimensions, quaternions are unique *up to sign*. So (0, 0, 0, 1) = (0, 0, 0, -1).

 - The tests conducted on [5/29](#5292021) thus corresponded to the following quaternions:
   - Test 1: #9
   - Test 2: N/A
   - Test 3: #14
   - Test 4: #17
 - For the tests conducted on [5/30](#5302021):
   - Test 1: #23
   - Test 2: #21

 - When using the lab (titled _Jonathan 5/27/2021_) to check through all 24 possible initial orientations, #5 and #15 looked the best, except for the fact that the sitting and laying down motions still looked sideways. So I added an optional (enabled by default) 90&deg; CCW rotation of the body about the vertical axis, and this seemed to make the motions look correct.

   - TODO: 
     - [ ] figure out why this worked
     - [ ] figure out if either #5 or #15 is the correct initialization quaternion (or neither)
     - [ ] apply whatever reasoning comes out of the above into the other joints (maybe)

     
## 5/30/2021

 - At this point, just trying some random adjustments to see if anything looks right.
   - Test 1: (-0.5, -0.5, 0.5, 0.5) = Chest in YZ facing -X, head in -Z. _Person seemed upside down, and the laying action looked wrong._
   - Test 2: (-0.5, 0.5, -0.5, 0.5) = Chest in YZ facing +X, head in -Z. _Person was primarily right-side-up as viewed from viewport. Still had the sit-lay-stand anomaly, though._
 - This started to get a bit tedious, and I was concerned about trying the same thing repeatedly or missing a possibility due to my lack of organization. Creating a lab module to address this problem... (see tomorrow's notes)


## 5/29/2021

 - Copied the opportunity dataset to the server
 - Tested out some of the transformations we discussed on Friday with the `S4-ADL4` file.
   
   **TEST 1**
    > Assumptions:
    >   1. We will use a coordinate system (West-Up-North) that is rotated 120&deg; CCW about the vector (1, 1, 1) relative to the Opportunity dataset coordinate system. 
    >   2. The Opportunity dataset is (X-Y-Z) = (North-West-Up).
    >      1. A default state (i.e. identity quaternion transformation) for the BACK based on sensor placement would have the frontal plane of the body in (opportunity) XY-plane, with the head pointed in the (opportunity) -x-direction.
    >      2. Since our coordinate system has been transformed, the above statement now becomes "...frontal plane of the body in XZ-plane, with the head pointed in the -z-direction." (i.e., we need to make the person "lean back" 90&deg; in the Three.js visualizer.)
    >
    >      This translated to the following code:
    >      ```js
    >      /* Transform our coordinate system */
    >      q.premultiply(new THREE.Quaternion(0.5, 0.5, 0.5, 0.5));
    >      q.multiply(new THREE.Quaternion(0.5, 0.5, 0.5, -0.5));
    >    
    >      /* Rotate the back to the correct initial position */
    >      q.premultiply(new THREE.Quaternion(-0.707, 0, 0, 0.707));
    >      ```
    > &nbsp;
    > Results: (all orientations described in Three.js coordinates unless otherwise noted)
    > 
    >   1. When the person was walking or standing, their head was generally pointed in the -x-direction and often spun about the x-axis. Supposing the floor was the YZ-plane, this could be plausible. When they laid down, the back was in XY with the head pointing in +Y. Again, with the sideways floor proposition this could be possible if the person was laying on their side. Check around the 40-second mark. (However, I'd like to think that I've made a mistake and the person was laying on their back. This is only an uneducated guess, however.) 
    >   2. The only real issues with the model appeared around 600 seconds when activitied labeled stand occasionally involved the model rotating with their head pointing in +Y. This observation is **not** compatible with the YZ-floor supposition.
    >   3. This is a bit of a reiteration from #1, but I really feel like the model needs to be rotated 90&deg; about the body's vertical axis. Meaning that laying down is back-down. This is influenced by the motion around 660 seconds where the sit-stand action looks a lot like a person leaning forward and then standing up (except that the visualizer showed a person leaning to the left and then standing up.)

    **TEST 2**

    > Same assumptions as Test 1 but tried reversing the order of the code just in case: 
    > ```js
    > /* Rotate the back to the correct initial position */
    > q.premultiply(new THREE.Quaternion(-0.707, 0, 0, 0.707));
    > 
    > /* Transform our coordinate system */
    > q.premultiply(new THREE.Quaternion(0.5, 0.5, 0.5, 0.5));
    > q.multiply(new THREE.Quaternion(0.5, 0.5, 0.5, -0.5));
    > ```
    > Results:
    > Failed miserably. Looked obviously wrong.

    **TEST 3**

    > Mostly the same assumptions as Test 1, except ignored the transformation mentioned in Assumption 2(II). So there was a differnent transformation, as shown below:
    > ```js
    > /* Transform our coordinate system */
    > q.premultiply(new THREE.Quaternion(0.5, 0.5, 0.5, 0.5));
    > q.multiply(new THREE.Quaternion(0.5, 0.5, 0.5, -0.5))
    > 
    > /* Rotate the back to the correct initial position */
    > q.premultiply(new THREE.Quaternion(0, 0, 0.707, 0.707));
    > ```
    > Results:
    > Again, seemed to be basically a failure. Interesting note, the person seemed to be upside down in this test.

    **TEST 4**

    > Again, mostly same assumptions as Test 1, except assume the sensors are (East-North-Up). So head needs to be pointed in (opportunity) -Y which is (Three.js) -X. Keeping frontal plane in XZ.
    >
    > ```js
    > /* Transform our coordinate system */
    > q.premultiply(new THREE.Quaternion(0.5, 0.5, 0.5, 0.5));
    > q.multiply(new THREE.Quaternion(0.5, 0.5, 0.5, -0.5));
    >  
    > /* Rotate the back to the correct initial position */
    > q.premultiply(new THREE.Quaternion(-0.5, 0.5, 0.5, 0.5));
    > ```
    >
    > Results:
    > Extremely similar output to Test 1, except that this time the "floor" seemed to be the Three.js XY plane with the mannequin's head pointing out of the screen (+Z). Even with these assumptions the sitting/standing conundrum @660s and the laying while standing @600s still occured.


## 5/28/2021

 - During meeting, discussed how to apply transformations in order to correctly visualize the Opportunity quaternions. We are considering moving the camera as an alternative to applying some sort of change-of-basis transformation. 

 - Got the web server up and running on the virtual machine - it is available [here](http://vcm-20389.vm.duke.edu/). *Note: we are currently using the [hmv_test](github.com/jpiland16/hmv_test) repository; may consider switching to a new repository for collaboration.* 

   - Initially had some problems using `pm2` (process manager) but realized this was due to not using `sudo`. The correct commands are given below:
     - `sudo pm2 start server.js` starts our webserver if it is not already running
     - `sudo pm2 ls` list running processes
     - `sudo pm2 restart server` restarts the server
     - `sudo pm2 log` shows the log (`console.log`, `console.warn`, etc.)


## 5/27/2021 

 - Improved the lab module format, primarily to address warnings found when running in development build. 
   - Made it possible to utilize the development build for Three.js testing by including an `if` statement that pulls the files from the internet if the address in the browser is `localhost:3000` (the default when using `npm start`.)


 ## 5/26/2021 

  - Update to yesterday's log: I've decided it is going to be easier just to show on the screen which activity is occuring, since that is a part of the dataset.

    - I have plans to eventually develop a method to output this kind of data, such as graphs and text, to the screen.

  - Finished implementing a lab interface and wrote a [guide](https://github.com/jpiland16/hmv-scratchpad/blob/master/jonathan-lab-guide/hmv_test%EA%9E%89%20lab%20guidelines.md) on how to make a lab. 

## 5/25/2021 

 - Am looking into using some of the information provided int the label columns to help us get going. For example, using the MATLAB scripts to sort through the data quicker, I am going to try to use the following data from S4-ADL4.dat:

 |Start time (s)|Start line #|Locomotion     |
 |--------------|------------|---------------|
 | 40.733       | 1223       | Walking       |
 | 43.300       | 1300       | Standing      |
 | 44.166       | 1326       | Sitting       |
 | 46.600       | 1399       | Laying (down) |


## 5/24/2021

 - I've been testing some ideas for converting the Opportunity dataset quaternions into a usable format, based on the the information about sensor placement on the arms.

 - **Main idea**: I was thinking that, before applying an "Opportunity quaternion" to a part of our model, we should apply a transformation that makes a supposed "sensor" on the arm would have the orientation corresponding to an identity quaternion value [(XYZW) = (0, 0, 0, 1)]. Then perhaps we would need to apply a transformation to rotate the coordinate system, since the ENU system has the +z-axis pointing "up" while Three.js has the +z-axis pointing out of the screen. I tried applying these quaternions based on [Sam's notes](https://github.com/jpiland16/hmv-scratchpad/blob/master/sam-log-notes/sam-log.md#5232021) from 5/23/2021.  *Retrospectively, I'm not sure if any of this worked or was even correct, because the model still looked fairly unusual.*

   - What I tried:
     
     RUA, RLA needed to be oriented so the back of the hand faced the front of the screen (+Z) and so that the hand pointed toward +X (right side of screen)

      - Premultiplied `(XYZW) = ( sqrt(2)/2, sqrt(2)/2, 0, 0 )` before opportunity quaternion

     LUA, LLA needed to be oriented in the same manner:

      - Premultiplied `(XYZW) = ( -sqrt(2)/2, -sqrt(2)/2, 0, 0 )` before opportunity quaternion

     BACK needed to be oriented such that the spine pointed to left of screen with right shoulder pointing up

      - Premultiplied `(XYZW) = ( 0, 0, sqrt(2)/2, sqrt(2)/2 )` before opportunity quaternion

    Then post-multiplied this new quaternion by `(XYZW) = (0.5, 0.5, 0.5, 0.5)` in an attempt to rotate the coordinate axes 120&deg; CCW about the unit vector parallel to `(XYZ) = (1, 1, 1)`.
    
 This still did not work, as the mannequin's arms were intersecting its body and moving in unusual ways. The test data I used (first 720 lines of S4-ADL4.dat) appear to start with a walking rhythm - but I wasn't able to simulate the walking motion with any sets of quaternions I tried.


## 5/23/2021

 - Made some progress on implementing Sam's cone test.
 - Improved the slider so that it keeps moving when you change menu tabs and still pauses at the end if repeat is disabled.
    - This improved slider will probably appear in the viewport on our next iteration
 - Started developing a different test including some of the Opportunity data but could not seem to get the quaternions to provide a useful visual representation 
