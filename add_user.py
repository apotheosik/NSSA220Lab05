#!/usr/local/bin/python3
import os
import csv
"""Chris Sequeira
    25 April 2022
    User adding and removing script"""

NO_OUT = " >/dev/null 2>&1"

"""If the C shell does not exist, install it"""
def cCheck():
    if os.system("which csh" + NO_OUT) == 0:
        os.system("yum -y install tcsh"+ NO_OUT)

"""strip and save header via csvreader
    @return list of user rows"""
def dataIntake():
    users = []

    with open("linux_users.csv", 'r') as userCSV:
        reader = csv.reader(userCSV, delimiter=",")
        next(reader) #skip header

    #one list element per person
        for row in userCSV:
            row = row.split(',')
            row.pop() #remove newline

            try:
                row.index("")
            except ValueError: #if the non value is not present, add entry to list
                users.append(row)
            else:
                print("Employee ", row[0], " unable to be added due to insuffient information.")

    return users


"""perform data validation and create users
    @param list of users with attributes"""
def createUsers(userList):
    print("Adding new users to the system.")
    print("Please note: The default password for all users is password.")
    print("For testing purposes, change the password to l$4pizz@")

    specialCharsAcceptableList = [3, 4] #columns 3 and 4 do not need '-' omitted.

    for userIndex in range(len(userList)): # userList[userIndex] = ['aa',...], [...
        for argumentIndex in range(len(userList[userIndex])): #userList[userIndex][argumentIndex] = 'aa', 'ab',

            #turn to lowercase version
            userList[userIndex][argumentIndex] = userList[userIndex][argumentIndex].lower()

            #if character is not a letter, omit
            for characterIndex in range(len(userList[userIndex][argumentIndex])): #userlist[userIndex][argumentIndex][letterIndex] = 'a'...
                if argumentIndex in specialCharsAcceptableList:
                    break
                if not ord(userList[userIndex][argumentIndex][characterIndex]) in range(ord("A"), ord("{")): #if character is not a letter
                    if not ord(userList[userIndex][argumentIndex][characterIndex]) in range(ord("0"), ord(":")): #if character is not a number
                        print("Before: ", userList[userIndex][argumentIndex])
                        userList[userIndex][argumentIndex] = userList[userIndex][argumentIndex].replace(userList[userIndex][argumentIndex][characterIndex], '')
                        print("After: ", userList[userIndex][argumentIndex])

            #must create dept directories before making home folders, but after removing special chars
            if argumentIndex == 5:
                os.system("mkdir /home/"+ userList[userIndex][5] + NO_OUT)

        #define arguments
        eID = userList[userIndex][0]
        lName = userList[userIndex][1]
        fName = userList[userIndex][2]
        office = userList[userIndex][3]
        phone = userList[userIndex][4]
        dept = userList[userIndex][5]
        group = userList[userIndex][6]
        username = fName[0] + lName
        shell = "/usr/bin/bash"
        password = "password"
        homeDir = "/home/" + dept + "/" + username
        #create group if it does not exist
        groupExistCheck = os.system("getent group " + group + NO_OUT)
        if groupExistCheck == 0:
            os.system("groupadd " + group + NO_OUT)

        #change from default /usr/bin/bash to /usr/bin/csh for office members
        if group == "office":
            shell = "/usr/bin/csh"

        #if user exists, add counter
        usernameCounter = 0
        while True:
            userExistCheck = os.system("id -u \"" + username + "\"" + NO_OUT)
            if userExistCheck == 0:
                #remove previously appended counter, futureproof
                for character in reversed(username):
                    if character.isdigit():
                        username = username.pop()
                    else:
                        break
                username = username + usernameCounter
                usernameCounter = usernameCounter+1
            else:
                break
        os.system("usermod " + username + " -g" + group + " --move-home " + homeDir + " --shell " + shell + NO_OUT)
        os.system("chfn " + " -f " + fName + lName + " -w " + phone + " -o " + office + username + NO_OUT)
        #forces password change on login
        os.system("passwd -e " + username + NO_OUT)

if __name__ == '__main__':
    os.system("clear")
    cCheck()
    createUsers(dataIntake())
