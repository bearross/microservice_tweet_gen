# https://github.com/storerjeremy/python-semrush
from python_semrush.semrush import SemrushClient
from setting import semrush_api_key

semrush_client = SemrushClient(key=semrush_api_key)


def get_semrush_metrics(url):
    result = semrush_client.domain_organic(domain=url, database='us', export_columns='Ph,Po,Pp,Pd,Nq,Cp,Ur,Tg,Tr,Tc,Co,Nr,Td')
    return result
