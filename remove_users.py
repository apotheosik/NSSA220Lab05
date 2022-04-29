#! /usr/bin/python3

import os


message = "Removed from system."

# Remove users

with open("/etc/passwd") as file:
    for line in file:
        if int(line.split(":")[2]) > 1000 and int(line.split(":")[2]) < 2000:
            user = line.split(":")[0]
            command = "sudo userdel -r -f " + user
            print("{:15s} {:20s}".format(user, message))
            os.system("sleep 1")
            os.system(command)


# Remove groups

with open("/etc/group") as file:
    for line in file:
        if int(line.split(":")[2]) > 1000 and int(line.split(":")[2]) < 2000:
            group = line.split(":")[0]
            os.system("sudo groupdel -f " + group)


# Remove directories

os.chdir("/home")
os.system("sudo rmdir ceo")
os.system("sudo rmdir security")
