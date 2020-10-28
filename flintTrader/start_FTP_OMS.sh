#!/bin/ksh

#Flint Trading Platform Launcher: Start up FTP OMS

#Launching by category

#Flint Trader --------------------------------------------------

### Order Entry for QA
x-terminal-emulator -e "ksh fix_writer.ksh"

sleep 2

#Feed ----------------------------------------------------------

### Feed Handler

sleep 2

#Support -------------------------------------------------------

### Platform Support Module
/home/csws/dev/github/finance/flintTrader/support/FTP_Monitor.py

sleep 2

#Compliance ----------------------------------------------------

sleep 2
