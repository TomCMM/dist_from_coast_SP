#===============================================================================
# DESCRIPTION
#     The aim of this scipt is to retrieve the nearest ditance of a point from 
#    a shape file. In ou case the coastline shapefile
#===============================================================================

import fiona
import pandas as pd
from shapely import geometry as geo
import numpy as np
from scipy.spatial import KDTree

from shapely.geometry import Polygon, Point, LinearRing, mapping


def get_shape_coordinates(shape_path):
    """
    PARAMETERES
        Path of the shape file ".shp"
    RETURN
        All shape coordinates from a shape file 
    """
    # coordinates = np.empty([1, 2])
    with fiona.open(shape_path) as fiona_collection:
        print(fiona_collection)
        for feature in fiona_collection:
            print('asdohvbsoa')
            sh_polygon =  geo.asShape(feature['geometry'] ) # shape polygon
            sh_coordinates = mapping(sh_polygon)['coordinates'] # shape coordinates
            
            coordinate = np.asarray(sh_coordinates)#[0]
            # try:
            #     coordinates = np.vstack((coordinates,coordinate)) # convert to array
            # except ValueError:
            #     pass
            # print "Coordinates from collection stacked"
            
    return coordinate

def distance_from_shape(stalat, stalon, sh_coordinates):
    """
    PARAMETERS
        stalat, pd.serei with the latitude of the stations
        stalon, pd.serei with the longitude of the stations
        sh_coordinates, numpy array with the position of the shape
    """

    n=1 # nb of neighboors
    tree = KDTree(sh_coordinates)
    querypoint = list(zip(stalon.values, stalat.values))
    distance, index = tree.query(querypoint, n)
    print("Position of the station:  " + str(querypoint))
    print("Position of the nearest shape file :  " + str(sh_coordinates[index]))
    print("The minimum distance (cartesian) from a station is " + str(distance) +" degree" )

    return distance

def dist_side_from_nearest_shape( stalat, stalon, sh_coordinates, latlon='Lon'):
    """
    PARAMETERS
        stalat, pd.serei with the latitude of the stations
        stalon, pd.serei with the longitude of the stations
        sh_coordinates, numpy array with the position of the shape
        latlon: return the position in the latitude longitude
    """

    n=1 # nb of neighboors
    tree = KDTree(sh_coordinates)
    querypoint = zip(stalon.values, stalat.values)
    distance, index = tree.query(querypoint, n)

    print("Position of the station:  " + str(querypoint))
    print("Position of the nearest shape file :  " + str(sh_coordinates[index]))
    print("The minimum distance (cartesian) from a station is " + str(distance) +" degree")

    nearest_point_shp = np.array([sh_coordinates[i,:] for i in index])
    if latlon == "Lon":
        sign_side = np.sign(nearest_point_shp[:,0] - stalon.values)
    else:
        sign_side = np.sign(nearest_point_shp[:,0] - stalat.values)

    dist_side = distance * sign_side
    return dist_side

if __name__ == '__main__':

    #####################################
    # Minimal example
    ######################################
    shape_path = "shapefile_coast.shp"
    sh_coordinates = get_shape_coordinates(shape_path)

    stalat = pd.Series([-23])
    stalon = pd.Series([-46])

    distance_from_shape(stalat, stalon, sh_coordinates[0])




