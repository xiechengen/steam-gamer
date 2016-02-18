import json
import datetime
import urllib2
from time import sleep

class SteamError(Exception):
    pass

class SteamAPI:
    """Base class for our other Steam API classes"""
    api_key = 'FC65FE32E5732FC54BC70256CDA122BB'
    steam_id = '76561198053933752'
    time = 0.01
    retries = 20

    def __init__(self, steam_id, api_key):
        """Sets the steam id of the user in question and your API key."""
        self.api_key = api_key
        self.steam_id = steam_id
        


    def _get_json(self, url, params = None):
        """Retrieves json from a particular url, and returns it as a json object."""
        if params is None:
            return json.load(self._open_url(url))
        else:
            return json.load(self._open_url(url % params))

    def _open_url(self, url):
        """
        Put here to make catching exceptions easier
        
        Sometimes Steam seems to throttle your requests if you're hitting them a bit hard.
        If you get an HTTPError from that, it will pause and retry a few times, which usually
        results in Steam letting your next requests go through. If it fails all the retries, it
        will just return None and continue on.

        TODO - better error logging for failed requests.

        """
        try:
            return urllib2.urlopen(url)
        except urllib2.URLError as e:
            #print 'URLError = ' + str(e.reason)
            return self._retry(url)
        except urllib2.HTTPError as e:
            print 'HTTPError = ' + str(e.code)
            return self._retry(url)
        except ValueError as e:
            print 'Not a proper URL'
        except:
            return self._retry(url)

    def _retry(self, url):
        """Retries your request n number of times"""
        
        for num in range(self.retries):
            print "{} is unreachable, retrying {} number of times".format(url, num + 1)
            try:
                return urllib2.urlopen(url)
            except:
                sleep(self.time)
        raise SteamError('Can\'t connect to Steam. Try again later.')
        

    def _date(self, date):
        return datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')