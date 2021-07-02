# Welcome to the Human Activity Visualizer

The Human Activity Visualizer is a free visualization tool that reads wearable sensor measurements taken over time and displays the activities of the sensor wearer via a virtual 3D model. Currently, the model is centered on the origin and changes in global position are not displayed. To try out the visualization tool on a sample dataset, click the 'View OPPORTUNITY Dataset' button and select a trial to view. To view your own uploaded dataset, the guide below will explain step-by-step how to get started.

## Uploading and Viewing Your Own Datasets

The Human Activity Visualizer requires a specific file format and only interprets certain types of sensor data. Before uploading your file, ensure that it meets the following format and data specifications. 

Your file must: 
  - be a .dat file
  - be sorted into columns
  - not contain headers

The data in your file must:
  - include time values in milliseconds
  - include global quaternions or acc+mag+gyro values taken over time
    - Note: other measurement types can be included in the uploaded file but will be ignored
  - be ordered so that columns for any quaternion values are in WXYZ order for each sensor
  - be ordered so that columns for any acc+mag+gyro values are in XYZ order for each sensor

For example, the column order for a dataset containing quaternion measurements for the back and upper left arm (ULA) would be:
#### Example 1
| Time (ms) 	| BACK Quat. W 	| BACK Quat. X 	| BACK Quat. Y 	| BACK Quat. Z 	| ULA Quat. W 	| ULA Quat. X 	| ULA Quat. Y 	| ULA Quat. Z 	|
|-	|-	|-	|-	|-	|-	|-	|-	|-	|

The column order for a dataset containing acc+mag+gyro measurements for the back would be:
#### Example 2
| Time (ms) 	| BACK Acc. X 	| BACK Acc. Y 	| BACK Acc. Z	| BACK Mag. X 	| ULA Mag. Y 	| ULA Mag. Z 	| ULA Gyro. X 	| ULA Gyro. Y 	| Gryo. Z |
|-	|-	|-	|-	|-	|-	|-	|-	|-	|- |

When the file has been correctly formatted, click the 'Upload File' button on the main page, select your file(s), and enter the necessary calibration information. For each sensor, select the sensor location, data type, and start column of each data type (indexed at zero).

For Example 1 you would input:
  - Time Start Column: 0
  - Sensor Type: BACK
    - Data Type: Quaternion
    - Start Column: 1
  - Sensor Type: ULA
    - Data Type: Quaternion
    - Start Column: 5
    
For Example 2 you would input:
  - Time Start Column: 0
  - Sensor Type: BACK
    - Data Type: Acc+Mag+Gyro
    - Start Column: 1

Check that all of the information has been entered correctly, and click the 'Submit" button at the bottom of the form. A landing screen will appear when the file has been successfully submitted. Select the file you want to view first and continue to the visualizer page. Once the file has downloaded, press the play button the in bottom left corner of your screen to begin the animation.

To view a different upload file, click on the hamburger icon in the top left corner and you will see the file directory. In the user-uploads folder, you will be able to access any additional files you uploaded. These files are only accessible by you but will be deleted from the server after two days.
