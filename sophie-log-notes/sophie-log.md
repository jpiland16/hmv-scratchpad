---
tags: [hmv-scratchpad]
title: sophie-log
---
## 5/21/2021
- Researched [Quaternions](https://www.youtube.com/watch?v=SCbpxiCN0U0&list=PLW3Zl3wyJwWOpdhYedlD-yCB7WQoHf-My&index=32)
- MVN Sensor Software Notes
  - [link](https://www.researchgate.net/profile/Per-Slycke/publication/239920367_Xsens_MVN_Full_6DOF_human_motion_tracking_using_miniature_inertial_sensors/links/0f31752f1f60c20b18000000/Xsens-MVN-Full-6DOF-human-motion-tracking-using-miniature-inertial-sensors.pdf 
)
  - INTRODUCTION
      - mechanical trackers worn by the user
        - provide joint angle data
        - kinematic algorithms use this data to determine bedy posture - LOOK INTO INVERSE KINEMATICS
      - mechanical trackers contain gyroscopes, accelerometers, and magnetometers
        - accelerometers find "down" using acceleration due to gravity
        - magnetometers sense horizontal plane using earth's magnetic field.
        - accelerometers & magnetometers combine to correct drift from of the gyroscope measurement 
      - each body segment's orientation and position can be estimated by integrating gyroscope data    and double integrating the accelerometer data
      - result is integration drift that must be accounted for by factoring in magnetometer
      - LOOK UP INERTIAL NAVIGATION ALGORITHMS 
  - WORKING PRINCIPLES 
     - initial pose is unknown so sensors must be calibrated
     - need to find sensor to segment alignment
     - Calibration GBq=QSq x BSq*(complex comjugate)
       - GBq=orientation of segment(body) wrt world
       - GSq=orientation of sensor wrt world
       - BSq=orientation of  sensor wrt body
         - This would make BSq*=orientationf of body wrt sensor?
   - INERTIAL TRACKING (could be helpful when we don't have automatically generated quaternion to work with)
      - gyroscopes provide change in angle wrt inital angle
        - GSqt=integral(1/2GSqt x omega
    
## Background Research
- Read through documentation from previous project
- Reviewed notes on Linear Algebra
- Researched IMUs
    - [Accelerometers](https://www.youtube.com/watch?v=9WAckt2vrrQ)
    - [Gyroscopes](https://www.youtube.com/watch?v=ti4HEgd4Fgo)

