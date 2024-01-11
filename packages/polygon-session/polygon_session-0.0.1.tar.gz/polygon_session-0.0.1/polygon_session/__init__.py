import os
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from requests import Session, get

retry_strategy = Retry(
    total=8,
    backoff_factor=0.125,
    status_forcelist=[429, 500, 502, 503, 504],
    # method_whitelist=["HEAD", "GET", "OPTIONS", "POST", "DELETE"]
)

class Polygon:
    def get(self, path, **kwargs):
        if not path.startswith('http'):
            kwargs = {k.replace('_', '.'):v for k, v in kwargs.items()}
            if not path.startswith('https://api.polygon.io'):
                path = 'https://api.polygon.io' + path
            if kwargs:
                path = path + '?' + urllib.parse.urlencode(kwargs)
        response = super().get(path)
        return response

class PolygonSession(Polygon, Session):
    def __init__(self):
        adapter = HTTPAdapter(max_retries=retry_strategy)
        super().__init__()
        self.mount("https://", adapter)
        try:
            key = os.environ['POLYGON_KEY']
        except KeyError:
            print("You must put your polygon key in an environment varialbe called 'POLYGON_KEY' ala:", file=sys.stderr)
            print("  export POLYGON_KEY='...'", file=sys.stderr)
            raise
        
        self.headers.update({'Authorization': f'Bearer {key}'})

