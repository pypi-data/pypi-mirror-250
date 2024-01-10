import icoscp_core.sites as sites
from typing import List, Dict
import geopandas as gpd
import pandas as pd




def get_sites_stations_list(inactive_stations_ids=["TRS"])->List[Dict]:
    """
    Retrieves a list of stations from the ICOS-CP API and compiles their details into a list of dictionaries.
    The function allows specifying which stations should be marked as 'inactive'.

    Args:
        inactive_stations_ids (list of str, optional): A list of station IDs that should be marked as 'inactive'. 
            Default is ["TRS"].

    Returns:
        List[Dict[str, Union[str, float]]]: A list of dictionaries, each containing details of a station. 
        The keys in the dictionary are 'id', 'name', 'status', 'latitude', 'longitude', and 'uri'.

    Raises:
        ConnectionError: If there is an issue connecting to the ICOS-CP API.
        ValueError: If the data returned from the API is not in the expected format.

    Note:
        - The function assumes the existence of 'sites.meta.list_stations()' method from the ICOS-CP API.
        - It's important to handle potential errors to prevent the application from crashing due to unforeseen issues.
    """
    stations = []
    sstc = {
                'id': 'SSTC', 
                "name": 'SITES Spectral Thematic Center', 
                'status': 'active', 
                "latitude": 55.7119, 
                "longitude": 13.2107, 
                "uri": "https://www.fieldsites.se/en-GB/sites-thematic-programs/sites-spectral-32634403"
            }
    try:
        # Attempt to get the list of stations from the ICOS-CP API
        station_data = sites.meta.list_stations()
    except Exception as e:
        raise ConnectionError(f"Error connecting to the ICOS-CP API: {e}")

    for dobj in station_data:
        try:
            # Check for expected attributes in each station object
            if not all(hasattr(dobj, attr) for attr in ['id', 'name', 'lat', 'lon', 'uri']):
                raise ValueError(f"Station object is missing one or more required attributes: {dobj}")

            # Determine the status of the station
            status = 'inactive' if dobj.id in inactive_stations_ids else 'active'

            # Append station details to the list
            stations.append({
                'id': dobj.id, 
                "name": dobj.name, 
                'status': status, 
                "latitude": dobj.lat, 
                "longitude": dobj.lon, 
                "uri": dobj.uri
            })
        except ValueError as ve:
            # Optionally log the error or handle it as needed
            print(f"Data format error: {ve}")
            continue  # Skip this station and continue with the next one
    
    stations.append(sstc)  # Add the SSTC station to the list
    
    return stations


def get_stations_geodataframe(epsg=4326):
    """
    Retrieves station data, converts it into a GeoDataFrame, and sets the specified coordinate reference system (CRS).

    The function first calls 'get_sites_stations_list' to retrieve station data. This data is then converted into 
    a pandas DataFrame. Each station's longitude and latitude are used to create a 'Point' geometry, which is necessary 
    for geospatial analysis. Finally, the DataFrame is converted into a GeoDataFrame, and the CRS is set based on 
    the given EPSG code.

    Args:
        epsg (int, optional): The EPSG code for the desired coordinate reference system. Default is 4326 
            (WGS 84 - World Geodetic System 1984).

    Returns:
        geopandas.GeoDataFrame: A GeoDataFrame containing station data with geometry and specified CRS.

    Raises:
        ImportError: If required modules (pandas, geopandas, shapely) are not installed.
        Exception: For any other unforeseen errors during the function execution.

    Example:
        >>> gdf = get_stations_geodataframe(epsg=4326)
        >>> print(gdf.head())

    Note:
        - This function depends on 'get_sites_stations_list', 'pandas', 'geopandas', and 'shapely' being available.
        - It's important to ensure the EPSG code provided is valid and appropriate for the intended geospatial analysis.
    """
    from shapely.geometry import Point
    
    try:
        # Retrieve station data using the get_sites_stations_list function
        stations = get_sites_stations_list()

        # Convert the list of station data into a pandas DataFrame
        df = pd.DataFrame(stations)

        # Create a Point geometry for each station
        df['geometry'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

        # Convert to GeoDataFrame and set CRS
        gdf = gpd.GeoDataFrame(df, geometry='geometry')
        gdf.set_crs(epsg=epsg, inplace=True)

        return gdf
    except ImportError as ie:
        raise ImportError(f"Missing required module: {ie}")
    except Exception as e:
        raise Exception(f"An error occurred in get_stations_geodataframe: {e}")


