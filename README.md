# Tello_Drone_Controller

In the **Main.py** file found in this repo you are going to find what you need to succesfully recognize a controller input connected to your device, with a usb connection and succesfully get the input data that the controller provides by moving joysticks or pressing buttons.

For this to work you are going to any IDE for python that there is available or essentially any programmer editor that runs the code, but I recommend an IDE it just makes is simpler to work with python and any external libraries you might need. Talking about libraries here is what you need for this to work.

> Libraries/Packages for Python

- pygame
  - This is essentially what you are going to use to update the state of the drone with the controller.
  - Install required either from IDE or from npm.
- tellopy
  - This contains the api to controll the drone and access any data that the drone provides.
  - Install required either from IDE or from npm.
- sys
- time
- traceback
- pygame.locals
- pygame.key
  - The packages above you need to debug or deal with errors in the program.
  
> Main.py

We runned this programm usign a **Windows system** using an IDE called **PyCharm** this IDE is free to download but you need a license for it, luckily if you are a student there is a free version for it here is the link to downloaded - [PyCharm](https://www.jetbrains.com/pycharm/) - and here is the link for the student license - [Student_license](https://www.jetbrains.com/community/education/#students) - and in case you need python installed on your system here is the link - [Python](https://www.python.org/downloads/) - Alright now that we got all the system requirements out of the way this is how it works.

First we have to get the controller input up and running in the programm, this can be found on line 244 and below, this code will pop up new window on your system that will display all the buttons and axis available on the controller connected to your system along with the name of the controller that we will be using later on. It looks something like this:

![Live Controller Input](/assets/images/controller_input.png)

Then we have the rest of the code which is from line 1 - 240, right now is commented out becuase I think the focus at first is getting the controller to work but that controlls the drone via wifi through a controller, we tested this out using a **Xbox Controller** and a **PS4 Controller** the layouts are defined as classes in the code and we later call these classes depending on the name of the controller to make calls to the drone wether to take off or move in certain way.

Within this code we have data comming back from the drone that displays the height, speed, wifi connection among things. Now since the drone does not provide a gps we can calculate or essentially generate coordinates from a starting point which is where the drone started flying and using the speed towards were the drone is moving.
