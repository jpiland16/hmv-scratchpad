## Hi.
You want to maintain or update this project. What do you need to know?

## Prior knowledge
It will be helpful to be familiar with the following programming languages, data formats, libraries, etc.
- Javascript - this app is primarily Javascript.
- Python - the app uses Python for some server-side calculations.
- JSON - important data is stored in JSON format.
- React - the client web app is built using React.
- Quaternions - quaternions are used to manipulate the model.
- [Xsens IMU sensors](http://www.opportunity-project.eu/system/files/MTi_and_MTx_User_Manual_and_Technical_Documentation.pdf) - multiple popular human activity recognition datasets, including OPPORTUNITY, use Xsens IMU sensors to collect data.
- [The OPPORTUNITY dataset](https://archive.ics.uci.edu/ml/datasets/OPPORTUNITY+Activity+Recognition) - the project was created with this dataset as the primary example.
- HTTP - the client gets files and some other data from the server using a (mostly) RESTful HTTP API.
- Web sockets - the file viewer page relies on web sockets for updates from the server.
- Node.js - the server uses the Node framework to handle incoming requests and to manage library dependencies.
- The layout of the [website](https://vcm-20389.vm.duke.edu/) - 🤔 go figure.
- THREE.js - The visualizer uses THREE.js to display a 3D scene to the user.
- JSDoc - an API documentation generator for JavaScript.

## How to run the app locally
- Option 1 (Recommended): Run the client in dev mode and server locally
    1. Open two instances of the command prompt in the root directory of the `hmv_test` repository.
    2. On the first terminal instance, use `npm start` to start the client. This should take several seconds, generate a list of complaints, and then open a browser window with the app's home page.
    3. On the second terminal instance, use `node server` to start the server. It should print `Directory rescan requested at <date and time> GMT` and hang as it waits for a client to ask for files. 
    4. You can now test the server. Changes to the client will automatically be applied when you save them, but changes to the server (`server.js`) need a restart.

- Option 2: Run the client in production mode and serve it
    1. Open a terminal in the project root directory.
    2. Use the command `npm run build` to create the production build of the React application. This should around a minute.
    3. Use `node server` to run the server, and use `https://localhost:<PORT>` to connect to it, where PORT is the port number that the server says it is listening to upon startup. (As of 7/22/2021, this is port 443.)
    4. You can now test the server as it behaves in a production environment. Always try this before pushing a change to master. You will have to re-build the client (step 2) to see the result of any changes you make.

- Option 3: Run the client in dev mode with no server
    1. Go to the start of the `subscribeToFile` function in `NetOps.js` and set the constant `SKIP_SOCKET` to `true`.
    2. Open the command prompt in the project root directory.
    3. Use `npm start` to start the client.
    4. You can now use the server to access the sample file `S4-ADL4.dat` from the OPPORTUNITY dataset. For other files you will need to run the server (see Option 1). Set `SKIP_SOCKET` back to `false` to connect to the server.




## The meat and potatoes: the Viewport
- The viewport's responsibility is to:
    1. Display the 3D scene containing the model
    2. Manipulate the model based on the target data
    3. Display the status of the target data: Whether it is still loading, or waiting on the model to load, or if an error was encountered
    4. Allow the user to choose the target data by presenting an interface for making an informed decision
    5. Allow the user to choose which time slice of the target data to display
    6. Allow the user to navigate to any other part of the site through one or more pages

How does the viewport achieve these goals?

(1) is handled by Visualizer.js. (2) is handled by the Viewport, Animator, Reset, and SceneInitializer. (3) is handled by NetOps and FileViewer. (4) is handled by Menu. (5) is handled by PlayBar. (6) is handled by Menu.

### Encyclopedia of Viewport's property set
- Page layout (Meta-menu) properties: Describe the current status of the menu in the interface, for adjusting components that need to resize themselves both inside and out of the menu.
    - menuIsOpen
    - menuIsPinned
    - selectedPanel
    - expandedItems
- File selection properties
    - selectedFile: An Object with a fileName and displayName property which represents the file currently being viewed. Has default filename "" (empty) and default display name "None".
    - fileStatus: An Object with a status and message property. The status can be one of an enumerated number of types (described in the doc for NetOps), and the message is relevant for errors.
    - clickFile: A Function to run when a new file is selected. Right now this is done using the menu.
    - files, lastFiles, fileMap: Their purpose isn't clear, but it seems that they hold the currently selected file. 'files' holds it in its 'current' field, while lastFiles and fileMap put the current file in index 0.

## Data format
The `/files/user-uploads/` directory contains all files available to the user. A valid, viewable file contains `quaternion_data.dat` and `metadata.json` files. 

The quaternion data file contains (w,x,y,z) quaternions in 4-column groups, sorted in order of time such that the first row is displayed first. The first column is treated as the 'time' column in milliseconds and is displayed on the right of the play bar in the visualizer interface.

The metadata file carries the following info:
- `name`: The name of the dataset. Not currently used, but was formerly used for assigning one metadata configuration to multiple data files.
- `displayName`: The name that should be shown to the user in the file selection process.
- `globalTransformQuaternion`: A quaternion to pre-multiply to every bone's orientation before the data quaternions are applied.
- `targets`: A list of objects representing the individual sensors. Each records the following data:
    - `bone`: The name of the bone for which the sensor determines the orientation. This is one of the following enumerated names, sorted topologically below:
        - ROOT (navel)
        - BACK
        - RUL (right upper leg)
        - RLL (right lower leg/shin)
        - RSHOE (right shoe)
        - LUL (left upper leg)
        - LLL (left lower leg/shin)
        - LSHOE (left shoe)
        - RUA (right upper arm)
        - RLA (right lower arm/forearm)
        - LUA (left upper arm)
        - LLA (left lower arm/forearm)
    - `type`: The type of orientation transformation to apply to the bone. As of 7/22/2021, this is always "Quaternion".
    - `column`: The first column in `quaternion_data.dat` that contains the actual transformation values. Column indices begin at 0 for the first column.
    - `localTransformationQuaternion`: A quaternion that is applied to the sensor's bone after the global transformation and before the data.
    
## How data is processed
The visualizer uses a standardized format of (w,x,y,z) quaternions to determine bone orientation. The following process determines these quaternions from the raw data.

The user sends the raw quaternion data (usually in the form of the actual dataset file) to the server, alongside some metadata from the upload form describing the column number and data type corresponding to each sensor.

This takes the form of a POST request to `/api/postform` carrying a JS FormData object, which is JSON that can have a file as its value. `server.js` uses the [formidable](https://www.npmjs.com/package/formidable) library to separate the form data and the file before passing them to `FormFileProcessor.js`, which calls `multi_sensor_fuser_obj.py` and passes in the file data using its `stdin`. This Python program instantiates the appropriate `DatatypeHandler` for each sensor. After a `DatatypeHandler` converts the relevant columns to quaternions, the Python program returns the aggregate data, which is then combined with a JSON metadata file and stored in the `/files/user-uploads/` directory.

## How processed data is applied to the model
`Animator.js` and `ModelOps.js` handle manipulating the model to show data.

`Animator.js` is a renderless component which checks on each re-render whether the selected time slice `timeSliderValue` has changed. When a file is loaded and the time slider changes, it initializes the data quaternion for each bone and calls `ModelOps.batchUpdateObject` to apply them.

`batchUpdateObject` then applies each quaternion. Additionally, it calculates the 'local' and 'global' quaternions associated with the new orientation. 
The 'global' quaternion is the orientation with respect to the global THREE.js coordinate system, such that the identity quaternion (wxyz)=(1,0,0,0) would point the bone in the x direction, with its local up facing in the y direction.
The 'local' quaternion is the orientation with respect to the bone's parent-the bone whose end it is attached to. A local quaternion of (1,0,0,0) means that the bone points in the same direction as its parent (for the bone ROOT, which has no parent, we expect global and local orientation to match).

The utility functions `getGlobalFromLocal` and `getLocalFromGlobal` transform between the two by multiplying a quaternion by the orientations of its parent, grandparent, etc., or by multiplying by their inverses.

# Important points that have to be mentioned somewhere
- There is a server-side and client-side aspect. The current divide is that the server processes the raw data into quaternions representing bone orientation, and the client uses these alongside the metadata to do further calculations.
    - Why have we made this divide? There is not a guiding principle. However, I (Sam) hesitate to change it because tinkering with metadata files is necessary when displaying new datasets.
