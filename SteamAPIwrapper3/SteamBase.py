import json
import datetime
import requests
from time import sleep

class SteamError(Exception):
    def __str__(self):
        return 'Unable to connect to Steam. Try again later.'
    
class SteamAPI:
    '''Base class for steam API classes'''
    def __init__(self, steam_id, api_key, time, retries):
        '''Sets the steam id for the user in question and you API key.'''
        self.api_key = api_key
        self.steam_id = steam_id
        self.time = time
        self.retries = retries

    def __get_json(self, url, params = None):
        '''Retrieves json from a particular url, return as json obj.'''
        if not params:
            return json.load(self.__open_url(url))
        else:
            return json.load(self.__open_url(url % params))

    def __open_url(self, url):
        '''
        This function is rewritten with requests, replacing the orignal urllib2
        model. Original function documentation is as below:
        
        Put here to make catching exceptions easier
        
        Sometimes Steam seems to throttle your requests if you're hitting them
        a bit hard.
        If you get an HTTPError from that, it will pause and retry a few times,
        which usually results in Steam letting your next requests go through.
        If it fails all the retries, it will just return None and continue on.

        TODO - better error logging for failed requests.
        '''
        try:
            return requests.get(url)
        except requests.URLRequired as e:
            print('URLRequired =', e)
        except requests.HTTPError as e:
            print('HTTPError =', e)
            return self.__retry(self, url, self.time, self.retries)
        except requests.exceptions.MissingSchema:
            print('Not a proper URL')
        except Exception as e:
            print(e)
            return self.__retry(self, url, self.time, self.retries)

    def __retry(self, url):
        '''Retries your request n times'''
        print('Problem occured during request for %s, retrying %d number of\
               times' % (url, self.retries))
        for i in range(self.retries):
            try:
                return requests.get(url)
            except:
                sleep(self.time)
        raise SteamError

    def __date(self, date):
        '''Purpose unclear, left undone for now. Original code below:'''
        return datetime.datetime.fromtimestamp(int(date)).strftime('%Y-%m-%d %H:%M:%S')
