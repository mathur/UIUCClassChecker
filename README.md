#UIUC Class Checker#

Checks every (user defined duration) to see if spots in a certain class open up. When they do, text you via Twilio's API!

##Installation##

###Step 1###

In the right column of the GitHub repository, click on "Download ZIP" and extract the directory somewhere you can access with a terminal.

###Step 2###

Install the standard python runtimes for your system. This differs from system to system, and in some cases, may even be provided with your operating system.

    sudo apt-get install python

###Step 3###

Install pip and easy_install, both of which will make installing dependencies both now and in the future easier.

    sudo apt-get install python-setuptools python-pip

###Step 4###

Use both to install the needed non-standard dependencies.

    source venv/bin/activate
    pip install -r requirements.txt

###Step 5###

Set up a twilio account at http://twilio.com (the free trial works fine too). Open the file "twilio_accnt.py" and change the information between the two brackets for all 3 fields, getting the information to fill those fields from your account on your account's page.


Thats it! All dependencies are now installed and you should be able to run the script.

##Usage##

To run the script, use the following command:

    source venv/bin/activate
    python script.py

The script will prompt you for several inputs before starting the looping process:

####Enterprise Username####
The username used to log into your Enterprise account on UIUC's Self-Service portal.

####AD Password####
Your Active Directory (AD) Password

####Course Subject (Subj)####
The "Subject" code in the class. For example, for the class CS 173, the "Course Subject" would be "CS" (without quotes)

####Course Number (Crse)####
The "Number" code in the class. For example, for the class CS 173, the "Course Number" would be "173" (without quotes)

####Your Phone Number####
The phone number you'd like to receive texts to if your class opens up. Leave blank if you don't want to receive text messages. 

####Time Interval (min)####
The time the program will wait in between requests to check the status of the course. The higher the better, since the University could lock you out of using software like this if they catch you. Something like 30 minutes should do the trick.
