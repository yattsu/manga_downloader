from inc.model import scrap
from inc.model import download
import os
import time

def get_choice():
  os.system('clear')
  prompt = '>> Name of the manga: '
  choice = None

  while choice is None:
    choice = input(prompt)
    if not choice.strip():
      choice = None

  return choice
  
def main(msg = False):
  choice = get_choice()
  scraper = scrap.Scrap(choice)
  results = scraper.clean_results()
  if results is False:
    print('   [X] Manga not found...')
    time.sleep(2)
    main()
    return

  for result in results:
    print('-- [{}] {}'.format(results.index(result) + 1, result['name']))
    if len(result['alt_names']) > 0 and ''.join(result['alt_names']).strip() != '':
      print('   Other names: {}'.format(', '.join(result['alt_names'])))
    print('\n')

  print('   [{} results found]'.format(len(results)))
  prompt = '\n>> Enter the number of the manga you want to download: '
  choice = int(input(prompt).strip())
  while choice == '' or int(choice) > len(results) or int(choice) < 1:
    choice = int(input(prompt))

  choice = results[choice - 1]

  #manga = {'link': '//www.mangahere.cc/manga/akaku_saku_koe/', 'name': 'Akaku Saku Koe', 'alt_names': ['あかく咲く声', '붉게 피는 소리', 'Hana Dorobou (The  ... oice That Blooms Red']}
  downloader = download.Download(choice)
  downloader.download()

if __name__ == '__main__':
  main()