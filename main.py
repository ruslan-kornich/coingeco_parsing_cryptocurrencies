import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('coingeco.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['symbol'],
                         data['price'],
                         data['url']])


def refined(s):
    r = s.split(' ')[0]
    return r.replace(',', '').replace('$', '')


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_="sort table mb-0 text-sm text-lg-normal table-scrollable").find('tbody').find_all(
        'tr')
    for tr in trs:
        tds = tr.find_all('td')

        try:
            name = tds[2].find('a').find('span').text
        except:
            name = ""
        try:
            symbol = tds[2].find('span', class_="d-lg-inline font-normal text-3xs tw-ml-0 md:tw-ml-2 "
                                                "md:tw-self-center tw-text-gray-500").text
        except:
            symbol = ""
        try:
            url = 'https://www.coingecko.com' + tds[2].find('a').get('href')
        except:
            url = ""
        try:
            pr = tds[4].find('span').text
        except:
            pr = ''
        try:
            price = refined(pr)
        except:
            price = ""

        data = {'name': name.strip(),
                'symbol': symbol.strip(),
                'url': url.strip(),
                'price': price.strip()}
        write_csv(data)


def main():
    pattern = 'https://www.coingecko.com/ru?page={}'
    for i in range(1, 130):
        url = pattern.format(str(i))
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()
