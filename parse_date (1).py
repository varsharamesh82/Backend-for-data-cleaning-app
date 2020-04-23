import pandas as pd
import sys
import re
import os
from datetime import date
import datetime
import dateparser
import holidays
import pytz
import statistics
import numpy as np

class parse_date(object):
    
    def __init__(self, input_csv,  deff,  out_type, change_list,normal_column,  out_file_name,  colname, country_code, out_file_path = os.getcwd(),  out_file_type = 'csv'):
        
        
        self.dataframe =pd.read_csv(input_csv)
        self.out_type = out_type
        self.colname=colname
        self.change_list=change_list
        self.deff=deff
        self.out_file_type = out_file_type
        self.out_file_path = out_file_path
        self.out_file_name = out_file_name
        self.normal_column=normal_column
        self.us_holidays = holidays.US()
        self.country_code=country_code
        
        
    def convert_date(self):
        dd=self.dataframe[self.colname]
        
        for i in range(dd.size):
            
            try:
                dy=dd[i]
                dt_stamp=dateparser.parse(dy)
            except:
                dt_stamp=dateparser.parse(self.deff)
                
            if(self.out_type == 'y-m-d'):
                dd[i]=dt_stamp.strftime('%Y/%m/%d')
            elif(self.out_type == 'y-d-m'):
                dd[i]=dt_stamp.strftime('%Y/%d/%m')
            elif(self.out_type == 'd-y-m'):
                dd[i]=dt_stamp.strftime('%d/%Y/%m')
            elif(self.out_type == 'm-y-d'):
                dd[i]=dt_stamp.strftime('%m/%Y/%d')
            elif(self.out_type == 'd-m-y'):
                dd[i]=dt_stamp.strftime('%d/%m/%Y')
            elif(self.out_type == 'm-d-y'):
                dd[i]=dt_stamp.strftime('%m/%d/%Y')
         
        self.dataframe['date']=dd;     
        
        #print(self.temp)
                
    
    def split_date(self):
        
        
        dd=self.dataframe[self.colname]
        yeaar=[0]*dd.size;
        monnth=[0]*dd.size;
        dayy=[0]*dd.size;
        weeek=[0]*dd.size;
       
        
        
        for i in range(dd.size):
        
            try:
                
                dy=dd[i]
                dt_stamp=dateparser.parse(dy)
                yeaar[i]=dt_stamp.year;
                monnth[i]=dt_stamp.month;
                weeek[i]=dt_stamp.isocalendar()[1]
                dtt=(date(dt_stamp.year,dt_stamp.month,dt_stamp.day)-date(dt_stamp.year,1,1)).days+1
                dayy[i]=dtt;
        
            except:
                dt_stamp=dateparser.parse(self.deff)
            
            
        self.dataframe['year']=yeaar
        self.dataframe['month']=monnth
        self.dataframe['week']=weeek
        self.dataframe['day']=dayy
       
        #print(self.temp)
        
        
    def check_holidays(self):
    
        dd=self.dataframe[self.colname]
        holidayss=[]
        for date in holidays.US().items():
            print(date)
        for i in range(dd.size):
            try:
                dy=dd[i]
                dt_stamp=dateparser.parse(dy)
                dt = dt_stamp.strftime('%m/%d/%Y')
                ho=self.us_holidays.get(dt)
                holidayss.insert(i,ho)
            except:
                holidayss.insert(i,"No holiday")
        
            
        self.dataframe['holidays']=holidayss
        #print(self.temp)
              
    def get_timezones(self):
        tz=pytz.country_timezones[self.country_code]
        dd=self.dataframe[self.colname]
        time_zone=[tz]*dd.size
        self.dataframe['Timezones']=time_zone
        
    def edit_headers(self):
        for key,val in self.change_list.items():
            self.dataframe.rename(columns={key:val}, errors="raise",inplace=True)
            
    def interpolate_miss(self):
        self.dataframe.interpolate(method ='linear', limit_direction ='both')
        
        
    def normal_distr(self):
        dg=self.dataframe[normal_column]
        mean=dg.mean()
        sd=dg.std()
        s = np.random.normal(mean, sd, 1000) #Random values in s
        #print("Random Values ")
        #print(s)
         
    def output_file(self):
        print(self.dataframe)
        if self.out_file_type == 'csv':
            self.dataframe.to_csv(self.out_file_path + '/%s' %self.out_file_name, index = False)
        elif self.out_file_type == 'json':
            print(self.out_file_path)
            self.dataframe.to_json(self.out_file_path + '/%s.json' %self.out_file_name)
            
    
            

if __name__ == '__main__':
    output_format=input("Enter the output date format")
    input_csv="F:\python36\date3.csv"
    country_code=input("Enter country code")
    change_list = dict()
    data_change=input("Enter the old column names and new column names spaced with :")
    normal_column=input('Enter the column name you want normal distribution')
    tem=data_change.split(" ")
    for val in tem:
        buf=val.split(":")
        change_list[buf[0]]=buf[1]
    p1=parse_date(input_csv,"1/1/2000",output_format,change_list,normal_column,"date2.csv","date",country_code,"F:\python36")
    p1.convert_date()
    p1.split_date()
    p1.check_holidays()
    p1.get_timezones()
    p1.edit_headers()
    p1.normal_distr()
    p1.output_file()
