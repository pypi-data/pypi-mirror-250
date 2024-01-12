import structlog
import requests


log = structlog.get_logger()


def get_alpha3_code(country_name):
    """
    To get alpha3code from OpenDataSoft API.
    :param country_name:
    :return: Alpha3code or country name in case alpha3code couldn't be retrieved.
    """
    url = (f"https://public.opendatasoft.com/"
           f"api/explore/v2.1/catalog/datasets/countries-codes/records?"
           f"select=iso3_code&where=label_en='{country_name}'&limit=1")
    try:
        response = requests.get(url)
        response.raise_for_status()
        country = response.json()['results'][0]['iso3_code']
        return country
    except IndexError:
        log.warning(f'Could not find Alpha3code for country {country_name}.')
    except Exception as e:
        log.error(f"Unable to get alpha3 code for {country_name} due to the following error: {e}")

    return None
