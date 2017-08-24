from steamapiwrapper3.SteamGames import *
from steamapiwrapper3.Users import SteamUser
import urllib.request, urllib.error, urllib.parse
import json
import csv
import time

def process(rigion="CN"):
    """
    This function is the main process of getting name and price of
    games on given area of steam.
    """
    stamp = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    file = open('outputs\\run%s.csv' % stamp, 'w', newline='', encoding='utf8')
    writer = csv.writer(file)
    games = Games()
    getall = games.get_all(rigion)
    counter = 1
    for item in getall:
        try:
            print("#%d" % counter, " ", item.appid, item.name, item.final)
            writer.writerow([item.appid, item.name, item.final])
        except UnicodeEncodeError as error:
            print(error)
            continue
        except Exception as e:
            print(e)
        '''
        if counter >= 10:
            print("Experiment end")
            break
        '''
        counter += 1
    file.close()

def new_processor(rigion="CN"):
    '''
    doc string empty for now
    '''
    return 0

if __name__ == '__main__':

    start = time.clock()
    end = None
    try:
        process()
    except Exception as e:
        print('Unexcpected error occured, mission abort.')
        print(e)
        end = time.clock()
    finally:
        if not end:
            end = time.clock()
        timeConsumed = end - start
    m , s = divmod(timeConsumed, 60)
    h , m = divmod(m, 60)
    print ("It takes %d hours %d minutes %.2f seconds." % (h, m, s))
