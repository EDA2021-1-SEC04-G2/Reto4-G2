﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import time
import tracemalloc
import csv


def init_analyzer():
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos
def load_data(analyzer):
    load_countries(analyzer)
    load_landing_points(analyzer)
    load_connections(analyzer)

def load_connections(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    eventsfile = cf.data_dir + 'Data/connections.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for connection in input_file:
        model.add_csv_connection(analyzer, connection)
    model.add_capitals(analyzer)
    model.add_landing_points_connections(analyzer)
    return analyzer

def load_countries(analyzer):
    eventsfile = cf.data_dir + 'Data/countries.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for country in input_file:
        model.add_country(analyzer, country)
    return analyzer

def load_landing_points(analyzer):
    eventsfile = cf.data_dir + 'Data/landing_points.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for landing_point in input_file:
        model.add_landing_point(analyzer, landing_point)
    return analyzer

def total_vertices(analyzer):
    """
    Total de paradas de autobus
    """
    return model.total_vertices(analyzer)


def total_edges(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.total_edges(analyzer)

def total_countries(analyzer):
    return model.total_countries(analyzer)

def total_landing_points(analyzer):
    return model.total_landing_points(analyzer)

#REQUERIMIENTOS

def connected_components(analyzer,landing_name1,landing_name2):
                   
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans = model.connected_components(analyzer,landing_name1,landing_name2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time,delta_memory

def critical_landing_points(analyzer):
               
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans=model.critical_landing_points(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time,delta_memory

def minimum_path(analyzer, verta, vertb):
           
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans=model.minimum_path(analyzer, verta, vertb)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time,delta_memory

def MST(analyzer):
        
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans=model.MST(analyzer)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time,delta_memory

def countries_to_landing_point(analyzer,landing_name):
    
    ans = None
    delta_time = -1.0
    delta_memory = -1.0

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    ans=model.countries_to_landing_point(analyzer,landing_name)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    
    return ans,delta_time,delta_memory


# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
