
import random
import math
import time
import numpy


class Simulated_Annealing:

    def __init__(self, nodes, list_layout, df):

        self.dict_cost={}
        self.nodes = nodes[:]
        self.nodes.append(0)
        self.nodes.insert(0, 0)
        self.list_layout = list_layout[:]
        self.df = df
        self.costs_list = []


    def cost(self,state):
        
        cost = 0
        for i in range(1, len(state)-1):
            cost = cost + self.dict_cost["%s->%s"%(state[i],state[i+1])]
        
        return cost
    
    def log30(self, t):
        return math.log(t, 30)

    def fill_dicts(self):

        """
        Crea dos diccionarios, uno con los costos de ir de un nodo a otro y otro con el camino entre nodos
        """

        for i in range(len(self.nodes)):
            for j in range(len(self.nodes)):
                if self.nodes[i] != self.nodes[j]:
                    if self.nodes[i] == 0:
                        id = '100->%s'%(self.list_layout.index(j))
                    elif self.nodes[j] == 0:
                        id = '%s->100'%(self.list_layout.index(i))
                    else:
                        id = '%s->%s'%(self.list_layout.index(i), self.list_layout.index(j))
                    self.dict_cost["%s->%s"%(self.nodes[i], self.nodes[j])] = self.df.loc["%s->%s"%(self.nodes[i], self.nodes[j]),"costo"]

    def sequence(self, alpha, t):
        
        """
        Ejecuta el algoritmo de recocido simulado y devuelve una lista con el mejor orden que encontro, 
        el costo de dicho orden y ademas una lista de las T y una de los costos de cada orden que ha ido
        encontrando para graficarlos 
        """   

        """if 0<len(self.nodes)<=10:
            t = t - 1000
        elif 10<len(self.nodes)<=20:
            t = t
        elif 20<len(self.nodes)<=30:
            t = t + 500
        else:
            t = t + 1000
        """
        new = self.nodes[:] #Nuevo estado depues de permutar sus nodos
        b_state = self.nodes[:] #Mejor estado econtrado
        c_state = self.nodes[:] #Estado actual con el que trabaja el algoritmo
        
        best_cost = 0

        #Listas para graficar
        cost_list = []
        temperature_list = []
        iteration_list = []
        
        

        while True:

            T = alpha(t)

            t = t - 1

            if T<0.00001:
                return (best_cost, b_state, cost_list, temperature_list, list(reversed(iteration_list))) 

            temperature_list.append(T)
            iteration_list.append(t)

            pos1=random.randrange(1,(len(c_state)-1),1) 
            pos2=pos1

            while pos1==pos2:
                pos2=random.randrange(1,(len(c_state)-1),1) 

            new[pos1],new[pos2] = new[pos2],new[pos1]

            cost1=self.cost(c_state)
            cost2=self.cost(new)
            deltaE=cost2-cost1

            if deltaE<0 or (random.random()<(math.exp(-deltaE/T)) and deltaE>0):
                c_state=new[:]
                cost1=cost2
                
            if cost1<best_cost or best_cost == 0:
                b_state=c_state[:]
                best_cost=cost1
            
            cost_list.append(cost1)
            new = c_state[:]


                



    