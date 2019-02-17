# Webreg-Script

Big thanks to Vaibhav Verma for his amazing project sniper which is the foundation for this project.

Webreg-Script automatically checks Rutgers Schedule of Courses for open classes and registers users for classes they want. I
set it up to check Rutgers SOC every twenty seconds and when the courses I wanted were open, it would log me into webreg, register
me for each course, take a screen shot of the webpage and email me the result letting me know if the script registered me
before anyone else could.

A little background history about why I made this script. When I should have been studying for my finals for the Spring 2018
semester I was waiting for webreg to allow people with my quantity of credits to register for classes. When it did I failed
to get into any of the CS classes that I wanted. I was so frustrated I could not focus on studying and I was very apprehensive
about leaving my entire Fall 2018 semester to the SPN process and risk not graduating on time. I also knew there was a
slim chance I'd get into the courses by using http://sniper.rutgers.io/ competing with all the other people using it or
by using any of its monetized clones.

With some new code for handling emails locally, some hardcoded classes I wanted to be registered for, and some web automation
libraries, I took Vaibhav's logic for checking for open courses and parsing json data and made a raspberry pi do the rest of the
work for me. I ended up getting into 4 CS classse for this semester. My friend also used the script to get into 2.

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



