# Webreg-Script

This script automatically opens the Rutgers course registration website, webreg, logs the user in and registers them for any class which just opened as a result of someone dropping the course. Its a nice set-it and forget-it solution to getting into closed courses and it gives the user peace of mind because it checks with a frequency faster than any human could and when a course opens up it registers the user for the class faster than anyone else can manually.

I wrote this because I needed a solution for getting into closed classes that registered me for classes faster than people using RUSniper.

Big thanks to Vaibhav Verma for his project sniper which provided the code for checking on classes open/closed status.


***FYI I dilberately did not include a requirments.txt and I also removed several necessary imports that would make this code
functional. I did this because, if everyone could just pull this code and run it, it would defeat the purpose of having
the script, and more importantly because widespread use of it may effectively ruin the Rutgers SOC api because the scripts
would basically ddos the school. I would rather post the code and leave it as a challenge (it shouldn't be too hard) to others
to figure out whats needed for requirements, imports, and some trickery in the way of overcoming an unforseen cron issue than not
share it at all.***

I will give some hints as to whats missing however and what else is needed to get this thing going,

wARNING: I take no responsability for what happens if/when you register for courses you didn't intend etc etc

1. You need to create a Windows live account if you don't already have one and either store you password and username
for the account in your distros enviornment variables or store them in plain text (not recommended) in the MY_ADDRESS and
PASSWORD variables in cron.py    **Gmail will not allow you to log into your email to use it to send mail from an automated script

2. You need to store your netid and password in your distros enviornment variables or store them in plaintext (not recommended)
in lines 147 and 149 respectively

3. You need to comment out my_classes on line 33 and input your desired course numbers and section numbers in the my_classes line on
line 32.

4. You need to change the department number in poll on line 168 in cron.py to whatever department number your trying
to get classes in.

**Changes number 3 & 4 are just getting rid of a test to see if the script is working because 700:133 interests me and because
its usually not full.

5. On line 9 in soc.py you need to change the 9 to the correspond semester and the year to whatever year it is,

Here are the corresponding semester codes 
//  winter: 0
//  spring: 1
//  summer: 7
//  fall: 9

you can also change level to G for graduate classes

6. In mycontacts.txt change name to your name and name@email.com to your email.com

7. You obviously have to setup cron to run the script at whatever frequency you want - see internet for more details.

8. You need to figure out what requirements need to be installed on your system with pip3 - you can do that by reading the code

9. You need to figure out what imports are needed - you can do that by checking the errors

10.  If you get an error likes this,

"""
Message: The browser appears to have exited before we could connect. If you specified a log_file in the FirefoxBinary constructor, check it for details.

Traceback (most recent call last):
  File "/home/brian/Programming/Python/SOC/Webreg-Script/cron.py", line 175, in <module>
    poll(700)
      File "/home/brian/Programming/Python/SOC/Webreg-Script/cron.py", line 169, in poll
    driver.quit()
UnboundLocalError: local variable 'driver' referenced before assignment
 """

good job your almost there! Google "X cron browser" assuming your not using wayland.

11. Once you learn about cron and X and potential solutions - be clever and just use cron to start a chain reaction



This code was written in debian stretch and ported to a raspberry pi where it was left to run for several weeks.
Rasbian is based on debian so it ran the same on my laptop and my raspberry pi.



