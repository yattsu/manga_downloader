import requests
from bs4 import BeautifulSoup as bs
from .. import config
import os

class Download:
  def __init__(self, manga):
    self.CONFIG = config
    self.manga = manga

  def make_request(self, link):
    r = requests.get(link)
    status_code = r.status_code
    if status_code != 200:
      return False

    page_source = r.text

    return page_source

  def get_chapters(self):
    link = 'http:' + self.manga['link']

    page_source = self.make_request(link)
    if not page_source:
      return False

    soup = bs(page_source, 'lxml')

    try:
      detail_list = soup.find('div', {'class': 'detail_list'})
      chapter_list = detail_list.find('ul')
    except AttributeError:
      print('   [X] An error has occured...')
      return False

    clean_chapters = []
    for li in reversed(chapter_list.find_all('li')):
      span = li.find('span', {'class': 'left'})
      a = span.find('a')
      href = a['href']
      title = a.string.strip()

      properties = {'href': href, 'title': title}
      clean_chapters.append(properties)

    return clean_chapters

  def download(self):
    chapters = self.get_chapters()
    if chapters is False:
      return False

    manga = self.manga
    path = self.CONFIG.path + manga['name'] + '/'

    if os.path.exists(path):
      print('   [X] It seems like you already have a directory with the same exact name...')
      return False

    chapter_counter = 0
    for chapter in chapters:
      chapter_path = path + chapter['title'] + '/'
      if not os.path.exists(chapter_path):
        os.makedirs(chapter_path)

      link = 'http:' + chapter['href']
      page_source = self.make_request(link)
      if not page_source:
        print('   [X] Skipping chapter #' + str(chapter_counter))
        chapter_counter += 1
        continue

      soup = bs(page_source, 'lxml')

      select = soup.find('select', {'class': 'wid60'})
      
      try:
        options = select.find_all('option')
      except AttributeError:
        print('   [X] An error has occured...')
        print('   [X] Skipping chapter #' + str(chapter_counter))
        chapter_counter += 1
        continue

      chapter_counter += 1
      print('-- Downloading chapter ' + str(chapter_counter) + '...')

      for option in options:
        image_path = chapter_path + option.string + '.png'
        link = 'http:' + option['value']
        page_source = self.make_request(link)
        if not page_source:
          print('   [X] Skipping image #' + option.string)
          continue

        soup = bs(page_source, 'lxml')
        image = soup.find('img', {'id': 'image'})
        if image is None:
          print('   [X] Skipping image #' + option.string)
          continue
        image_link = image['src']
        r = requests.get(image_link)
        status_code = r.status_code
        if status_code != 200:
          print('   [X] Skipping image #' + option.string)
          continue

        with open(image_path, 'wb') as f:
          f.write(r.content)
