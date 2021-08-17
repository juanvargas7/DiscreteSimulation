# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:56:27 2021

Theather Simulation

@author: Juan
"""
# Reduce average wait time

# Think of all the possible process for the events of 

# Working in muinutes 

import matplotlib.pyplot as plt
import simpy as sp
import random as rn
import statistics as st


wait_times =[]

#Create Theater
class Theather(object):
    
    def __init__(self, env, cashiers, server, ushers):
        self.env = env
        self.cashiers = sp.Resource(env,cashiers)
        self.server = sp.Resource(env,server)
        self.ushers = sp.Resource(env,ushers)

    def purchase_ticket(self, person):
        yield self.env.timeout(rn.randint(1,3))
        
    
    def check_ticket(self,person):
        yield self.env.timeout(3/60)
        
        
    def sell_food(self, person):
        yield self.env.timeout(rn.randint(5, 2))
            

# The event the person is gonna do in order
def go_to_movies(env,person, theater):
    arrival_time = env.now
    
    with theater.cashiers.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(person))
    
    with theater.ushers.request() as request:
        yield request
        yield env.process(theater.check_ticket(person))

    if rn.choice([True,False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(person))
            
    wait_times.append(env.now - arrival_time)
            

# The function that does everything
def run_theater(env, cashiers, servers, ushers):
    theater = Theather(env, cashiers, servers, ushers)

    for person in range(20):
        
        env.process(go_to_movies(env, person, theater))
        
    while True:
        yield env.timeout(rn.uniform(.5, .1))
        
        person += rn.sample([1,2,3,4], 1)[0]
        env.process(go_to_movies(env, person, theater))


# Utility
def avg_wait_time(wait_times):
    return st.mean(wait_times)

#
def calculate_wait_time(wait_times):
    average_wait = st.mean(wait_times)
    
    # Pretty print the results
    
    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)


def main(cashiers,servers,ushers):
    rn.seed()
    
    env = sp.Environment()
    env.process(run_theater(env, cashiers, servers, ushers))
    env.run(until = 100)
    
    minutes , seconds = calculate_wait_time(wait_times)
    
    print(f"Average wait time: {minutes}:{seconds}")

if __name__ == '__main__':
    main(cashiers = 7, servers = 3, ushers = 1)