"""
                            "Object Sorting based on Colour and Shape using Niryo Robotic Arm (NED2)"
Details:
1.  Either create your own workspace, or use a workspace created by default.
    To create workspace: open NiryoStudio App, go to Library > Workspaces > Create new
2. Open NiryoStudio, and connect to the Niryo Robot

3. Code sorts objects based on the color (Red, Green, and Blue).
4. It only works with "square" shaped objects

5. Conveyor belt is used to move objects to the workspace
6. IR Sensor is also used to stop the objects within the workspace

References:
    https://docs.niryo.com/dev/pyniryo/v1.0.5/en/source/examples/examples_vision.html
    https://docs.niryo.com/dev/pyniryo/v1.0.5/en/source/vision/image_processing_overview.html
"""

from pyniryo import *   # Import Library

# Create an object "robot" of the NiryoRobot class, IP address for hotspot mode: "10.10.10.10"
robot = NiryoRobot("10.10.10.10")

workspace_name = "convayeur_belt"  # Using the ready-made conveyor belt workspace

# Calibrating robot, updating gripper, and opening it.
robot.calibrate_auto()
robot.update_tool()
robot.release_with_tool()

# Defining Sensor Pin, and setting Conveyor Belt
sensor_pin_id = PinID.DI5
conveyor_id = robot.set_conveyor()


# Function to move robot to a specific Pose
# PoseObject is an object which allows to store all poses’ (x, y, z, roll, pitch, yaw) in one single instance
def move_to_pos(x_, y_, z_, roll_, pitch_, yaw_):
    position_move = PoseObject(
        x=x_, y=y_, z=z_,
        roll=roll_, pitch=pitch_, yaw=yaw_
    )
    robot.move_pose(position_move)


robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.BACKWARD)  # Run Conveyor Belt

square_expected = ObjectShape.SQUARE  # Define Shape of the objects
red_count, green_count, blue_count = 0, 0, 0  # Setting variables to count the objects of each color

while True:
    robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.BACKWARD)  # Running Conveyor Belt
    move_to_pos(0.1908, -0.1454, 0.3412, -2.245, 1.513, -2.999)  # Moving to observational pose

    # Check if object is in the workspace
    # Wait in this while loop, unless an object has been detected by Sensor, "if object is detected the loop will break"
    while robot.digital_read(sensor_pin_id) == PinState.HIGH:
        robot.wait(0.1)
    robot.stop_conveyor(conveyor_id)  # Stop conveyor belt as soon as object is detected
    print("conveyor stopped")

    #   "robot.detect_object" is used to detect objects within the workspace

    obj_found1, pos_array1, shape1, color1 = robot.detect_object(workspace_name,
                                                             shape=square_expected,
                                                             color=ObjectColor.GREEN)
    obj_found2, pos_array2, shape2, color2 = robot.detect_object(workspace_name,
                                                             shape=square_expected,
                                                             color=ObjectColor.BLUE)
    obj_found3, pos_array3, shape3, color3 = robot.detect_object(workspace_name,
                                                             shape=square_expected,
                                                             color=ObjectColor.RED)
    print("GREEN color detected: ", color1)
    print("BLUE color detected: ", color2)
    print("RED color detected: ", color3)

    if obj_found3 or obj_found1 or obj_found2:  # If an object is found, stop conveyor
        robot.stop_conveyor(conveyor_id)  # Keeping conveyor stopped

    """ 
    1.  When Green or Blue color objects are present in the workspace, the RED color was mistakenly detected too, 
        So the below If condition makes sure that whenever RED color is detected mistakenly, 
        the Robot only sees the other color (Green or Blue).
    2. "robot.vision_pick" function is used to pick the object from the workspace.
    """
    if color3 == ObjectColor.RED and (color1 == ObjectColor.GREEN or color2 == ObjectColor.BLUE):
        color3 = ObjectColor.ANY
    else:
        # Making a vision pick
        obj_found3, shape3, color3 = robot.vision_pick(workspace_name,
                                                       shape=square_expected,
                                                       color=ObjectColor.RED)
    print("color found red: ", color3)

    obj_found1, shape1, color1 = robot.vision_pick(workspace_name,
                                                shape=square_expected,
                                                color=ObjectColor.GREEN)
    print("color found green: ", color1)

    obj_found2, shape2, color2 = robot.vision_pick(workspace_name,
                                                shape=square_expected,
                                                color=ObjectColor.BLUE)
    print("color found blue: ", color2)

# Calculate the current "pose" of the Robot, and move the arm a little up so that it doesn't collide with objects
    current_pose = robot.get_pose()
    move_to_pos(current_pose.x, current_pose.y, current_pose.z+0.15, current_pose.roll, current_pose.pitch, current_pose.yaw)  # go a little up

# Based on the color of the found object, place the object at it's fixed location.
# Robot will stack the objects based on color, give offset in the z-axis using: (0.084+(red_count*0.01))
    if obj_found3 and color3 == ObjectColor.RED:
        red_count+= 1
        print("Num of red objects detected", red_count)
        move_to_pos(0.0025, -0.3556, 0.0922+0.25, -0.416, 1.530, -1.929)  # go to place pose, & a little up
        move_to_pos(0.0398, -0.3075, 0.084+(red_count*0.01), 0.873, 1.550, -0.665)  # object placing pose
        robot.release_with_tool()
        move_to_pos(0.0398, -0.3075, 0.0946+0.25, 0.873, 1.550, -0.665)  # taking a little up
    elif obj_found1 and color1 == ObjectColor.GREEN:
        green_count+=1
        print("Num of green objects detected", green_count)
        move_to_pos(0.0025, -0.3556, 0.0922+0.25, -0.416, 1.530, -1.929)  # go to place pose, & a little up
        move_to_pos(-0.0093, -0.2337, 0.0925+(green_count*0.01), -2.782, 1.479,1.961)  # object placing pose
        robot.release_with_tool()
        move_to_pos(-0.0093, -0.2325, 0.0921+0.25, -2.782, 1.479,1.961)  # taking a little up
    elif obj_found2 and color2 == ObjectColor.BLUE:
        blue_count+=1
        print("Num of blue objects detected", blue_count)
        move_to_pos(0.0025, -0.3556, 0.0922+0.25, -0.416, 1.530, -1.929)  # go to place pose, & a little up
        move_to_pos(-0.0560, -0.2967, 0.0938+(blue_count*0.01), -1.871, 1.481, 2.917)  # object placing pose
        robot.release_with_tool()
        move_to_pos(-0.0560, -0.2967, 0.0938+0.25, -1.871, 1.481, 2.917)  # taking a little up
