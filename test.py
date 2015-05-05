from CPB.cpb import *

'''
movie = Movie()

movies = movie.get_last()
sorted = movie.group(movies)
print sorted'''

cpb = CPB("http://www.cpasbien.pw/")
list_torrents = cpb.get_list_torrent(category=CATEGORIES.MOVIES, order=ORDERS.SEEDERS.DES, quality=QUALITY.ALL, limit=100)
for t in list_torrents:
    print t
'''
torrents = {}
for t in list_torrents:
    if t.name not in torrents:
        torrents[t.name] = {}
    if t.season not in torrents[t.name]:
        torrents[t.name][t.season] = {}
    if t.episode not in torrents[t.name][t.season]:
        torrents[t.name][t.season][t.episode] = {}
    if t.quality not in torrents[t.name][t.season][t.episode]:
        torrents[t.name][t.season][t.episode][t.quality] = {}
    torrents[t.name][t.season][t.episode][t.quality]["link"] = t.link
    torrents[t.name][t.season][t.episode][t.quality]["seeders"] = t.seeders
    torrents[t.name][t.season][t.episode][t.quality]["leechers"] = t.leechers
    torrents[t.name][t.season][t.episode][t.quality]["size"] = t.size
print torrents'''
    
        
