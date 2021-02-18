
#Basic logic:


# Input a choice (1, 2 or 3)
choice=int(input("Type number above: "))

# Set the choices

print("Choice is",choice)

if choice == 1: 
 # Define RAM variables
 TotalRAM=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | cut -d \' \' -f 2'], shell= True)
 RAMUsed=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | cut -d \' \' -f 3'], shell= True)
 RAMFree=subprocess.check_output(['free -h  | grep ^Mem | tr -s \' \' | cut -d \' \' -f 4'], shell= True)
 Threshold_RAM_Usage=2048000

        print("Checking RAM Usage...")
 print(" Your total RAM Capacity is: ", TotalRAM)
 print(" Now, your system is using: ", RAMUsed)
        print(" And, you have free RAM Capacity of: ", RAMFree)

 # Check if RAM is overused
 RAMfreeValue=int(subprocess.check_output(['free   | grep ^Mem | tr -s \' \' | cut -d \' \' -f 4'], shell= True))
        if RAMfreeValue <= Threshold_RAM_Usage:  # I also converted the string to integer using int ()   
                print("Alert: Now, you only have the following amount of free RAM: ",  RAMFree)



elif choice == 2:
# Define CPU variables
 # I used check_ouput module here, shell=true means the command will be executed through the shell
 '''Important! READ THIS! When shell=True is dangerous?
 If we execute shell commands that might include unsanitized input from an untrusted source, 
 it will make a program vulnerable to shell injection,
 a serious security flaw which can result in arbitrary command execution. 
 For this reason, the use of shell=True is strongly discouraged
 in cases where the command string is constructed from external input
 '''

 cpuload=subprocess.check_output(['uptime | grep -o \"[0-9]*.[0-9][0-9]\"$'], shell= True)
 Threshold_CPU_Load=0.90
 

 print("Checking CPU...")
 print("Your CPU is overloaded by this amount in the last 15 minutes: ", cpuload) 

 # set up an alert if the CPU load  is above 0.90 over 15 minutes
 if float(cpuload) >= Threshold_CPU_Load:   # Notice: I converted the string cpuload to a float number using float()
  print("Alert: your CPU is overloaded, your CPU is overloaded by: ",  cpuload, " in the last 15 minutes")

elif choice == 3: 
 # Define Disk variables for /home parition
        HomeUsage=subprocess.check_output(['df | grep "/home" | cut -d  " "  -f 13'], shell= True)
        Threshold_home_Usage=75



 print("Checking disk space:") 
 print("Your current Home partition usage is: ", HomeUsage )

   # Check if /home is overused
 HomeUsageValue=int(HomeUsage[:2])
        if int(HomeUsageValue) >= Threshold_home_Usage:  # I also converted the string to integer using int ()   
                print("Alert: Now, you over-used your /home partition by:", HomeUsage )﻿





------------------------------------------------------------------------------------------------------

---------------------------------  NYFIX REMCOM

#!/bin/ksh
#Here are all the commands we want to do on each box asigned to a variable.
#NOTE: Command may not work on fixpmt and does not work for apps logs

#commands='bash; cat *.ini | grep -i fix_mode; cat *.ini | grep -i port; cat *.ini | grep -i day; cat *.ini | grep -i host; cat #*.ini | grep -i send; cat *.ini | grep -i target; cat *.ini | grep -i contact; cat *.ini | grep -i customer; echo "Orders"; grep #-c -s 35=D fix.log; echo "DKs"; grep -c -s 35=Q fix.log; echo "Order rejects:";grep -c -s 39=8 fix.log'

commands='clear; echo "_______________________________________________"; cat *.ini | grep -i fix_mode; cat *.ini | grep -i port; cat *.ini | grep -i day; cat *.ini | grep -i host; cat *.ini | grep -i send; cat *.ini | grep -i target; cat *.ini | grep -i contact; cat *.ini | grep -i number; cat *.ini | grep -i customer; cat *.ini | grep -i vendor; pwd; echo "Order Rejects:"; cat fix.log | grep -c 39=8; echo ""; echo ""; echo ""; ls -ltr | grep -i fix.*; echo "_______________________________________________"; echo "If you see a lot of errors like cannot open ini or not found"; echo "then the connection may be disabled or removed. Try to find"; echo "FSM on your own following existing conventions"; echo "_______________________________________________"'

while true; do

    read prodfsm?"Input FSM:"
    clear
   
