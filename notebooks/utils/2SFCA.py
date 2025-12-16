import geopandas as gpd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
from shapely import geometry
import libpysal

# Default projected CRS for Singapore (SVY21)
SG_CRS_EPSG = 3414

def green_data_prepocessing(
    green,
    boundry,
    buffer,
    destination: str = 'centroids',
    edges: gpd.GeoDataFrame | None = None,
    component_buffer: float = 20,
    min_area: float = 400,
):
    """
    green space data preprocessing:
    green is the green space geodataframe;
    boundry is the city's administrative boundry;
    destination represents the fake gate of green space, 'centroids' means using centroids of 
    green space as access point. 'Entrance' means using the intersections points;
    buffer is added around the green space to do the intersection with road network, usually 20m

    """
     
    # transfer the CRS (project to Singapore CRS by default)
    boundry = boundry.to_crs(epsg=SG_CRS_EPSG)
    green = green.to_crs(epsg=SG_CRS_EPSG)
    
    # clip green space within the buffered city boundry
    # first to add a buffer around the boundry to ensure people 
    # live around the edge of the boundry could access the green space outside the city but still within distance threshold
    boundry_buffer = boundry.buffer(buffer)
    green_clip = green.clip(boundry_buffer,keep_geom_type=False)
    
    # merge the overlap green space into one polygon
    s_ = (
        gpd.GeoDataFrame(geometry=[green_clip.unary_union])
        .explode(index_parts=False)
        .reset_index(drop=True)
        .set_crs(epsg=SG_CRS_EPSG)
    )
    s_ = gpd.sjoin(s_, green_clip, how='left').drop(columns=['index_right'])
    green_dis = s_.dissolve(s_.index, aggfunc='first')
    # reset the index 
    green_dis =green_dis.reset_index(drop=True)
    # create the buffer of green space, usually ~20m, for entrance/network intersection
    green_dis['buffer_20m'] = green_dis['geometry'].buffer(component_buffer)
    
    # define the green areas that overlap with each other within 20m as the same component
    W = libpysal.weights.fuzzy_contiguity(green_dis['buffer_20m'])
    green_dis['green_components']= W.component_labels
    green_space = green_dis.dissolve('green_components')

    
    #create the centroid of the green space
    green_space['centroids'] = green_space['geometry'].centroid
    #calculate the area of the green space
    green_space['area'] = green_space['geometry'].area
    # select area threshold (m^2)
    green_space = green_space[green_space['area'] > float(min_area)]
    green_space = green_space.reset_index(drop=True)
    
    entrance = []  
    # choose different fake gate model
    # use centroid of green space 
    if destination == 'centroids':
        green_access = green_space[['centroids','area']]
        green_access.rename(columns = {'centroids': 'geometry'}, inplace = True)
        green_access['park_id'] = list(range(len(green_space)))
        
    
    # use the intersection points: the road network and buffered green space polygon
    elif destination == 'Entrance':
        if edges is None:
            raise ValueError("edges GeoDataFrame is required when destination='Entrance'.")
        # ensure edges are in same CRS
        edges = edges.to_crs(green_space.crs)
        # add the buffer of 20m for each components
        green_space['buffer'] = green_space['geometry'].buffer(component_buffer)
        for i in range(len(green_space)):
            green_area = green_space.loc[i,'geometry'].area
            intersection = green_space['buffer'][i].boundary.intersection(edges)
            try:
                for point in intersection:
                    dic = {'geometry': point, 'area': green_area, 'park_id': i}
                    entrance.append(dic)
            except: continue
    green_access = gpd.GeoDataFrame(entrance) if destination == 'Entrance' else green_access
    # if the distance of two fake entrances is less than 50m, then keep the first entrance
    green_access['buffer'] = green_access['geometry'].buffer(25)
    w_e = libpysal.weights.fuzzy_contiguity(green_access['buffer'])
    green_access['entrance_components']= w_e.component_labels
    # Delete duplicate rows based on specific columns 
    green_access =  green_access.drop_duplicates(subset=["entrance_components"], keep='first')
    green_access = green_access.reset_index(drop=True)
    
    return green_access 

