#!/usr/bin/bash

#Download NASDAQ shortsell restricted list

ssrfile="https://www.nasdaqtrader.com/dynamic/symdir/shorthalts/shorthalts`date +%Y%m%d`.txt"


function validate_url()
{
    wget --spider $1
    return $?
}

if validate_url $ssrfile; then
	echo -e "\nFile available. Downloading\n`date`\n"
	curl -o /home/csws/dev/github/finance/flintTrader/data/nasdaq_shortsell_restricted.txt "$ssrfile" || echo -e "\n\nFILE DOWNLOAD FAIL!!!\n\n"
else
	echo -e "Nasdaq Shortsell restriction list not found on site:\n$ssrfile"
fi



#Download latest file
#echo -e "\n\nDownloading $ssrfile\n"
#curl -o /home/csws/dev/github/finance/flintTrader/data/nasdaq_shortsell_restricted.txt "$ssrfile"

