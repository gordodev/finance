#!/bin/ksh
#ELEMENT: This is a working loop. Keeps asking questions until you say no
#Variables: qnum=question number
#Version: 2.0
#Note: Version 3 adds modularity
#Date 5/21/14
#NOTE: 5/21/14 added modular question numbers. It works. Next add modification to existing scripts function

#script to create quiz scripts

trap 'echo "Exiting $quizname";  read endscript?"Exit script?"; if [[ $endscript = [yY]* ]] then exit; fi; date' INT TERM EXIT #avoid script being killed by ctrl+c

#get quiz name/description
read quizname?"What is quiz name? "
read quizdesc?"What does quiz do? "


#create quiz file & add description
echo "#!/bin/ksh" > $quizname.tmp
echo "clear" >> $quizname.tmp
echo 'echo "DESCRIPTION: '$quizdesc'"' >> $quizname.tmp
echo "quizname=$quizname" >> $quizname.tmp
echo ' ' >> $quizname.tmp


#Logging
#create directory variable, then check if folder exists and create it if it does not exist.
echo 'DIRECTORY="./log"' >> $quizname.tmp
echo 'if [ ! -d "$DIRECTORY" ]' >> $quizname.tmp
echo 'then' >> $quizname.tmp
echo '  mkdir ./log' >> $quizname.tmp
echo 'fi' >> $quizname.tmp
echo ' ' >> $quizname.tmp


echo 'echo "~~" >> ./log/$quizname.log' >> $quizname.tmp
echo 'echo "$quizname started at $(date)" >> ./log/$quizname.log' >> $quizname.tmp
echo ' ' >> $quizname.tmp

#Send score keeping and error logging function over to script
echo 'function addpoints {' >> $quizname.tmp
echo ' '>> $quizname.tmp
echo 'read answer?"What is answer? "'>> $quizname.tmp
echo 'if [[ "$answer" = "$canswer"* ]]'>> $quizname.tmp
echo 'then'>> $quizname.tmp
echo '        let cqnum=cqnum+1'>> $quizname.tmp
echo 'else' >> $quizname.tmp                 #if answer wrong, log it with correct answer
echo '     date >> ./log/$quizname.err' >> $quizname.tmp
echo '     echo "$question is not $answer, it is $canswer" >> ./log/$quizname.err' >> $quizname.tmp  #done logging
echo 'fi'>> $quizname.tmp
echo 'clear' >> $quizname.tmp
echo ' '>> $quizname.tmp
echo '}'>> $quizname.tmp

echo ' '>> $quizname.tmp

#Correct question variable initiation
echo '#Initiate correct question variable' >> $quizname.tmp
echo 'cqnum=0 '>> $quizname.tmp
echo 'qnum=0 '>> $quizname.tmp
echo ' '>> $quizname.tmp

echo '#Questions _____________________________________ vvv'>> $quizname.tmp


#Begin question building loop. Run until broken when user says to stop by not answering yes to continue question
qnum=0
echo 'tqnum=0'  >> $quizname.tmp
while true; do
let qnum=qnum+1
echo '#QUESTIONBEGIN' >> $quizname.tmp
echo 'let tqnum=tqnum+1'  >> $quizname.tmp
echo 'let qnum=qnum+1'  >> $quizname.tmp
echo ' ' >> $quizname.tmp
echo ' ' >> $quizname.tmp
echo 'echo "Question $qnum:"' >> $quizname.tmp
echo ""
#read question?"QUESTION $qnum: "; echo 'echo "'$qnum\) $question'"' >> $quizname.tmp
read question?"QUESTION $qnum: "; echo 'echo $qnum\) '$question'' >> $quizname.tmp
echo 'question='"'$question'"'' >> $quizname.tmp #Send question variable to quiz script so you can pull it up for logging.

echo ""
read choice1?"Enter choice A: "; echo 'echo "   A: '$choice1'"' >> $quizname.tmp
read choice2?"Enter choice B: "; echo 'echo "   B: '$choice2'"' >> $quizname.tmp
read choice3?"Enter choice C: "; echo 'echo "   C: '$choice3'"' >> $quizname.tmp
read choice4?"Enter choice D: "; echo 'echo "   D: '$choice4'"' >> $quizname.tmp
echo ""
read answer?"What is the answer? "; echo 'canswer="'$answer'"' >> $quizname.tmp

#echo 'canswer="'$canswer'"'>> $quizname.tmp

#check is this is question1. If true add timestamp initiation
#Begin timming
if [[ $qnum = 1 ]]
then
    echo "Adding timestamp for first question"
    echo '#Time recorded' >> $quizname.tmp
    echo ' '>> $quizname.tmp
    echo '#This will store and display current time. Current time is time since epoch in seconds'>> $quizname.tmp
    echo 'echo "Time is: $(date +%R:%S)"'>> $quizname.tmp
    echo 'btime=$(date +"%s") '>> $quizname.tmp
    echo '#Activity to be timed begins here___________Begin timer'>> $quizname.tmp
fi

echo ' ' >> $quizname.tmp
echo 'addpoints' >> $quizname.tmp    #Add points
echo '#QUESTIONEND' >> $quizname.tmp

#Continue or quit adding questions
read continueq?"More questions? "

if [[ $continueq = [yY]* ]]
then
    echo "You have more"
    continue
elif    [[ $continueq = [nN]* ]]
then
    break
elif    [ $# -eq 0 ]
then
    continue
else
    echo "User has no more questions. Exiting . . . ."
    break
fi
done

echo '#QUESTIONFINAL' >> $quizname.tmp
echo '#END Questions _________________________________________________________ ^^^'>> $quizname.tmp
echo ' ' >> $quizname.tmp

#End timming
echo '#Activity complete here ______________________________________END timing' >> $quizname.tmp
echo 'etime=$(date +"%s") #End time recorded'>> $quizname.tmp
echo 'diff=$(($etime-$btime)) #Elapsed time calculation'>> $quizname.tmp
echo 'echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed."'>> $quizname.tmp

#Send score code
echo '#Begin scoring logic' >> $quizname.tmp
echo 'typeset -F0 score'>> $quizname.tmp
echo 'typeset -F0 cqnum'>> $quizname.tmp
echo 'typeset -F0 tqnum'>> $quizname.tmp
#echo 'tqnum='$qnum'' >> $quizname.tmp
echo 'let score="((($cqnum/$tqnum)*100))"'>> $quizname.tmp
echo 'echo "You got $cqnum answers correct out of $tqnum questions and your score was $score%"'>> $quizname.tmp
echo '#echo "score math is $cqnum / $tqnum times 100"'>> $quizname.tmp

#Logging

echo 'echo "$(($diff / 60)) minutes and $(($diff % 60)) seconds elapsed.">> ./log/$quizname.log' >> $quizname.tmp
echo 'echo "You got $cqnum answers correct out of $tqnum questions and your score was $score%" >> ./log/$quizname.log' >> $quizname.tmp
echo 'echo "$quizname stopped at $(date)" >> ./log/$quizname.log' >> $quizname.tmp

#END SCRIPT