# preprocessing population data
def population_data_prepocessing(
    pop,
    boundry,
    distance_threshold: float,
    pop_col: str = 'population',
):
    
    """
    population data prepocessing:
    pop is the population geodataframe;
    boundry is the city's administrative boundry; 
    distance_threshold is the walking or driving distance; 
    
    """
    
    # transfer the CRS
    boundry = boundry.to_crs(epsg=SG_CRS_EPSG)
    pop = pop.to_crs(epsg=SG_CRS_EPSG)
    
    # clip population within the city boundry
    boundry_2_buffer = boundry.buffer(2*distance_threshold)
    pop_clip = pop.clip(boundry_2_buffer,keep_geom_type=False)

    if pop_col not in pop_clip.columns:
        raise ValueError(f"Population column '{pop_col}' not found in data.")
    # remove low-population records to avoid extreme small denominators
    pop_remove = pop_clip[(pop_clip[pop_col] >= 10)].copy()
    pop_remove['area'] = pop_remove['geometry'].area

    # For polygonal census grids, drop slivers near boundary; for points, skip
    geom_types = set(pop_remove.geometry.geom_type)
    if not geom_types.issubset({"Point", "MultiPoint"}):
        med_area = pop_remove['area'].median()
        pop_remove_bound = pop_remove[pop_remove['area'] >= 0.5 * med_area]
    else:
        pop_remove_bound = pop_remove
    
    #create the centroid of the population grid cell
    pop_remove_bound['centroids'] = pop_remove_bound['geometry'].centroid
    #create the buffer of each grid cell, which equals the distance threshold
    pop_remove_bound['buffer'] = pop_remove_bound['geometry'].buffer(distance_threshold)
    # reset the index 
    pop_remove_bound  = pop_remove_bound.reset_index(drop=True)
    
    return pop_remove_bound

def get_the_index_within_dist(pop_clip, green_access, pop_col: str = 'population'):
    
    """
    this step is to create a dataframe with pairs of population grid cell and green space
    whose euclidian distance is smaller than distance threshold
    
    """
  
    k= []
    for i in range(len(pop_clip)):
        for j in range(len(green_access)):
            if green_access['geometry'][j].within(pop_clip['buffer'][i]):
            #distance. = pop_clip['centroids'][i].distance(access_point['geometry'][j])
                index = {'pop_index': i, 'green_index': j,
                         'green_area': green_access['area'][j],
                         'park_id': green_access['park_id'][j],
                         'pop_num': pop_clip.loc[i, pop_col]}
                k.append(index)
    df_index = pd.DataFrame(k)
    return df_index

def origin_node(df_index, pop_clip, G_proj: nx.Graph):
        
    """
    Function to get the nearest node id of each 
    centroid of population grid cell

    """
    # get the unique value of pop index
    pop_unique = df_index['pop_index'].unique()
    
    orig_id = []
    # get the nearest node id of each centroid of population grid cell
    for i in range(len(pop_unique)):
        pop_index = pop_unique[i]
        orig_node = ox.distance.nearest_nodes(
            G_proj,
            pop_clip.loc[pop_index, 'centroids'].x,
            pop_clip.loc[pop_index, 'centroids'].y,
        )
        dic = {'pop_index':pop_unique[i],'orig_node':orig_node}
        orig_id.append(dic)
    orig_id_df = pd.DataFrame(orig_id)
    return orig_id_df

def target_node(df_index, green_access, G_proj: nx.Graph):

    """
    Function to get the nearest node id of 
    fake entrance of UGS
    
    """
    # get the unique value of green index
    green_unique = df_index['green_index'].unique()
    target_id = []
    # get the nearest node id of each green space
    for i in range(len(green_unique)):
        green_index = green_unique[i]
        target_node = ox.distance.nearest_nodes(
            G_proj,
            green_access.loc[green_index, 'geometry'].x,
            green_access.loc[green_index, 'geometry'].y,
        )
        dic = {'green_index':green_unique[i],'target_node': target_node}
        target_id.append(dic)
    target_id_df = pd.DataFrame(target_id)
    return target_id_df

