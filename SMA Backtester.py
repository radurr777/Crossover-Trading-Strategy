#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

class SMABacktester():
    def __init__(self,symbol,SMA_S,SMA_L,start,end):
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L=SMA_L
        self.start=start
        self.end= end
        self.results = None
        self.get_data()
        
    def get_data(self):
        df=yf.download(self.symbol,start=self.start,end=self.end)
        data=df.Close.to_frame()
        data["returns"]=np.log(data.Close.div(data.Close.shift(1)))
        data["SMA_S"]=data.Close.rolling(self.SMA_S).mean()
        data["SMA_L"]=data.Close.rolling(self.SMA_L).mean()
        data.dropna(inplace=True)
        self.data2=data                                
        
        return data                                
        
    
    def test_result(self):  
        data=self.data2.copy().dropna()  
        data["position"]=np.where(data["SMA_S"]>data["SMA_L"],1,-1)
        data["strategy"]=data["returns"]*data.position.shift(1)
        data.dropna(inplace=True)
                                         
        data["returnsbh"] =data["returns"].cumsum().apply(np.exp)
        data["returnstrategy"]=data["strategy"].cumsum().apply(np.exp)
        perf=data["returnstrategy"].iloc[-1]  
        outperf=perf-data["returnsbh"].iloc[-1]
        self.result =data                                  
                                         
        ret=np.exp(data["strategy"].sum())
        std=data["strategy"].std()*np.sqrt(252) 
                                         
        return round(perf,6) ,round(outperf,6) 
                                         
                                         
    def plot_result(self):
        if self.result is None:
            print("Run the test please")
        else:
            title ="{} | SMA_S{} | SMA_L{}".format(self.symbol,self.SMA_S,self.SMA_L)
            self.result[["returnsbh","returnstrategy"]].plot(title=title,figsize=(12,8))                              
                                        
                                         
                                      

