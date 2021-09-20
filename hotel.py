import random as rn
import numpy as np
import pandas as pd
import simpy as sp
import matplotlib.pyplot as mpl



class hotel_monitor:
    """Monitor for the hotel class"""
    
    def __init__(self,env,hosts,rooms,staff):
        self.env = env
        
        self.host = hosts
        self.rooms = rooms
        self.staff = staff
        
        self.total = 0
        self.host_occ = []
        self.occupied = []
        self.time = []
        self.rooms_clean = []
        
    def observe(self):
        
        self.time.append(self.env.now)
        self.occupied.append(self.rooms.count)
        self.host_occ.append(self.host.count)
        self.rooms_clean.append(self.staff.count)
        
    def to_pandas(self):
        return pd.DataFrame({'time': self.time, 'bed_occupied':self.occupied,'hosts_occupied':self.host_occ,'rooms_cleaning':self.rooms_clean})
    

class hotel_model:
    """Hotel model class with enviroment class embeded"""
    
    def __init__(self,rooms,hosts,staff,seed):
        rn.seed(seed)
        self.env = sp.Environment()
        
        
        self.rooms = sp.Resource(self.env,rooms)
        self.hosts = sp.Resource(self.env,hosts)
        self.staff = sp.Resource(self.env,staff)
        
        # monitor must have the resources and the enviroment
        self.monitor = hotel_monitor(self.env,self.hosts,self.rooms,self.staff)
        
        
    def go_hotel(self):
        # Person events

        with self.hosts.request() as request:
            yield request
            yield self.env.process(self.wait_host())
            
        with self.rooms.request() as request:
            yield request
            self.monitor.total += 1
            yield self.env.process(self.wait_room())
            
            # First we have to clean the room before we release it for use
            with self.staff.request() as request:
                yield request
                yield self.env.process(self.clean_room())
            
            
    def run(self):
        # PEM
        
            
        while True:
            
            
            yield self.env.timeout(rn.gauss(20, 1))
            
            for i in range(rn.randint(1, 5)):
                self.env.process(self.go_hotel())
    
    
    def wait_host(self):
        # to wait a host is 4 minutes with a %30 of a minute in deviation
        
        yield self.env.timeout(rn.gauss(15, 1.5))
        
        
    def wait_room(self):
        # Average is 60 minutes * 8 hours , std = 30
        
        yield self.env.timeout(rn.gauss(60*6, 30))

    def clean_room(self):
        
        yield self.env.timeout(rn.gauss(40, 2.1))

    def mon(self,lapse):
        # monitor pem
        
        while True:
            yield self.env.timeout(lapse)
            self.monitor.observe()
                
            
# 30 rooms, 3 hosts, seed = 0

mod = hotel_model(rooms = 100,hosts = 3,staff = 10,seed = 1)

# Check every 10 minutes, each iteration is minute

# setup monitor
mod.env.process(mod.mon(10))

# setup pem
mod.env.process(mod.run())

# A week of simulation
mod.env.run(60*24*7)

mpl.plot(mod.monitor.occupied)
mpl.plot(mod.monitor.host_occ)
mpl.plot(mod.monitor.rooms_clean)

print(f" Total clients: {mod.monitor.total}")
data = mod.monitor.to_pandas()


