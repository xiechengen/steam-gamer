#! usr/bin/env python
#coding=utf-8
import requests, csv
from bs4 import BeautifulSoup

# for test using csv file as data storage temporarily
target_url = "http://store.steampowered.com/search/?tags=599&page=1#sort_by=_ASC&page=1"

class WrongURL(Exception):
    def __str__(self):
        return "Invalid url input, input should be valid url of game index."

def Initialization():
    """
    This function asks user to input the needed initialization informations 
    of the scraping mission.
    'filename' can be replaced by db later...
    """
    url = pagenum = filename = None
    while True:
        if not url:
            try:
                url = target_url
            except WrongURL as wurl:
                print(wurl)
                url = None
                continue
        if not pagenum:
            try:
                pagenum = int(input('Please enter the page numbers you want'
                                ' to scrape:'))
                # here to be changed to monitor the total page number by a function
            except ValueError:
                print('Please enter an integer!')
                pagenum = None
                continue
        if not filename:
            try:
                filename = input('Please enter the file name to save data'
                         '(file name must include postfix ".csv"):')
                if filename[-4:] != '.csv':
                    raise CSVfileNameError
            except CSVfileNameError as cfne:
                print(cfne)
                filename = None
                continue
        if url and pagenum and filename:
            break
    return (url, pagenum, filename)     