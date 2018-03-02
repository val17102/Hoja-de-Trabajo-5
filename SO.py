import simpy
import math
import random



mram = 100

instrucciones = 3

tiempos = []

capacidad_procesos = 2

intervalo = 10

cantidad_procesos = 25

env = simpy.Environment()

ram = simpy.Container(env, init = mram, capacity = mram)
 
cpu = simpy.Resource(env, capacity = capacidad_procesos)

class SO:
    def __init__(self):
        self.poop = 0
        

class Proceso:
    def __init__(self, nom, num, env, so):
        self.env = env
        self.terminado = False
        self.nombre = nom
        self.memoriaR = random.randint(1,10)
        self.numInstrucciones = random.randint(1,10)
        self.tiempo_crear = 0
        self.tiempo_fin = 0
        self.tiempo_total = 0
        self.numero = num
        self.sistema_operativo = so
        self.proceso = env.process(self.procesar(env, so))

    def crear_proceso(env, i):
        tiempo_crear = random.expovariate(1.0/intervalo)
        Proceso('Proceso' % i, i, env)
        yield env.timeout(tiempo_crear)

    def procesar(self, env):
        self.tiempo_crear = env.now
        print("Nuevo proceso a las ",self.tiempo_crear)
        with ram.get(self.memRequerida) as getRam:
            yield getRam
            siguiente = 0
            while not self.terminado:
                with cpu.request() as req:
                    yield req
                    for i in range(instrucciones):
                        if self.numInstrucciones > 0:
                            self.numInstrucciones = self.numInstrucciones - 1
                            siguiente = random.randint(0,1)
                    yield env.timeout(1)
            
                    if siguiente == 0:
                        yield env.timeout(5)
                    if self.numInstrucciones == 0:
                        self.terminado = True
            print()
            ram.put(self.memoriaR)
        self.tiempo_fin = env.now
        self.timepo_total = int(self.tiempo_fin - self.tiempo_crear)
        tiempos.insert(self.numero, self.tiempo_total)

class Main():
    def _init_(self):
        sistema_operativo = SO()
        for i in range (cantidad_procesos):
            env.process(crear_proceso(env, i))
        env.run()
        tiempoPromedio = (sum(tiempos)*1.0/(len(tiempos))
        print("Promedio: ", tiempoPromedio)

Main()
        


    
                
        
    


