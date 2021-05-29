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
 """

import config as cf
import model
import csv


def init_analyzer():
    analyzer = model.newAnalyzer()
    return analyzer


# Funciones para la carga de datos
def load_data(analyzer):
    load_connections(analyzer)
    load_countries(analyzer)
    load_countries(analyzer)

def load_connections(analyzer):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    eventsfile = cf.data_dir + 'Prep Data/connections.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for connection in input_file:
        model.addStopConnection(analyzer, connection)
    model.addRouteConnections(analyzer)
    return analyzer

def load_countries(analyzer):
    eventsfile = cf.data_dir + 'Prep Data/countries.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for country in input_file:
        model.add_country(analyzer, country)
    return analyzer

def load_landing_points(analyzer):
    eventsfile = cf.data_dir + 'Prep Data/landing_points.csv'
    input_file = csv.DictReader(open(eventsfile, encoding='utf-8-sig'))
    for landing_point in input_file:
        model.add_landing_point(analyzer, landing_point)
    return analyzer

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)
def total_countries(analyzer):
    return model.total_countries(analyzer)

def total_landing_points(analyzer):
    return model.total_landing_points(analyzer)


def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """

    ans = model.connectedComponents(analyzer)


    return ans