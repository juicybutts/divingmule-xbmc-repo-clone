import urllib,urllib2,re,os
import xbmcplugin,xbmcgui,xbmcaddon
from BeautifulSoup import BeautifulSoup
try:
    import json
except:
    import simplejson as json

__settings__ = xbmcaddon.Addon(id='plugin.video.weather.channel')
__language__ = __settings__.getLocalizedString
home = __settings__.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

def Categories():
        addPlaylist('Play Top Stories','',3,icon)
        addDir('News','news',1,icon)
        addDir('Most Popular','popular',1,icon)
        addDir('Forecasts','forcast',1,icon)
        addDir('On TV','tv',1,icon)
        addDir('Living','living',1,icon)
        addDir('Storms','storms',1,icon)

        
def getSubcate(url):
        base_url = 'http://www.weather.com/weather/videos/news-41/top-stories-169/-/'
        req = urllib2.Request(base_url)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        soup = BeautifulSoup(link)
        if url == 'news':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[0]('li')
        elif url == 'popular':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[1]('li')
        elif url == 'forcast':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[2]('li')
        elif url == 'tv':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[3]('li')
        elif url == 'living':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[4]('li')
        elif url == 'storms':
                items = soup.find('div', attrs={'class' : "videoCollectionContent"})('ul')[5]('li')
        for item in items:
                name = name = item('a')[0].string
                url = item('a')[0]['href'].split('-')[-2].split('/')[0]
                addDir(name,url,2,icon)


def INDEX(url):
        url='http://wxdata.weather.com/wxdata/video/get.js?fn=getVideoCollection&cb=YAHOO.bcps.VideoService._handlePlaylistResponse&subcatid='+url+'&key=e88ca396-a740-102c-bafd-001321203584'
        req = urllib2.Request(url)
        req.addheaders = [('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        newStr = link[48:-1]
        data = json.loads(newStr)
        videos = data['clips']
        for video in videos:
            name = video['title']
            #videoId = video['bcVideoId']
            thumb = video['largethumb']
            desc = video['description']
            url = 'http://v.imwx.com/v/wxcom/'+video['sr56']+'.mov'
            addLink(name,url,desc,thumb)

            
def playLatest():
        url = 'http://wxdata.weather.com/wxdata/video/get.js?fn=getVideoCollection&cb=YAHOO.bcps.VideoService._handlePlaylistResponse&subcatid=169&key=e88ca396-a740-102c-bafd-001321203584'
        req = urllib2.Request(url)
        req.addheaders = [('Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.3) Gecko/20100401 Firefox/3.6.3 ( .NET CLR 3.5.30729)')]
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        newStr = link[48:-1]
        data = json.loads(newStr)
        videos = data['clips']
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for video in videos:
            name = video['title']
            #videoId = video['bcVideoId']
            thumb = video['largethumb']
            desc = video['description']
            url = 'http://v.imwx.com/v/wxcom/'+video['sr56']+'.mov'
            info = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=thumb)
            playlist.add(url, info)
        play=xbmc.Player().play(playlist)
                
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param


def addLink(name,url,description,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot":description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok
        
        
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

        
def addPlaylist(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok


params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None:
    print ""
    Categories()

elif mode==1:
    print ""+url
    getSubcate(url)
        
elif mode==2:
    print ""+url
    INDEX(url)

elif mode==3:
    print ""
    playLatest()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
