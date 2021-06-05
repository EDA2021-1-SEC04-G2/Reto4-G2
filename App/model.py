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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import haversine as hs
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landing_points': None,
                    'connections': None,
                    'components': None,
                    'paths': None,
                    'countries':None
                    }
        #informacion de los cables de cada landing point, los valores son listas de cables
        analyzer['landing_points_cables'] = m.newMap(numelements=1280,
                                     maptype='PROBING')
        #diccionarios con informacion de cada landing point, los valores son diccionarios con caracteristicas
        analyzer['landing_points_info'] = m.newMap(numelements=1280,
                                     maptype='PROBING')
        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=False,
                                              size=1280,
                                              comparefunction=compare_vertices)
        analyzer['countries'] = m.newMap(numelements=1280,
                                     maptype='PROBING')
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')

# Funciones para agregar informacion al catalogo

def add_country(analyzer,country):
    m.put(analyzer['countries'],country['CountryName'],country)

def add_landing_point(analyzer,landing_point):
    m.put(analyzer['landing_points_info'],landing_point['landing_point_id'],landing_point)

def add_connection(analyzer, connection):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(connection, connection['origin'])
        destination = format_vertex(connection, connection['destination'])
        weight=0
        if connection['cable_length']!='n.a.':
            cable_length=float(connection['cable_length'][:-3].replace(',','')) 
            weight=cable_length
        band_with=connection['capacityTBPS']
        add_vertex(analyzer, origin)
        add_vertex(analyzer, destination)
        add_edge(analyzer, origin, destination, weight)
        add_landing_point_cable(analyzer, connection)
        add_capital(connection,analyzer)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:add_connection')

def add_capital(analyzer,connection):
    landing=connection['origin']
    landing_point=m.get(analyzer['landing_points_info'],landing)['value']
    country=landing_point['name'].split(', ')[-1]
    capital=m.get(analyzer['countries'],country)['value']
    capital_name=capital['CapitalName']
    latitude_origin=float(landing_point['latitude'])
    longitude_origin=float(landing_point['longitude'])
    origin_coo=(latitude_origin,longitude_origin)
    latitude_capital=float(capital['CapitalLatitude'])
    longitude_capital=float(capital['CapitalLongitude'])
    capital_coo=(latitude_capital,longitude_capital)
    distance=hs.haversine(origin_coo,capital_coo)
    capital_vertex=format_vertex(connection,capital_name)
    add_vertex(analyzer,capital_vertex)  


    
def add_vertex(analyzer, vertex):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], vertex):
            gr.insertVertex(analyzer['connections'], vertex)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:add_vertex')

def add_edge(analyzer, origin, destination, weight):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, weight)
    return analyzer

def add_landing_point_cable(analyzer, connection):
    
    entry = m.get(analyzer['landing_points_cables'], connection['origin'])
    if entry is None:
        lstcables = lt.newList(cmpfunction=compare_cables_id)
        lt.addLast(lstcables, connection['cable_id'])
        m.put(analyzer['landing_points_cables'], connection['origin'], lstcables)
    else:
        lstcables = entry['value']
        info = connection['cable_id']
        if not lt.isPresent(lstcables, info):
            lt.addLast(lstcables, info)

    #como no es dirigido hay que agregar ambos vertices

    entry = m.get(analyzer['landing_points_cables'], connection['destination'])
    if entry is None:
        lstcables = lt.newList(cmpfunction=compare_cables_id)
        lt.addLast(lstcables, connection['cable_id'])
        m.put(analyzer['landing_points_cables'], connection['destination'], lstcables)
    else:
        lstcables = entry['value']
        info = connection['cable_id']
        if not lt.isPresent(lstcables, info):
            lt.addLast(lstcables, info)
    return analyzer

def add_landing_points_connections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lstcon = m.keySet(analyzer['landing_points_cables'])
    for key in lt.iterator(lstcon):
        lstcables = m.get(analyzer['landing_points_cables'], key)['value']
        prevcable = None
        for cable in lt.iterator(lstcables):
            cable = key + '-' + cable
            if prevcable is not None:
                weight=0.1
                add_edge(analyzer, prevcable, cable, weight)
            prevcable = cable

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista
def connected_components(analyzer,verta,vertb):
    #req 1
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    connected=scc.stronglyConnected(analyzer['components'],verta,vertb)
    return scc.connectedComponents(analyzer['components']),connected

# Funciones de ordenamiento
def format_vertex(connection, landing_point):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = landing_point + '-'
    name = name + connection['cable_id']
    return name

def compare_cables_id(route1, route2):
    """
    Compara dos rutas
    """
    if (route1 == route2):
        return 0
    elif (route1 > route2):
        return 1
    else:
        return -1

def compare_vertices(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def total_vertices(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def total_edges(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])

def total_countries(analyzer):
    return m.size(analyzer['countries'])

def total_landing_points(analyzer):
    return m.size(analyzer['landing_points_cables'])
