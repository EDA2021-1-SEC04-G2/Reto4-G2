"""
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
import sys
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import haversine as hs
assert config

default_limit=1000
sys.setrecursionlimit(default_limit*10000)

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

def add_csv_connection(analyzer, connection):
    landing_id1=connection['origin']
    landing_id2=connection['destination']
    cable_name=connection['cable_name']
    distance=distance_landing(analyzer, landing_id1, landing_id2)
    add_connection(analyzer, landing_id1, landing_id2, cable_name, distance)


def add_connection(analyzer, landing_id1, landing_id2, cable_name, distance):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = format_vertex(landing_id1, cable_name)
        destination = format_vertex(landing_id2, cable_name)
        add_vertex(analyzer, origin)
        add_vertex(analyzer, destination)
        add_edge(analyzer, origin, destination, distance)
        add_landing_point_cable(analyzer, landing_id1, cable_name)
        add_landing_point_cable(analyzer, landing_id2, cable_name)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:add_connection')

def add_capitals(analyzer):
    countries=analyzer['countries']
    landing_info=analyzer['landing_points_info']
    for country_name in lt.iterator(m.keySet(countries)):
        country=m.get(countries,country_name)['value']
        capital_name=country['CapitalName']
        capital_info={'landing_point_id':capital_name, 'latitude':country['CapitalLatitude'],
                      'longitude':country['CapitalLongitude'],'Sub':False, 'name':capital_name}
        add_landing_point(analyzer, capital_info)
        encontrar=False
        mindist=-1
        minland=''
        for landing_id in lt.iterator(m.keySet(landing_info)):
            landing_dic=m.get(landing_info,landing_id)['value']
            if landing_dic['Sub']==True:
                country2=landing_dic['name'].split(', ')[-1]
                distance=distance_landing(analyzer, capital_name, landing_id)
                if country2==country_name:
                    encontrar=True
                    landing_point_cables=m.get(analyzer['landing_points_cables'],landing_id)['value']
                    for cable_name in lt.iterator(landing_point_cables):
                        add_connection(analyzer, capital_name, landing_id, cable_name, distance)
                if mindist==-1 or distance<mindist:
                    mindist=distance
                    minland=landing_id
        if not encontrar:
            landing_point_cables=m.get(analyzer['landing_points_cables'],minland)['value']
            for cable_name in lt.iterator(landing_point_cables):
                add_connection(analyzer, capital_name, minland, cable_name, mindist)
    


    
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

def add_landing_point_cable(analyzer, landing_id, cable_name):
    
    entry = m.get(analyzer['landing_points_cables'], landing_id)
    if entry is None:
        lstcables = lt.newList(cmpfunction=compare_cables_name)
        lt.addLast(lstcables, cable_name)
        m.put(analyzer['landing_points_cables'], landing_id, lstcables)
    else:
        lstcables = entry['value']
        if not lt.isPresent(lstcables, cable_name):
            lt.addLast(lstcables, cable_name)
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

def name_to_id(analyzer, landing_name):
    landing_info=analyzer['landing_points_info']
    for landing_point in lt.iterator(m.valueSet(landing_info)):
        landing_name2=landing_point['name']
        if landing_name2==landing_name:
            return landing_point['landing_point_id']

# Funciones utilizadas para comparar elementos dentro de una lista
def connected_components(analyzer,landing_name1,landing_name2):
    #req 1
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    landing_id1=name_to_id(analyzer,landing_name1)
    landing_id2=name_to_id(analyzer,landing_name2)
    cable1=lt.getElement(m.get(analyzer['landing_points_cables'],landing_id1)['value'],1)
    cable2=lt.getElement(m.get(analyzer['landing_points_cables'],landing_id2)['value'],1)
    verta=format_vertex(landing_id1,cable1)
    vertb=format_vertex(landing_id1,cable2)
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    connected=scc.stronglyConnected(analyzer['components'],verta,vertb)
    return scc.connectedComponents(analyzer['components']),connected

# Funciones de ordenamiento
def format_vertex(landing_point_id, cable_name):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = landing_point_id + '-'+ cable_name
    return name

def distance_landing(analyzer, landing_id1, landing_id2):
    latitude1=m.get(analyzer['landing_points_info'],landing_id1)['value']['latitude']
    latitude2=m.get(analyzer['landing_points_info'],landing_id2)['value']['latitude']
    longitude1=m.get(analyzer['landing_points_info'],landing_id1)['value']['longitude']
    longitude2=m.get(analyzer['landing_points_info'],landing_id2)['value']['longitude']
    coo1=(float(latitude1),float(longitude1))
    coo2=(float(latitude2),float(longitude2))
    dist=hs.haversine(coo1,coo2)
    return dist

def compare_cables_name(route1, route2):
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
    return m.size(analyzer['landing_points_info'])
