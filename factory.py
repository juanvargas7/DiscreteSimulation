#    Guitar Factory

import simpy as sp
import random as rn


class Monitor:
    
    def __init__(self,env):
        self.env = env
        self.y = []
        self.t = []
    
    def observe(self,y):
        self.y.append(y)
        self.t.append(self.env.now)




class GuitarFactory:
    
    def __init__(self, env, neck_maker, body_maker, painter, assembler):
        self.env = env
        
        # Material
        
        self.wood = sp.Container(capacity=100, init = 100)
        self.electronic = sp.Container(capacity=100, init = 10)
        
        # Inventory
        
        self.neck = sp.Container(capacity=100, init =0)
        self.body = sp.Container(capacity=100, init = 0)
        self.pre_paint = sp.Container(capacity=100, init =0)
        self.post_paint = sp.Container(capacity=100, init = 0)
        
        # product 
        self.guitars = sp.Container(capacity=100, init = 0)
        
        
    def make_neck(self, monitor):
        while True:
            yield self.wood.get(1)
            monitor.observe(self.wood.level())
            yield self.env.timeout(rn.normalvariate(45/60, 2/60))
            yield self.neck.put(1)
            monitor.observe(self.neck.level())
        
    def make_body(self, monitor):
        while True:
            yield self.wood.get(1)
            monitor.observe(self.wood.level())
            yield self.env.timeout(rn.normalvariate(40/60, 1/60))
            yield self.body.put(1)
            monitor.observe(self.body.level())
            
    def assemble_guitar(self, monitor):
        while True:
            yield self.electronic.get(1)
            monitor.observe(self.electronic.level())
            yield self.neck.get(1)
            monitor.observe(self.neck.level())
            yield self.post_paint.get(1)
            monitor.observe(self.post_paint.level())
            
            yield self.env.timeout(11/60,0.1/60)
            
            yield self.guitar.put(1)
            monitor.observe(self.guitars.level())
            
    def paint(self, monitor):
        while True:
            yield self.pre_paint.get(1)
            yield self.env.timeout(rn.normalvariate(21/60, 2/60))
            yield self.post_paint.put(1)
            monitor.observe(self.post_paint.level())
            

# PEM

def run(env, shop):
    env.process(shop.make_neck())
    env.process(shop.make_body())
    env.process(shop.paint())
    env.process(shop.assemple_guitar())

    
    