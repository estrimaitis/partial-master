# -*- coding: utf-8 -*-
"""
Created on Fri Nov 12 13:53:40 2021

author: Emilis Strimaitis - emka
strimaitis.emilis@gmail.com
"""

import pandas as pd
import numpy as np
from datetime import datetime

class passive():
    def __init__(self,data):
        
        #data
        self.data=data
        
        #variables
        self.sum=0
        self.drawdown=0
        self.drawdown_data=[]
        self.risk=1
        self.remaining_risk=0
         
        #user input variables
        self.maximum_allowed_drawdown=0
        
        #buffer variables
        self.result=[]
        
    def reset_variables(self):
        self.sum=0
        self.drawdown=0
        self.drawdown_data=[]
        self.risk=1
        self.remaining_risk=0
        
    def request_user(self):
        "This method will request the user for input data"
        try:
            while(1):
                self.incremental_value = float(input( "fill % incremental value "))
                if self.incremental_value >0:
                    break
                else:
                    print("please, fill a number positive or different to zero")
        except:
            print("Only numbers")         
        
        
        try:
            while(1):
                self.maximum_allowed_drawdown = float(input( "fill maximun allowed drawdown "))
                if self.maximum_allowed_drawdown <=0:
                    break
                else:
                    print("please, fill a number negative or equal to zero")
        except:
            print("Only numbers")
            
            
   
                
        print("maximum allowed drawdown: {}".format(self.maximum_allowed_drawdown))
        
    def Update_drawdown(self,outcome):
        "outcome could be negative or positive"
        if self.drawdown + outcome <= 0:
            self.drawdown = self.drawdown + outcome
        elif self.drawdown + outcome > 0:
            self.drawdown =0
        self.drawdown_data.append(self.drawdown)

    def Update_sum(self,add):
        "add  variable could be -1 or  take_profit value"
        self.sum = self.sum + add

    def give_results(self):
        now = datetime.now()
        
        self.result = np.array(self.result,dtype=float)
        self.result=np.round(self.result,decimals=2)
        self.result=self.result[self.result[:, 0].argsort()]
        
        self.result_df=pd.DataFrame(self.result,columns=["Sum","First_partial","Second_partial","Third_partial","Fourth_partial", "Drawdown"])
        self.result_df.to_csv("./results/result {}.csv".format(now.strftime("%d-%m-%H-%M")))
        
        for i in list(range(0,6)):
            print('\n')


        print("TOP 10")
        print('\n')
        for i in list(range(1,11)):
            print("Sum: {} First: {} Second: {}  Third: {}  Fourth: {} Drawdown: {}".format(round(self.result[-1*i][0],3),
                                                                                  round(self.result[-1*i][1],3),
                                                                                  round(self.result[-1*i][2],3),
                                                                                  round(self.result[-1*i][3],3),
                                                                                  round(self.result[-1*i][4],3),
                                                                                  round(self.result[-1*i][5],3)))
            print('\n')
            
    def logic(self):
        "This method is the logical strategy"

        for Fourth_partial in np.arange(0 , 100 ,self.incremental_value):
            for Third_partial in np.arange(0 , 100,self.incremental_value):
                for second_partial in np.arange(0 , 100 ,self.incremental_value):
                    for first_partial in np.arange(0 , 100 ,self.incremental_value):
                        
                        for index, row in data.iterrows():
                        
                            if row["Partial 1"]>0:
                                
                                self.risk=1
                                aux=((row["Partial 1"])*first_partial/100)
                                self.Update_sum(aux)
                                self.Update_drawdown(aux)
                                
                                self.risk=1-(first_partial/100)
                            else:
                                outcome=-1 ; self.Update_drawdown(outcome)
                                self.Update_sum(-1)
                                if abs(self.drawdown) > abs(self.maximum_allowed_drawdown):
                                    self.sum=-10000
                                    break
                            
                            if row["Partial 2"]>0:
                               aux_risk=self.risk*(second_partial/100)         
                               self.Update_sum(row["Partial 2"]*aux_risk)
                               self.Update_drawdown(row["Partial 2"]*aux_risk)
                               self.risk=self.risk-aux_risk 
                            else:
                                if row["Final"]>0:
                                    self.Update_sum(row["Final"]*self.risk)
                                    self.Update_drawdown(row["Final"]*self.risk)  
                                continue
                               
                               
                            if row["Partial 3"]>0:
                               aux_risk=self.risk*(Third_partial/100) 
                               self.Update_sum(row["Partial 3"]*aux_risk)
                               self.Update_drawdown(row["Partial 3"]*aux_risk)   
                               self.risk=self.risk-aux_risk
                            else:
                                if row["Final"]>0:
                                    self.Update_sum(row["Final"]*self.risk)
                                    self.Update_drawdown(row["Final"]*self.risk)   
                                continue
                            
                            if row["Partial 4"]>0: 
                               aux_risk=self.risk*(Fourth_partial/100)
                               self.Update_sum(row["Partial 4"]*aux_risk)
                               self.Update_drawdown(row["Partial 4"]*aux_risk)
                               self.risk=self.risk-aux_risk
                            else:
                                if row["Final"]>0:
                                    self.Update_sum(row["Final"]*self.risk)
                                    self.Update_drawdown(row["Final"]*self.risk)   
                                continue
                            
                            if row["Final"]>0:
                                self.Update_sum(row["Final"]*self.risk)
                                self.Update_drawdown(row["Final"]*self.risk)   
                                
                        
                        
                        self.result.append([self.sum,
                                        first_partial,
                                        second_partial,
                                        Third_partial,
                                        Fourth_partial,
                                        min(self.drawdown_data)])
                        
                        print("Sum: {}   First: {}   Second: {} Third: {}  Fourth: {} Drawdown: {}".format(round(self.result[-1][0],2),
                                                                                  round(self.result[-1][1],2),
                                                                                  round(self.result[-1][2],2),
                                                                                  round(self.result[-1][3],2),
                                                                                  round(self.result[-1][4],2),
                                                                                  round(self.result[-1][5],2)))
                        self.reset_variables()

                  
                        
if __name__ == "__main__":
    
    data= pd.read_csv("./input/data.csv")
    
    script_instace=passive(data)
    script_instace.request_user()
    script_instace.logic()
    script_instace.give_results()
    input()    
  
    
  
  