echo "Identifying FSM..."


    #Below is the list of FSMs that this script is aware of and that it will check for in user input
    for fsm in fix3 fix9 fix10 fixi sfix1 fixpmt fix1 fix2 fix4 fix5 fix6 fix7 fix8 fix11

    #Identify FSM; will check for existance of all fix boxes and echo path when foun#d
    #_____________________________________________________________FSM CHECKS
        do
        echo "Checking for $fsm..."
echo "."
echo ".."
echo "...."
echo "........"
echo "............."
echo "......................."
echo "......................................"
echo "............................................................................"
echo "........................................................................................................................................................"
        clear

        # Basically setting prodfsm to the first field of what user input, then checking if it matching a value in for loop
#The found value is also being set to 1 to indicate success
        prodfsm1=$(echo $prodfsm | awk {'print $1'})
        if [[ $prodfsm1 = $fsm ]]
            then
            let found=1
            clear
            echo ""
            echo ""

            echo "cd /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`; $commands"
            echo ""
            echo ""
            echo ""
            echo ""
            echo ""
        sleep 2
            echo ""
#remote
#sleep 1
                echo "_____________________FIX LOG TAIL_____________________"
#      sleep 1
                ssh -l support $fsm tail -10 /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log
  #      sleep 1
                echo "_____________________FIX LOG 35=3_____________________"
  #    sleep 1

                ssh -l support $fsm cat -v /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log | grep 35=3 | awk '{gsub(/39=/,"+_____>39=");print}'
    #    sleep 1

                echo "_____________________FIX LOG 35=9_____________________"
    #  sleep 1

                ssh -l support $fsm cat -v /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log | grep 35=9 | awk '{gsub(/39=/,"+_____>39=");print}'
      #  sleep 1

                echo "_____________________FIX LOG 39=8_____________________"
      # sleep 1

                ssh -l support $fsm cat -v /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log | grep 39=8 | awk '{gsub(/39=/,"+_____>39=");print}'
        #sleep 1

echo "_____________________FIX LOG 35=Q_____________________"

                ssh -l support $fsm cat -v /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log | grep 35=Q | awk '{gsub(/39=/,"+_____>39=");print}'
        #sleep 1

#remote

            echo ""
            echo ""
            #displaying the generated grouped commands to user's teminal so they can copy and past it on fix box
            echo "                                "
            #ssh -l support $fsm tail -10 /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`/fix.log
           
            echo "cd /opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`; $commands"
            echo ""
            echo " "
            echo " "
        #sleep 10
    #Break for loop/stop checking for FSMs
    break

            else
            let found=0

            fi
        done

    if [[ $found = 1 ]]
        then
        echo "Successfully identified valid FSM. Copy and paste above commands into $fsm window and hit enter"
        echo "You will then be on $fsm in directory "/opt/nyfix/$fsm/Engines/`echo $prodfsm | awk {'print $NF'}`""
    sleep 10
#PLACEHOLDER  This is where the old remote commands were^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

       
                clear


    elif [[ $found = 0 ]]
        then
        echo "Invalid or unrecognized FSM, try manual navigation."
        echo "____________________________________________________________________________________________"
        echo "NOTE: You should be pasting your getEngineInfo results into this script. See example below:"
        echo "fix5 => FAHNFT/comm/DBAM"
        echo "____________________________________________________________________________________________"
        echo ""
        echo ""
        echo ""
    fi
done

#End Script____________________________________________________________________________________________________
#!/bin/ksh

###############################################################################
# remcom
# Carlyle Gordon
# NYFIX, Inc.
# 03/17/2007
###############################################################################
#Purpose is to eliminate the need to have multiple putty sessions open by mirroring# user's commands to FSM.
###############################################################################

trap 'clear; echo "."; sleep 1; clear; echo "  ."; sleep 1; clear; echo "          ."; sleep 1; clear; echo "User closed script on $(date)"; echo '$userpath';exit' 9 2 3

CompID_History="CompID History: "
CMS_History="CMS Search History: "

