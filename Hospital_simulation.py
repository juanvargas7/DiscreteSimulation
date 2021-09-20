# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 14:57:55 2021

@author: Juan
"""
import simpy as sp
import random as rn 
import pandas as pd
import matplotlib.pyplot as plt



def fun():
    pass


class Hospital:
    
    """ Monitor and """
    
    def __init__(self, env):
        self.env = env
        self.time = []
        self.bed_occ = []
        self.queue_list = []
        self.line_list = []
        
        self.bed_count = 0

        self.admissions = 0 

        
    def observe(self):
        self.time.append(self.env.now)
        self.bed_occ.append(self.bed_count)

        
    def to_pandas(self):
        temp = pd.DataFrame()
        temp['Time'] = self.time
        temp['Bed Occupied'] = self.bed_occ
        return temp
    
    def admission(self):
        self.admissions += 1
        

    
    
class Hospital_Model:
    
    """ Hospital events class """
    
    def __init__(self, beds, hosts, doctors):
        
        self.env = sp.Environment()
        self.monitor = Hospital(self.env)
        
        self.beds = sp.Resource(self.env,beds)
        self.host = sp.Resource(self.env,hosts)
        self.doctors = sp.Resource(self.env,doctors)
        

        
    def host_wait(self):
        yield self.env.timeout(rn.gauss(1, 0.1))
        
    def bed_usage(self):
        yield self.env.timeout(rn.gauss(1, 0.2))
        
    def doctor_time(self):
        yield self.env.timeout(rn.gauss(1., 0.1))
        
    def monitor_(self):
        while True:
            yield self.env.timeout(1)
            self.monitor.observe()
        
        
    def go_hospital(self):
        self.monitor.admission()
        
        
        with self.host.request() as request:
            yield request
            yield self.env.process(self.host_wait())
            
            
            
            
        
        
        with self.beds.request() as request:
            yield request
            
            yield self.env.process(self.bed_usage())
            
            
            
        

    def run(self,number):
        rn.seed(number)
        self.env.process(self.monitor_())
        
        for i in range(20):
            self.env.process(self.go_hospital())

        while True:
            yield self.env.timeout(2)
            
            for i in range(rn.randint(1, 4)):
                self.env.process(self.go_hospital())
            

        
        
mod = Hospital_Model(10, 3, 5)

mod.env.process(mod.run(0))
mod.env.run(200)

data = mod.monitor.to_pandas()