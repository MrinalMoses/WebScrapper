from AQI_avg import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016,avg_data_2017,avg_data_2018
import sys
import pandas as pd
from bs4 import BeautifulSoup
import os
import csv


def html_data(month,year):
    file=open('/Desktop/New folder/data/html/{}/{}.html'.format(year, month))
    text=file.read()
    
    finalD=[]
    tempD=[]
    
    soup = BeautifulSoup(text, "lxml")
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a = tr.get_text()
                tempD.append(a)

    rows = len(tempD) / 15

    for times in range(round(rows)):
        newtempD = []
        for i in range(15):
            newtempD.append(tempD[0])
            tempD.pop(0)
        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length - 1)
    finalD.pop(0)
    
    for a in range(len(finalD)):
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD

def datacombine(year, cs):
    for a in pd.read_csv('/Desktop/New folder/data/combineddata/realdata' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist

if __name__=='__main__':
    if not os.path.exists(('/Desktop/New folder/data/combineddata')):
        os.makedirs('/Desktop/New folder/data/combineddata')
    for year in range(2013, 2019):
        final_data=[]
        with open('/Desktop/New folder/data/combineddata/realdata'+str(year)+'.csv','w') as csvfile:
             wr = csv.writer(csvfile, dialect='excel')
             wr.writerow( ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1,13):
            temp = html_data(month, year)
            final_data=final_data+temp
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))()
        for i in range(len(final_data)-1):
            final_data[i].insert(8, pm[i])
        with open('/Desktop/New folder/data/combineddata/realdata'+str(year)+'.csv','a') as csvfile:
             wr = csv.writer(csvfile, dialect='excel')
             for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-":
                        flag = 1
                if flag != 1:
                    wr.writerow(row)
                    
                    
    data_2013 = datacombine(2013, 600)
    data_2014 = datacombine(2014, 600)
    data_2015 = datacombine(2015, 600)
    data_2016 = datacombine(2016, 600)
    data_2017 = datacombine(2016, 600)
    data_2018 = datacombine(2016, 600)
    total=data_2013+data_2014+data_2015+data_2017+data_2018
    
    with open('/Desktop/New folder/data/combineddata/realdata.csv','w') as csvfile:
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        wr.writerows(total)
    
            