mycommands='clear; echo "_______________________________________________"; cat *.ini | grep -s FIX_MODE | grep SERVER && netstat -an | grep $(cat *.ini | grep PORT | sed -n 's/PORT//p') || cat *.ini | grep -i FIX_MODE; cat *.ini | grep -i port; cat *.ini | grep -i day; cat *.ini | grep -i host; cat *.ini | grep -i send; cat *.ini | grep -i target; cat *.ini | grep -i contact; cat *.ini | grep -i number; cat *.ini | grep -i customer; cat *.ini | grep -i vendor; pwd; echo "Order Rejects:"; cat fix.log | grep -c 39=8; echo "orders:"; echo $(cat fix.log | grep -c 35=D); echo "ACKs:"; echo $(cat fix.log | grep 39=0 | grep -c 20=0); echo "Session Rejects:"; echo $(cat fix.log | grep -c 35=3); echo "DKs:"; echo $(cat fix.log | grep -c 35=Q); echo ""; echo ""; echo ""; ls -ltr | grep -i fix.*; echo "_______________________________________________"; echo "If you see a lot of errors like cannot open ini or not found"; echo "then the connection may be disabled or removed. Try to find";!
  echo "FSM on your own following existing conventions"; echo "_______________________________________________"'

clear
echo "$(date)"
echo "$(date -u)"
echo "                                                                                        $(logname)"
echo "                                          --- NYFIX Autonavigator --- V.3"
echo "                                      Run commands remotely from prodgate(Now CMS Aware)"
echo "                                    ____________________________________________"
echo "                                                                                      At the CompID prompt you can also enter:"
echo "                                                                                      CMS box number(1,2,3..)"
echo "                                                                                      11=clientorderid in cms search or on FIX FSM"
echo "                                                                                      Soon with BranchSeqNums you can auto-search all CMS boxes"

#This loop should not be repeated until user done investigating current connection
#This is just determining where to go for logs
#_________________________________________________________________________________________________FIGURE OUT FSM

while true; do

    if [[ $CompID_History != "CompID History: "  ]]
    then
        echo $CompID_History
    fi
    echo ""
    echo "______________________"
    echo "----------------------"
    read compids?"What CompIDs do you have?"
    #echo $CompID_History | grep $compids 2> /dev/null || CompID_History="$CompID_History $compids"  #store compid for future ref when did'nt alraady
    echo $CompID_History | grep -s -q $compids 2> /dev/null || CompID_History="$CompID_History $compids"  #store compid for future ref when did'nt alraady
       
#                                                                        ___________    ___________
    if [[ $compids != ?*  ]]
        then
            echo "That does not look like a CompID. Try again."
                continue 1
                echo $?

    elif [[ $compids = exit ]]
    then
        clear
        echo "Exiting NYFIX Remote Command."
        sleep 1; clear
        echo "Exiting NYFIX Remote Command  ."
        clear
        exit


#                                                                          User wants ProdEng Script
                elif [[ $compids = prod* ]]
                then
                        echo "prodEngSupport.sh"
                        echo "Going to ProdEng script"
                        /opt/pescripts/bin/./prodEngSupport.sh
            echo "Returned to Autonav script"
            continue 1


#                                                                            User entereed CMS BranchSeqNum
        elif [[ $compids = [A-Z]*-[0-9]* ]]
    then
        BranchSeqNum=compids
        echo "CMS Branch Sequence number is $compids"
        echo "I don't know how to search for that yet, but you can enter the box number as a"
        echo "CompID and I can take you there."
                echo "Sorry, I am not yet CMS aware. My next version will be CMS aware"
        echo "In the future I will be able to take BranchSeqNum from FIX Trader and -"
        echo "search multiple boxes for that number"
        continue 1
#                                                                              User entered CMS box number
    elif [[ $compids = [0-9] ]]
    then
        cmspath=/opt/nyfix/cms/cmsr$compids
        cmsbox=cmsr$compids

        echo "[Going to CMSR$compids...]"
        echo '['$CMS_History']'
        read searchstring?"What are you looking for on CMSR$compids? "
        if [[ $CMS_History = "CMS Search History: " ]]                      #CMS History set   
        then
            CMS_History="CMS Search History: $searchstring"
        else
            CMS_History="$CMS_History    _ $searchstring"
           
        fi
       
        if [[ $searchstring = "11="* ]]
        then
            cmscommand="grep '$searchstring' fix.log && vi +/'$searchstring' fix.log || echo 'Sorry, $searchstring not found'"
           
            elif [[ $searchstring = [A-Z]* ]]
            then
            cmscommand="grep '$searchstring' output && vi +/'$searchstring' output || echo 'Sorry, $searchstring not found'"
        else
            continue 1
        fi

        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"
                echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"

                echo "Please copy and paste command below at the prompt below"
                echo "____________________________________________________________________________________"
                echo ""
                echo ""
                echo ""
                echo ""
        echo "cd $cmspath"
        echo $cmscommand
                echo ""
                echo ""
                echo ""
                echo "____________________________________________________________________________________"


            ssh -l support $cmsbox
            continue 1
        fi
