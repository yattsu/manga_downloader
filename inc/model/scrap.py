import requests
from bs4 import BeautifulSoup as bs
from .. import config

class Scrap:
  def __init__(self, query):
    self.CONFIG = config
    self.source = self.CONFIG.source
    self.query = query

  def make_soup(self):
    query = self.query.replace(' ', '+')
    source = self.source + '/search.php?name=' + query
    r = requests.get(source)

    status_code = r.status_code
    if status_code != 200:
      return False

    page_source = r.text
    soup = bs(page_source, 'lxml')

    return soup

  def get_results(self):
    soup = self.make_soup()

    try:
      soup = soup.find('div', {'class': 'result_search'})
      if 'no manga series' in soup.get_text().lower():
        return False

      dls = soup.find_all('dl')
    except AttributeError:
      return False

    return dls

  def clean_results(self):
    dls = self.get_results()
    if dls is False:
      return False

    results = []
    for dl in dls:
      a = dl.find('a', {'class': 'name_one'})
      href = a['href']
      name = a.string

      dd = dl.find('dd')
      alt_names = []
      for alt in dd.string.split(':')[1].split(';'):
        alt_names.append(alt.strip())

      properties = {'link': href, 'name': name, 'alt_names': alt_names}
      results.append(properties)

    return results
