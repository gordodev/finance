import pandas as pd
table=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]
df.to_csv("/home/csws/dev/github/finance/downloader/S&P500-Info.csv")
df.to_csv("/home/csws/dev/github/finance/downloader/S&P500-Symbols.csv", columns=['Symbol'])



'''
df.to_csv("S&P500-Info.csv")
df.to_csv("S&P500-Symbols.csv", columns=['Symbol'])



/home/csws/dev/github/finance/downloader/S&P500-Symbols.csv
'''
