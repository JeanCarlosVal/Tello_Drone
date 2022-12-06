# Tello_Drone_Controller

> Description

In this repository you are going to find a python program to connect to a drone called **TELLO** and be able to controll it with a controller connected via usb (currently the only controller supported is the Xbox Controller). What this program does is connect to drone from there the user will be prompted to enter some information about them and then when user submits, the drone will be available to receive commands from the controller. When the user finishes flying the drone the program will upload user and drone data to a dynamodb table hosted on aws.

> Libraries and Packages

This program uses:
- os ( to access evironment variables )
- boto3 ( SDK to use aws services )
- pygame ( to display user Interface and drone information on a screen )
- djitellopy from Tello ( to be able to connect to the drone and send/receive data to drone )

> Structure

I have created some classes and initialized them as objects on the program, there is the **Input** class that extends to **UserInputPrint** class that together have functions to render input fields and store the values on variables that can be access within the class. The **DroneInfoPrint** class that all it has is some functionality that makes it easier to render information about the drone.

> DynamoDB

[DynamoDB implementation](https://github.com/JeanCarlosVal/Tello_Drone/tree/main/db)

> djitellopy

Here is a really usefull documentation from [djitellopy](https://djitellopy.readthedocs.io/en/latest/) package, I recomend going through the implementation beacause it give you a better understanding of what is happening behind the scenes and also what is being send to the drone, this package uses the original Tello sdk its just a wrapper around the original sdk.

