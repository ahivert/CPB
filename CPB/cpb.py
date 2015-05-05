# -*- coding: utf8 -*-

from lxml import html
import requests
import math


class Torrent(object): 
    name = None
    link = None
    seeders = 0
    leechers = 0
    size = 0
    season = 0
    episode = 0
    category = None
    


    def __init__(self, name, link, seeders, leechers, size, quality, category, season=0, episode=0):
        self.name = name
        self.link = link
        self.seeders = seeders
        self.leechers = leechers
        self.size = size
        self.season = season
        self.episode = episode
        self.quality = quality
        self.category = category        
    
    def __str__(self, *args, **kwargs):
        return self.name.encode("utf-8")

        
class CPB(object):

    url = None
    max_per_page = 30
    url_cat = "view_cat.php?categorie="
    url_search = "recherche/"
    
    def __init__(self, url):
        self.url = url

    
    def _get_html(self, url, page=0):
        if '?' in url:
            url += "&page=" + str(page)
        else:
            url += "/page-" + str(page)
        req = requests.get(self.url+url)
        return html.fromstring(req.text)
    
    
    def get_list_torrent(self, category, order, quality, limit=0):
        url = "view_cat.php?categorie=" + category + "&trie=" + order        
        return self._get_rows(limit=limit, url=url, list_quality=quality, category=category)
    
            
    def search(self, url, quality, query):        
        url_search = url + query 
        return self._get_rows(url_search, quality)
    
    
    def _get_torrent_link(self, url):
        filename =  url.split('/').pop()[:-5]
        return self.url + 'telechargement/' + filename + '.torrent'
    
    
    def _get_max_page(self, html):
        return int(html.xpath('//div[@id="pagination"]/a[strong]')[0].getprevious().xpath(".//text()")[0])
    
    def _get_last_index_title(self, tab_title):
        for index, w in enumerate(tab_title):
            if w.isupper() and index>0 :
                return index
                
    
    def _get_name(self, tab_title):        
        last_index_title = self._get_last_index_title(tab_title)        
        return ' '.join(tab_title[:last_index_title])
    
    
    def _get_quality(self, tab_title, quality):
        for index, w in enumerate(tab_title):
            if w.upper() in quality:
                index_quality = index
                break
        
        return tab_title[index_quality]
    
    
    def _get_season_episode(self, tab_title):
        title_last_idx = self._get_last_index_title(tab_title)          
        while tab_title[title_last_idx][0].upper() != 'S' or tab_title[title_last_idx][3].upper() != 'E':
            title_last_idx +=1
       
        
        season = int(tab_title[title_last_idx][1:3])
        episode = int(tab_title[title_last_idx][4:6])
        
        return season, episode
        
    def _get_rows(self, limit, url, list_quality, category):
        torrents = []
        html = self._get_html(url)
        
        max_page = self._get_max_page(html)
        
        if limit == 0: # Get all torrents
            nb_page=max_page
        else:
            nb_page = int(math.ceil(float(limit) / self.max_per_page)) # Theoritical value need to reevaluate if quality not good
            
        for page in range(nb_page):
            list_torrents = html.xpath('//div[@class="ligne0" or @class="ligne1"]')
            for line in list_torrents:
                title = (line.xpath('a/text()'))[0]
                # check if quality is correct
                quality_ok = False
                for q in list_quality:
                    if q in title.upper():
                        quality_ok = True
                        break
               
                        
                if quality_ok :
                    tab_title = title.split(' ')                    
                    link = self._get_torrent_link(line.xpath('a/@href')[0])
                    size = line.xpath('div[@class="poid"]/text()')[0].replace(u'\xa0','')
                    seeders = line.xpath('div[@class="up"]/span[@class="seed_ok" or @class="seed_nok"]/text()')[0]
                    leechers = line.xpath('div[@class="down"]/text()')[0]                    
                    name = self._get_name(tab_title)
                    quality = self._get_quality(tab_title, list_quality)
                    
                    if category == CATEGORIES.SHOWS:
                        try:
                            season, episode = self._get_season_episode(tab_title)
                        except:
                            pass
                    else:
                        season = None
                        episode = None
                    
                    torrent = Torrent(name=name, 
                                      link=link, 
                                      seeders=seeders, 
                                      leechers=leechers, 
                                      size=size, 
                                      quality=quality, 
                                      category=category, 
                                      season=season, 
                                      episode=episode)
                    torrents.append(torrent)
                    
                    limit -= 1
               
                if nb_page != max_page and limit == 0:
                    break
                
            html = self._get_html(url, page)
        return torrents
                        

     
            

class CATEGORIES():
    MOVIES = "films"
    SHOWS = "series"
    MUSIC = "musique"
    EBOOK = "ebook"
    SOFTWARE = "logiciels"
    PC_GAME = "jeux-pc"
    CONSOLE_GAME = "jeux-consoles"
    

class QUALITY():
    ALL = ['DVDSCR','DVDRIP', 'HDTV', '720P', '1080P',
            'WEBRIP']
    GOOD = [
            'DVDRIP', 'HDTV', '720P', '1080P',
            'WEBRIP'
            ]
    BEST = ['HDTV', '720P', '1080P']

class ORDERS():
    class SEEDERS():
        DES = "seeds-d"
        ASC = "seeds-a"  
    class LEECHERS():
        DES = "leechs-d"
        ASC = "leechs-a"
    class DATE():
        DES = "date-d"
        ASC = "date-a"
    class NAME():
        DES = "nom-d"
        ASC = "nom-a"
    class SIZE():
        DES = "poid-d"
        ASC = "poid-a"        
