# NiryoRobot-OpenCV-ColorSorting
I have recently worked with the Niryo Robotic Arm (NED2). The arm is equipped with a camera and was capable of successfully sorting 
square-shaped objects based on color.

NiryoStudio should be installed beforehand, as it will be used to create the "workspace". Workspace is the area from which the arm will pick up the objects after detecting them. Connect the Robot with the NiryoStudio and create a workspace by going to Library > Workspaces > Create new.

Refer to the following link of Niryo Robot's documentation: [NED2 Documentation](https://docs.niryo.com/dev/pyniryo/v1.0.5/en/source/vision/image_processing_overview.html) 


## Demo Video
Click on the image below to watch the youtube video of the hardware

[![Watch the video](https://github.com/EhtishamAshraf/niryoRobot-OpenCV-ColorSorting/blob/main/1-Arm.jpeg)](https://youtu.be/g6igqMyEAQ4)

## Hardware Setup
The arm is equipped with a camera, and raspberry pi, and servo motors. The conveyor belt has an IR sensor which is used to detect the object's presence in the workspace.

# Libraries required for the Simulator
The robotic arm only required pyniryo library to operate.

### Installing the Library

pyniryo:
```bash
pip install pyniryo
```

# Flowchart
The below figure shows the flowchart of the system:
![FlowChart](FlowChart.png)

# Algorithm Flowchart
The algorithm works as follows:
1. Capture an Image,
2. detect markers
3. extract workspace
4. extract color features of the object
5. find object's position w.r.t to the Robot
6. Move the arm to pick up the object

![Algorithm FLowchart](AlgorithmFlowChart.png)


The markers need to ber perfectly detected for the algorithm to work
![Detected Markers](Detected_Markers.jpg)

Once the markers are detected perfectly, the workspace is extracted
![Workspace Extraction](https://github.com/EhtishamAshraf/niryoRobot-OpenCV-ColorSorting/blob/main/Extracted_Workspace.jpg)

After extracting the workspace, we can apply Image Processing techniques, to find the object and detect its color.
An RGB Image containing different color objects as shown below
![RGB Image](https://github.com/EhtishamAshraf/niryoRobot-OpenCV-ColorSorting/blob/main/RGB%20Images.png)
We can use color thresholding to detect the objects in the image, then dilate the images to close small gaps in the objects.
![Dilated Images](https://github.com/EhtishamAshraf/niryoRobot-OpenCV-ColorSorting/blob/main/DIlated%20Images.png)

Then we can find the contours of the detected objects and subsequently determine the centroid of each object. Once the centroid is identified, the position of the object within the workspace can be calculated. Using pyniryo functions, the position of the object relative to the NED2 Arm coordinate system can then be determined.
![Contours and Centroid Detection](https://github.com/EhtishamAshraf/niryoRobot-OpenCV-ColorSorting/blob/main/Contours_with_Centroids.png)
