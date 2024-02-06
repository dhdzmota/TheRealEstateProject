import requests
import os
import yaml

PAR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(PAR_PATH, 'config.yaml')


def inegi_denue_search_places(method='Buscar',
                              key_word=None,
                              latitude=None,
                              longitude=None,
                              radio=2500,
                              name_place=None,
                              state=00,
                              economic_activity=0,
                              geo_area='01',
                              estrato=0
                              ):
    '''
    # YET TO FINISH
    Function for data collection using INEGI DENUE API.

    Available methods:
    - Buscar: (default) Performs a query to retrieve all
    establishments that meet the specified conditions.
    - Nombre: Conducts a search for all establishments by
    name or business name, with the option to narrow down
    the results by federal entity.
    - Cuantificar: Conduct a count of all establishments
    with the option to refine the search by geographical
    area, economic activity, and stratum.

    More info: https://www.inegi.org.mx/servicios/api_denue.html
    '''
    with open(CONFIG_PATH, "r") as f:
        token = yaml.full_load(f)['inegi_denue']['token']

    base_url = f'https://www.inegi.org.mx/app/api/denue/v1/consulta/{method}/'
    url_buscar = f'{key_word}/{latitude},{longitude}/{radio}/{token}'
    url_name = f'{name_place}/{state}/1/1000/{token}'
    url_cuantificar = f'{economic_activity}/{geo_area}/{estrato}/{token}'
    urls = {'Buscar': url_buscar,
            'Nombre': url_name,
            'Cuantificar': url_cuantificar}
    try:
        return requests.get(base_url + urls[method]).json()

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")


def foursquare_search_places(key_word=None,
                             latitude=None,
                             longitude=None,
                             radio=2500,
                             categories=None,
                             chains=None,
                             exclude_chains=False,
                             exclude_all_chains=False,
                             min_price=1,
                             max_price=4,
                             near=None,
                             polygon=None,
                             sort='relevance',
                             limit=50
                             ):
    '''
    Function for data collection using Foursquare Places API.
    Search for places in the FSQ Places database using a location
    and querying by name, category name, telephone number, taste
    label, or chain name. For example, search for "coffee" to get
    back a list of recommended coffee shops.

    You may pass a location with your request by using one of the
    following options. If none of the following options are passed,
    Place Search defaults to geolocation using ip biasing with the
    optional radius parameter.

    ll & radius (circular boundary)
    near (geocodable locality)

    Documentation link:
    https://location.foursquare.com/developer/reference/place-search


    Params:
    - query: string. A string to be matched against all content for
    this place, including but not limited to venue name, category,
    telephone number, taste, and tips.
    - latitude: float. Latitude coordinate around which to retrieve
    place information
    - longitude: float. Longitude coordinate around which to retrieve
    place information
    - radius: int. Sets a radius distance (in meters) used to
    define an area to bias search results. The maximum allowed radius
    is 100,000 meters. Radius can be used in combination with ll or ip
    biased geolocation only. By using radius, global search results
    will be omitted.
    - categories: string. Filters the response and returns FSQ Places
    matching the specified categories. Supports multiple Category IDs,
    separated by commas. For a complete list of Foursquare Category IDs,
    refer to the Category Taxonomy page.
    - chains: string. Filters the response and returns FSQ Places
    matching the specified chains. Supports multiple chain IDs,
    separated by commas. For more information on Foursquare Chain IDs,
    refer to the Chains page.
    - exclude_chains: string. Filters the response and returns FSQ Places
    not matching any of the specified chains. Supports multiple chain IDs,
    separated by commas. For more information on Foursquare Chain IDs,
    refer to the Chains page.
    - exclude_all_chains: boolean. Filters the response by only returning
    FSQ Places that are not known to be part of any chain.
    - min_price: int. Restricts results to only those places within the
    specified price range. Valid values range between 1 (most affordable)
    to 4 (most expensive), inclusive.
    - max_price: int. Restricts results to only those places within the
    specified price range. Valid values range between 1 (most affordable)
    to 4 (most expensive), inclusive.
    - near: string. A string naming a locality in the world
    (e.g., "Chicago, IL"). If the value is not geocodable, returns an error.
    - polygon: string. A string containing the list of coordinates which
    define the edges of the polygon. Must have at least 4 coordinates and
    be considered a "closed" polygon.
    - sort: string. Specifies the order in which results are listed.
    Possible values are: relevance (default), rating, distance.
    - limit: int. The number of results to return, up to 50. Defaults to 50.
    '''
    params = list(
        foursquare_search_places.__code__.co_varnames
    )[:foursquare_search_places.__code__.co_argcount]
    with open(CONFIG_PATH, "r") as f:
        token = yaml.full_load(f)['foursquare']['token']
    url = "https://api.foursquare.com/v3/places/search?"
    ll = f"{latitude},{longitude}"
    headers = {"accept": "application/json",
               "Authorization": token}
    params.remove('longitude')
    params = [v.replace('latitude', 'll') for v in params]
    for p in params:
        if eval(p) is not None:
            url += f"{p}={eval(p)}&"
    url = url[:-1]
    print(url)
    try:
        return requests.get(url, headers=headers, verify=False).json()

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
