#! python3
import requests, csv
from bs4 import BeautifulSoup

# for test using csv file as data storage temporarily
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

def StartOperation(init_url:str, pages:int, filename:str)->None:
    '''
    type init_url: str
    rtype: None
    '''
    num = 0
    error_counter = 0
    perpage = 25
    failure_urls = []
    file = open(r'C:\Users\spencer\Desktop\%s' % filename,
                'w', newline='',
                encoding='utf8')
    writer = csv.writer(file)
    for i in range(1,pages):
        url = init_url + str(i)
        # print(url)
        res = requests.get(url)
        try:
            res.raise_for_status()
        except Exception as e:
            print('There is a problem:', e)
        # There should be four fields for now: names, prices, discounts
        soup = BeautifulSoup(res.text, 'lxml')
        names = soup.select('a > div[class="responsive_search_name_combined"] >\
                             div > span[class="title"]')
        
        dis_and_prices = soup.select('a > div > div > div') # can it be seperated by bs4?
        # manual seperation of discount and price below:
        discounts, prices = [], []
        for k in range(len(dis_and_prices)):
            if k % 2 == 0:
                discounts.append(dis_and_prices[k])
            else:
                prices.append(dis_and_prices[k])
        counter = 0
        for j in range(len(names)):            
            try:
                writer.writerow([names[j].getText(),
                                 prices[j].getText().strip(),
                                 discounts[j].getText().strip()])
                print('#%5d' % (25*(i-1) + j), names[j].getText(), prices[j].getText().strip(),
                                 discounts[j].getText().strip())
            except Exception as e:
                print('Error occured on page %d line %d' % (i+1, j+1))
                print('error message:', e)
                if url not in failure_urls:
                        failure_urls.append(url)
                error_counter += 1
    file.close()
    if error_counter:
        print('\nTotal failed item number: %d items!' % error_counter)
    return failure_urls

if __name__ == '__main__':

    # The following is for development test:
    target_url = "http://store.steampowered.com/search/?page="
    pgm = 635
    fln = "dev_test_file.csv"
    # url, pgm, fln = Initialization()
    failures = StartOperation(target_url, pgm, fln)
    if failures:
        print('[The urls below occured problem]:')
        for item in failures:
            print(item)
    else:
        print('All pages successfully scraped!')