#     __________    ___________    ___________    ___________    ____Done other than CompID Validation__________        ___________

    compcount=$(echo "$compids" | wc -w)                                #count strings that user entered

#                                                                                User entered single string
    if [[ $compcount = 1  ]]
    then
        echo "Searching for single string. . ."
        echo ""
            cat /opt/pescripts/bin/data/engineInfoList*txt | grep -i $compids
        if [[ $? != 0 ]]
        then
            echo "Invalid CompID"
            continue 1
        fi

        echo "______________________________________"
        echo ""
#break


#                                                                                  User entered 2 strings
    elif [[ $compcount = 2  ]]
    then
        echo "Searching for double string. . ."
        echo ""
            cat /opt/pescripts/bin/data/engineInfoList*txt | grep -i $(echo $compids | awk {'print $1'}) | grep -i $(echo $compids | awk {'print $2'})
        if [[ $? != 0 ]]
                then
                        echo "Invalid CompID"
                        continue 1
                fi

        echo "______________________________________"
        echo ""
#break

#       

#                                                                          User not enter single or double string
    else
            echo "No more than 2 entries possible, usually just engine and CompID"
        echo ""
        continue 1
    fi

#____________________________________________________________________________________________________________________________________________
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#__________________________________________________________Input validation__________________________________________________________________

    while true; do
        echo '(Hit "Enter" to search again)'
        read prodfsm?'Copy and paste FSM that you want to check from above: '
            clear
#      _________________________________________                            Check user input valid or exit request
#                                                                                If user wants to exit...
            if [[ $prodfsm = exit ]]
            then
                    echo "Exiting Remote Commander..."
                    sleep 1
                    clear
                    echo "Bye $(logname)!"
                    date
                    date -u
                        exit

        elif [[ $prodfsm != ?* ]]
        then
                        echo "Nothing entered, backing up"
            continue 2


#                                                                      If user does not enter FSM in viewengineinfo format
            elif [[ $prodfsm != *\=\>*  ]]
            then
                    echo "Not sure what you entered, but you should be pasting FSM from GetEngineInfo script"
                    echo "FSM MUST be in this format:"
                    echo "fix3 => NYFIX3/comm/BLP"
            echo ""
               
            if [[ $prodfsm = *fix* ]]
                    then
                echo ""
                            echo "It looks like you are trying to enter an engine name, but I need the comm handler too."
                            echo "You must enter \"CompID/comm/CompID\" after \"engine name =>\""
            fi
    continue 1

#                                                                          User wants ProdEng Script
        elif [[ $prodfsm = prod*[!rRtT4] ]]
                then
                        echo "prodEngSupport.sh"
                        echo "Going to ProdEng script"
                        /opt/pescripts/bin/./prodEngSupport.sh

        else
            break
                fi
    done
#____________________________________________________________________________________________________________________________________________
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#__________________________________________________________Go to Engine______________________________________________________________________


   
#Done validating garbage, now going to FSM
   
#                          First field of fsm user entered
    echo "Checking for $(echo $prodfsm | awk {'print $1'})..."
        echo "."
        echo ".."
                userengine=$(echo $prodfsm | awk {'print $1'})
        userpath='/opt/nyfix/'$userengine'/Engines/'`echo $prodfsm | awk {'print $NF'}`''
                echo "User path is now $userpath"

    #______________________________________________________________________________________________________Figured out FSM
        #______________________________________________________________________________________________________Echo commands to box
        #

                #Tailing fix log on remote box
        echo "Tailing fix log on remote box"
        ssh -l support $userengine tail -30 $userpath/fix.log
        ssh -l support $userengine "cd $userpath; $mycommands"
#                                                                  Remote Command Loop; running commands remotely
    while true; do
                read usercommands?"(AutoNav 3.0,$prodfsm)% "
#                                                                        _________________________________
                if [[ $usercommands = exit* ]]
                then
#                                                              replace fix.log with path/fix.log and asign result to variable
                        echo "Exiting $userengine ...."
#                                                                        go 2 loops up which is for loop
                        continue 2

