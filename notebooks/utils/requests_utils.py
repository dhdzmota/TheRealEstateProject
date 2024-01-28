import requests
import os
import yaml

PAR_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CONFIG_PATH = os.path.join(PAR_PATH, 'config.yaml')

with open(CONFIG_PATH, "r") as f:
    token = yaml.full_load(f)['inegi_denue']['token']

# NOT FINISHED YET
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
