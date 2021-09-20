# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 10:08:19 2021

@author: Juan
"""

import simpy as sp
import random as rn
import matplotlib.pyplot as plt


class lemonade_stand:
    
    def __init__(self,env, cashier=1):
        self.cashier = sp.Resource(env,capacity=cashier)
        self.env = env
        
        #
        self.data = []
        self.sold = 0
        
        # 
        self.waiting_time = []
        
    def sell(self):
        # Selling lemonade time and tabulate
        past = self.env.now
        yield self.env.timeout(rn.normalvariate(3, 0.2))
        self.sold += 1
        self.data.append((self.env.now,self.sold))
        self.waiting_time.append(self.env.now - past)
        
def Car(env,stand): # Customer
    print(f"Requested : {env.now}")
    with stand.cashier.request() as request:
        yield request
        yield env.process(stand.sell())
        print(f"Sold: {env.now}")
        
    
def run(env,stand):   # PEM
    
    for car in range(2):
        env.process(Car(env,stand))
        
        # Customer walking in
    while True:
        
        yield env.timeout(rn.normalvariate(1, 0.1))
        env.process(Car(env,stand))

if __name__ == '__main__':
    rn.seed()
    env = sp.Environment()
    stand = lemonade_stand(env)
    env.process(run(env,stand))
    env.run(8*60*5)
    
    data = stand.data
    
    x_val = [x[0] for x in data]
    y_val = [x[1] for x in data]
    
    plt.scatter(x_val,y_val)
    plt.plot(x_val,y_val,'or')
    plt.show()
    
    
    plt.hist(stand.waiting_time)