#                                                                        _________________________________
                elif [[ $usercommands = "11="* ]]
                then
                        echo "Searching for ClOrderID...."
            ssh -l support $userengine 'cd '$userpath'; cat fix.log | grep '$usercommands' |  sed 's/39=/_____39=/g' | sed 's/32=/_____32=/g' | sed             's/14=/_____14=/g' | sed 's/55=/_____55=/g''



#                                                                        _________________________________
                elif [[ $usercommands = cd* ]]
                then
            echo "Requesting directory change...."
                        echo $userpath
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"

                        echo "Please copy and paste command below at the prompt below"
                        echo "____________________________________________________________________________________"
                        echo ""
                        echo ""
                        echo ""
                        echo "cd $userpath"
                        echo "$usercommands"
                        echo ""
                        echo ""
                        echo ""
                        echo ""
                        echo "____________________________________________________________________________________"

            sh -l support $userengine

#                                      User wants ProdEng Script
elif [[ $usercommands = prod* ]]
                then
                        echo "prodEngSupport.sh"
                        echo "Going to ProdEng script"
            /opt/pescripts/bin/./prodEngSupport.sh

#                                                                          _____________________________
                elif [[ $usercommands = go*  ]]
                then
#                                                            1st field stripping
                        usercommands=$(echo $usercommands | awk '{ $1 = ""; print }')
                        echo "user commands"
                        echo $usercommands
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"

                        echo "Taking you to FIX Engine to run commands locally"
                        echo "Copy and paste commands below into the prompt below"
                        echo "Type \"exit\" when you want to come back to Remote Commander"
                        echo "____________________________________________________________________________________"

                        echo ""
                        echo ""
                        echo ""
                        echo "cd $userpath"
            echo "$usercommands"
                        echo ""
                        echo ""
                        echo ""
                        echo "____________________________________________________________________________________"

                        ssh -l support $userengine
#                                                      User hit ENTER
#                                                                          _______________________________
                elif [[ $usercommands != ?* ]]
                then
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"
                        echo "############################################################COPY AND PASTE COMMANDS BELOW!!!!########"


                        echo "Please copy and paste command below at the prompt below"
                        echo "____________________________________________________________________________________"
                        echo ""
                        echo ""
                        echo ""
                        echo "cd $userpath"
                        echo "$usercommands"
                        echo ""
                        echo ""
                        echo ""
                        echo "____________________________________________________________________________________"
                        ssh -l support $userengine
#                                                                                  User trying to grep
#                                                                          _________________________________
        elif [[ $usercommands = *grep* ]]
                then
                        clear
            echo "[grep request]                                    (-i caseinsensitive -v inverse -c count)"
            echo ""
                        ssh -l support $userengine 'cd '$userpath'; '$usercommands' |  sed 's/39=/_____39=/g' | sed 's/32=/_____32=/g' | sed 's/14=/_____14=/g'             | sed 's/55=/_____55=/g''
            echo "__________________________________________________________________________________________________________"

                elif [[ $usercommands = @(vi*|tree*|less*|tail*|top*|touch*|more*|cat fix.log) ]]
                then
                        clear
                        echo "[Bad command for Autonav environment]                                    "
                        echo ""
            echo "cd $userpath; $usercommands"
            echo ""
            echo ""
            echo ""
            echo ""
            ssh -l support $userengine ""

#                                                                          _________________________________
                else
                        ssh -l support $userengine "cd $userpath; $usercommands"

                fi

                echo "Last command ran on $userengine :      $usercommands"
                date
                date -u
                continue 1
    done
done

#Variables:
#CompID_History: Used to store previously entered CompIDs, for user reference so they can copy and paste then to go to previous connection
#mycommands=Commands that will be run when a remote session with an FSM is established
#compids=variable for CompIDs that user enters for autonavigation
#compcount=variable for counting how many CompIDs that the user has entered so we can grep or grep first field | grep second field using awk
#prodfsm=FSM in the ViewEngineInfo script format(fix3 => NYFIX3/comm/BLP
#userengine=set to first field of prodfsm(fix3/fix9)
#userpath=location or directory of FSM, based on standard /opt/nyfix/enginename/commhandler
#usercommands=Anything user types in at Remote Command prompt. Some triggers are(go cd exit)
#gocms=used to determine if user wants to go to CMS
#END SCRIPT___________________________________________________________________________________________________________END SCRIPT