def OD_Matrix(merge, G_proj: nx.Graph):
    """
    get the real distance between each pair of population grid cell and green space 
    """
    distance = []
    for i in range(len(merge)):
        try: 
            orig_node = merge.loc[i, 'orig_node']
            target_node = merge.loc[i, 'target_node']
            dist = nx.shortest_path_length(
                G_proj, source=orig_node, target=target_node, weight='length'
            )
            distance.append(dist)
        except:
            distance.append(np.nan)
    merge['distance'] = distance
    return merge

def nearest_entrance(OD_mile): # OD_mile is the OD Matrix after selection, e.g real_distance < 1km
    unique = OD_mile['pop_index'].unique()
    OD_nearest_E = []
    for i in unique:
        df = OD_mile.loc[OD_mile['pop_index'] == i]
        df1 = df.groupby('park_id').min('distance')
        for j in df1.index:
            dic = {'pop_index': i,'park_id': j,'distance':df1.loc[j,'distance'],
              'green_area': df1.loc[j,'green_area'], 'pop_num':df1.loc[j,'pop_num']}
            OD_nearest_E.append(dic)
    OD_nearest_E = pd.DataFrame(OD_nearest_E)
    return OD_nearest_E

def M2tsfca(
    OD_nearest_E: pd.DataFrame,
    distance_threshold: float,
    supply_col: str = 'green_area',
):

    # Gaussian-like decay, normalized to 1 at distance=0 and ~0 at threshold
    OD_nearest_E['weight'] = (
        np.exp(-(OD_nearest_E['distance'] / distance_threshold) ** 2 / 2 - np.exp(-1 / 2))
        / (1 - np.exp(-1 / 2))
    ).astype(float)
    OD_nearest_E['weighted_pop'] = OD_nearest_E['weight'] * OD_nearest_E['pop_num']

    # Sum weighted population each site serves
    s_w_p = pd.DataFrame(OD_nearest_E.groupby('park_id').sum('weighted_pop')['weighted_pop'])
    s_w_p = s_w_p.rename({'weighted_pop': 'sum_weighted_pop'}, axis=1)
    middle = pd.merge(OD_nearest_E, s_w_p, how='left', on='park_id')

    if supply_col not in middle.columns:
        raise ValueError(f"Supply column '{supply_col}' not found in OD_nearest_E.")

    # Supply-demand ratio
    middle['supply_ratio'] = middle[supply_col] / middle['sum_weighted_pop']

    # Accessibility score per origin-site pair
    middle['access_score'] = middle['weight'] * middle['supply_ratio']

    # Aggregate by origin
    pop_score_df = pd.DataFrame(
        middle.groupby('pop_index').sum('access_score')['access_score']
    )

    # Diagnostics
    mean_dist = middle.groupby('pop_index').mean('distance')['distance']
    pop_score_df['mean_dist'] = mean_dist

    mean_supply = middle.groupby('pop_index').mean('supply_ratio')['supply_ratio']
    pop_score_df['mean_supply'] = mean_supply

    # If area-based supply present, include mean area for reference
    if 'green_area' in middle.columns:
        mean_area = middle.groupby('pop_index').mean('green_area')['green_area']
        pop_score_df['mean_area'] = mean_area

    return pop_score_df


def build_walk_graph_within_boundary(boundry: gpd.GeoDataFrame, network_type: str = 'walk') -> nx.Graph:
    """
    Build a projected walking graph (NetworkX) from OSM within the given boundary.
    Returns a graph projected to EPSG:3414 suitable for length-based routing.
    """
    boundry = boundry.to_crs(epsg=4326)
    poly = boundry.unary_union
    G = ox.graph_from_polygon(poly, network_type=network_type, simplify=True)
    Gp = ox.projection.project_graph(G, to_crs=f"EPSG:{SG_CRS_EPSG}")
    return Gp


def graph_edges_gdf(G: nx.Graph) -> gpd.GeoDataFrame:
    """Return edges GeoDataFrame from a projected graph for reference/intersections."""
    _, edges = ox.graph_to_gdfs(G)
    return edges