#!/usr/bin/ksh

#FIXWriter
#This will generate and erase FIX messages for FIX application development testing

touch fix.log
clear

echo "What do you want? "
echo ""
echo "i:insert order"  #Default
echo "io:insert order"
echo "ix:insert execution"
echo "d:delete log"

read choice?"Types choice: "

echo "You chose $choice"


if [[ $choice == "i" ]]
then
    echo "Inserting order"
    echo "35=D^55=AAPL^38=100" >> fix.log
elif [[ $choice == "del" ]]
then
    rm -v fix.log

elif [[ $choice == "ix" ]]
then
        echo "insert execution"
    echo "35=8^55=AAPL^38=100"

elif [[ $choice == "io" ]]
then
        echo "Inserting order"
    echo "35=D^55=AAPL^38=100"


fi

echo ""
echo ""

echo "fix.log contents:  "
cat fix.log

