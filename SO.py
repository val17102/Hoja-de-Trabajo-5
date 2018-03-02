import simpy
import random
import math

random.seed(10)

mram = 100

instrucciones = 3

operacion = 5

tiempos = []

capacidad_proceso = 2

intervalo = 10

cantidad_procesos = 25


class SO:
        def __init__ (self, env):
                self.ram = simpy.Container(env, init=mram, capacity=mram)
                self.cpu = simpy.Resource(env, capacity=capacidad_proceso)

class Proceso:
    def __init__(self, nom, num,env, so):
        self.env = env
        self.terminado = False
        self.nombre = nom
        self.numInstrucciones = random.randint(1,10)
        self.memoriaR = random.randint(1,10) 
        self.tiempo_crear = 0 
        self.tiempo_fin = 0 
        self.tiempo_total = 0 
        self.numero = num 
        self.sistema_operativo = so
        self.proceso = env.process(self.procesar(env, so))

    def procesar(self,env,so):
        inicio = env.now
        self.tiempo_crear = env.now
        print ('%s: creado a las %d.'%(self.nombre, inicio))
        with so.ram.get(self.memoriaR) as getRam:  
                yield getRam
                print('%s: esta en la Ram a las %d.' % (self.nombre, env.now)) 
                siguiente = 0 
                
                while not self.terminado: 
                        with so.cpu.request() as req:
                                print('%s: quiere entrar al CPU a las %d.' % (self.nombre, env.now))
                                yield req
                                print('%s: entra al CPU a las %d.' % (self.nombre, env.now))
                                for i in range (instrucciones):  
                                        if self.numInstrucciones > 0:
                                                self.numInstrucciones = self.numInstrucciones - 1
                                                siguiente = random.randint(0,2)  
                                yield env.timeout(1)  
                                if siguiente == 0:
                                        yield env.timeout(operacion)
                                if self.numInstrucciones ==1:
                                        self.terminado = True
                print('%s: terminado a las %d' % (self.nombre, env.now))
                so.ram.put(self.memoriaR) 
        self.tiempo_fin = env.now
        self.tiempo_total = int(self.tiempo_fin - self.tiempo_crear) 
        tiempos.insert(self.numero, self.tiempo_total) 


def crear_procesos(env, so,i):
        tiempo_crear = random.expovariate(1.0/intervalo)
        Proceso('Proceso # %d' % i, i, env, so)
        yield env.timeout(tiempo_crear)  
    
class principal(object):     
    def __init__(self):
        env = simpy.Environment()  
        sistema_operativo = SO(env)  
        for i in range (cantidad_procesos):
                env.process(crear_procesos(env, sistema_operativo,i))  
        env.run()       

        tiempoTotalPromedio = sum(tiempos)*1.0/(len(tiempos))

        print ("El tiempo Promedio es de: ", tiempoTotalPromedio)




principal()

