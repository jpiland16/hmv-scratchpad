---
tags: [hmv-scratchpad]
title: jonathan-log
created: '2021-05-24T17:36:41.689Z'
modified: '2021-05-26T21:26:27.013Z'
---

Note: all quaternions in these notes will be given in XYZW format.

## 5/23/2021

 - Made some progress on implementing Sam's cone test.
 - Improved the slider so that it keeps moving when you change menu tabs and still pauses at the end if repeat is disabled.
    - This improved slider will probably appear in the viewport on our next iteration
 - Started developing a different test including some of the Opportunity data but could not seem to get the quaternions to provide a useful visual representation 

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

## 5/25/2021 

 - Am looking into using some of the information provided int the label columns to help us get going. For example, using the MATLAB scripts to sort through the data quicker, I am going to try to use the following data from S4-ADL4.dat:

 |Start time (s)|Start line #|Locomotion     |
 |--------------|------------|---------------|
 | 40.733       | 1223       | Walking       |
 | 43.300       | 1300       | Standing      |
 | 44.166       | 1326       | Sitting       |
 | 46.600       | 1399       | Laying (down) |

 ## 5/26/2021 

  - Update to yesterday's log: I've decided it is going to be easier just to show on the screen which activity is occuring, since that is a part of the dataset.

    - I have plans to eventually develop a method to output this kind of data, such as graphs and text, to the screen.

  - Finished implementing a lab interface and wrote a [guide](https://github.com/jpiland16/hmv-scratchpad/blob/master/jonathan-lab-guide/hmv_test%EA%9E%89%20lab%20guidelines.md) on how to make a lab. 

    
