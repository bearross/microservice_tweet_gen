# https://github.com/seomoz/SEOmozAPISamples/tree/master/python
from mozscape import Mozscape
from setting import moz_access_id, moz_secret_key

moz_client = Mozscape(moz_access_id, moz_secret_key)


def get_url_metrics(urls):
    """ get url metric from url list """
    # metrics = client.urlMetrics(['www.moz.com', 'www.moz.com'])
    # mozMetrics = client.urlMetrics('www.moz.com')
    try:
      authorities = moz_client.urlMetrics(urls, Mozscape.UMCols.domainAuthority | Mozscape.UMCols.pageAuthority)
    except Exception as e:
      authorities = None
    
    return authorities
