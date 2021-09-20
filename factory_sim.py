# -*- coding: utf-8 -*-

"""
Created on Sun Aug 15 02:26:47 2021

Factory Simulation utilizing SimPy 
to analyze the cost of the machines breaking in a factory

This is a practice code 

@author: Juan
"""

import simpy as sp
import numpy as np


# create a generator 

def factory_run(env, repairers, spares):
    global cost 
    
    cost = 0.0
    
    # 50 machines doing the process
    # creating 50 machine and adding the events in the enviroment
    
    for i in range(50):
        env.process(operate_machine(env,repairers,spares))
    
    while True:
        cost += 3.75*8*repairers.capacity + 30*spares.capacity
        
        # cost will be appended every 8 hours
        yield env.timeout(8)
    
    
    
def operate_machine(env, repairers, spares):
    global cost
    
    while True:
        yield env.timeout(time_to_failure())
        
        t_broken = env.now
        print(f"Machine broke: {t_broken}")
        
        # Repair process
        yield spares.get(1)
        
        t_replaced = env.now
        print(f"Machine replaced: {t_replaced}")

        cost += 20*(t_replaced - t_broken)


def time_to_failure():
    return np.random.uniform(132, 182)
    
def repair_machine(env)    
    


# setting seed
np.random.seed(1)

# Setting enviroment
env = sp.Environment()

repairers = sp.Resource(env,3)

spares = sp.Container(env, init = 20, capacity = 20)

env.process(factory_run(env,repairers,spares))


env.run(until = 8*5*52)