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
    header = []
    users = []

    with open("linux_users.csv", 'r') as userCSV:
        csvreader = csv.reader(userCSV)

    # take header field to ignore
        header = next(userCSV)

    #one list element per person
        for row in userCSV:
            users.append(row)

    #export user with attributes without trailing space
    return users.pop()

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
            #notify user and remove entry for missing information
            if userList[userIndex][argumentIndex] == '':
                print("User ", userList[userIndex][2], " ", userList[userIndex][3], "account was not added due to missing information. ")
                userList.pop(userIndex)

            #if character is not a letter, omit
            for characterIndex in range(len(userList[userIndex][argumentIndex])): #userlist[userIndex][argumentIndex][letterIndex] = 'a'...
                if argumentIndex in specialCharsAcceptableList: #TODO fix where this is placed?
                    break
                if not ord(userList[userIndex][argumentIndex][characterIndex]) in range(ord("A"), ord("z")): #if character is not a letter, remove
                    userList[userIndex][argumentIndex] = userList[userIndex][argumentIndex].pop[characterIndex]

            #must create dept directories before making home folders, but after removing special chars
            if argumentIndex == 5:
                os.system("mkdir "+ userList[userIndex][5] + NO_OUT)

        #define arguments
        eID = userList[userIndex][0]
        lName = userList[userIndex][1]
        fName = userList[userIndex][2]
        office = userList[userIndex][3]
        phone = userList[userIndex][4]
        dept = userList[userIndex][5]
        group = userList[userIndex][6]
        password = "password"
        homeDir = "/home/" + dept + "/" + username
        #create group if it does not exist
        groupExistCheck = os.system("getent group ", group + NO_OUT)
        if groupExistCheck == 0:
            os.system("groupadd " + group + NO_OUT)

        #change from default /usr/bin/bash to /usr/bin/csh for office members
        if group == "office":
            shell = "/usr/bin/csh"

        #if user exists, add counter
        username = fName[0] + lName
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.system("clear")
    cCheck()
    createUsers(dataIntake())
