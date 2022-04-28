from ast import iter_child_nodes
import re
import random
from select import select
import numpy as np
from Simulated_Annealing_db import Simulated_Annealing

class Genetic_Algorithm:

    def __init__(self, n_population):
        self.numero_poblacion = n_population
        self.population = []
        self.fitness_list = []
        self.probability = []
        self.total_fitness = 0
        self.total_fitness_list = []
        self.orders = []
        self.best = []
        self.st_dev_list = []
        self.iteration_list = []
        self.father1 = []
        self.father2 = []

    def read_txt(self):

        orders=open("C:\\Nacho\\Facultad\\IA2\\Grupo6-IA-II\\TP1\\Ejercicio_3\\orders.txt","r")
        a = 1
        list_1 = []
        list_2 = []
        list_3 = []
        counter = 0
        for i in orders:
            list_1.append(i) #txt en una lista
            if i==("Order %s\n"%(a)):
                a = a + 1
                list_2.append(counter) #puntos donde cortar las lista del txt
            counter = counter + 1

        for i in range(len(list_2)-1):
            list_3.append(list_1[list_2[i]+1:list_2[i+1]-1])
        list_3.append(list_1[list_2[len(list_2)-1]+1:-1])
        
        list_1 = []
        list_2 = []

        for i in range(len(list_3)):
            for j in range(len(list_3[i])):
                for s in re.findall(r'-?\d+\.?\d*', list_3[i][j]):
                    list_2.append(int(s)+1)
            list_1.append(list_2)
            list_2 = []
        
        self.orders = list_1[:]
        #print(self.orders)

    def child_complete(self,father,child,pos): 
        aux=[]
        c_2=0
        c=0 
        for j in range(pos,len(father)):
            if father[j] not in child: 
                aux.append(father[j])
        for i in range(len(aux)):
            child[pos+i]=aux[i]
        aux=[]
        c_2=0
        c=0  
        for j in range(len(father)):
            if father[j] not in child: 
                aux.append(father[j])
    
        while c<len(aux):
            for j in range(pos,len(father)):
                if child[j]==0:
                    child[j]=aux[c]
                    c=c+1
            child[c_2]=aux[c]
            c=c+1
            c_2=c_2+1
        return child


    def crossover(self):
        child_1=[]
        child_2=[]
        for i in range(len(self.father1)):
            child_1.append(0)
            child_2.append(0)
        pos1=random.randrange(0,len(self.father1),1)
        pos2=pos1
        while pos1==pos2:
            pos2=random.randrange(1,len(self.father1),1) 

        if pos1<pos2:
            for i in range(pos1,pos2):
                child_1[i]=self.father2[i]
                child_2[i]=self.father1[i]
            child_1=self.child_complete(self.father1,child_1,pos2)
            child_2=self.child_complete(self.father2,child_2,pos2)
        else:
            for i in range(pos2,pos1):
                child_1[i]=self.father2[i]
                child_2[i]=self.father1[i]
            child_1=self.child_complete(self.father1,child_1,pos1)
            child_2=self.child_complete(self.father2,child_2,pos1)
        
        child_1=self.mutation(child_1)[:]
        child_2=self.mutation(child_2)[:]
        return (child_1,child_2)

    def mutation(self,child):
        if random.random()<0.05:
            pos1=random.randrange(0,len(child),1)
            pos2=pos1
            while pos1==pos2:
                pos2=random.randrange(1,len(child),1) 
            child[pos1],child[pos2]=child[pos2],child[pos1]
        return child

    def fitness(self,list_layout): #lista layout es uno de los individuos de la poblacion, osea una configuracion del layout
        fitness = 0
        #print(self.orders)
        for i in self.orders:
            #print(self.orders.index(i))
            s = Simulated_Annealing(i,list_layout)
            s.fill_dicts()
            fitness = fitness + s.sequence()[0]
            del s 
        
        return 100/fitness


    def selec_parents(self, p):
        i = random.random()
        j = 0
        l = 0
        for k in self.probability:
            if j <= i <= j+k:
                if p==1:
                    self.father1 = self.population[l][:]
                elif p==2:
                    self.father2 = self.population[l][:]
                return (l)
            j = j+k
            l = l + 1  
                 


    def first_population(self):
        individuo = []
        for i in range(100):
            individuo.append(i+1)

        while len(self.population)<self.numero_poblacion:
            a = random.sample(individuo, 100)
            if a not in self.population:
                self.population.append(a)
                
    def optimal_layout(self):
        self.read_txt()
        self.first_population()
        self.best = self.population[0][:]
        iteration=0
        
        while iteration<13:
            self.iteration_list.append(iteration)
            index_list = []
            children_list = []
            self.fitness_list = []
            self.total_fitness = 0
            self.probability = []
            aux=0
            #lista del fitness
            for i in range(len(self.population)):
                self.fitness_list.append(self.fitness(self.population[i]))
                self.total_fitness = self.total_fitness + self.fitness_list[i]
                aux = aux + 100/self.fitness_list[i]
                try:
                    if self.fitness_list[i]>self.fitness(self.best):
                        self.best = self.population[i][:]
                except:
                    pass


            #lista de fitness total 
            self.total_fitness_list.append(aux)

            #lista de probabilidades de cada individuo
            for i in range(len(self.fitness_list)):
                self.probability.append(self.fitness_list[i]/ self.total_fitness)

            #seleccion 
            for i in range(int(len(self.population)/2)):
                index_1 = self.selec_parents(1)
                self.father2 = self.father1[:]
                index_2 = index_1
                while self.father2==self.father1 and (index_1, index_2) in index_list:
                    index_2 = self.selec_parents(2)
                index_list.append((index_1, index_2))
                children_list.extend(self.crossover())
            
            #Desviación estandar relativa a la media 
            if iteration>9:
                st_dev=np.std(self.total_fitness_list[-10:])/np.average(self.total_fitness_list[-10:])
                self.st_dev_list.append(st_dev)
                if st_dev<0.01:
                    print("converge")
                    return self.best
        
            #nueva poblacion
            self.population=children_list[:]
            iteration = iteration  + 1

        #print(self.total_fitness)
        return (self.best)