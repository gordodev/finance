#!/bin/bash -v

#   Download CBOE securities list

#Test connectivity

if ping -c 1 markets.cboe.com; then echo good; else echo "Unable to connect to http://markets.cboe.com"; exit; fi

Today="$(date '+%Y%m%y')"
SSH_OPTIONS='-o ConnectionTimeout=5 -o PasswordAuthentication=no'
DirTarget="/home/csws/dev/github/finance/flintTrader/data"

echo -e "Downloading CBOE file...\n"
wget -q --connect-timeout=10 -O "${DirTarget}/cboe.csv" "http://markets.cboe.com/us/options/market_statistics/symbol_reference/?mkt=cone&listed=1&unit=1&closing=1"

echo -e "\n\nDownload attempt complete.\n"
