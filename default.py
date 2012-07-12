import re, sys
import urllib, urllib2
import xbmcgui, xbmcplugin, xbmcaddon
import showEpisode

addon = xbmcaddon.Addon(id='plugin.video.blisteredthumbs')

baseLink = "http://www.blisteredthumbs.net"

def mainPage():
    addDirectoryItem(addon.getLocalizedString(30000),{'action':"listLatest"})
    addDirectoryItem(addon.getLocalizedString(30001),{'action':"listShows"})
    addDirectoryItem(addon.getLocalizedString(30002),{'action':"listPlatforms"})

def listShows():
    addDirectoryItem('Substance TV',{'action':"listVideos",'link' : baseLink+"/show/show-substance-tv"},baseLink+"/show_images/thumbnails/1305265880-115x50.jpg")
    addDirectoryItem('Bennett The Sage',{'action':"listVideos",'link' : baseLink+"/show/show-bennett-the-sage"},baseLink+"/show_images/thumbnails/1287774048-115x50.jpg")
    addDirectoryItem('RinryGameGame',{'action':"listVideos",'link' : baseLink+"/show/show-rinrygamegame"},baseLink+"/show_images/thumbnails/1291931887-115x50.png")
    addDirectoryItem('MMO Grinder',{'action':"listVideos",'link' : baseLink+"/show/show-mmo-grinder"},baseLink+"/show_images/thumbnails/1321479436-115x50.jpg")
    addDirectoryItem('GameJams',{'action':"listVideos",'link' : baseLink+"/show/show-gamejams"},baseLink+"/show_images/thumbnails/1299312822-115x50.jpg")
    addDirectoryItem('Heart of Gaming',{'action':"listVideos",'link' : baseLink+"/show/show-heart-of-gaming"},baseLink+"/show_images/thumbnails/1299023028-115x50.jpg")
    addDirectoryItem('Ashens',{'action':"listVideos",'link' : baseLink+"/show/show-ashens"},baseLink+"/show_images/thumbnails/1303370810-115x50.png")
    addDirectoryItem('Benzaie',{'action':"listVideos",'link' : baseLink+"/show/show-benzaie"},baseLink+"/show_images/thumbnails/1287800440-115x50.jpg")
    addDirectoryItem('Lee/Dena Still Gaming',{'action':"listVideos",'link' : baseLink+"/show/show-leedena-still-gaming"},baseLink+"/show_images/thumbnails/1296447617-115x50.jpg")

def listPlatforms():
	addDirectoryItem('MMO',{'action':"listVideos",'link' : baseLink+"/category/mmo"},baseLink+"/wp-content/themes/BT2/images/mmo_nav.png")
	addDirectoryItem('Mobile',{'action':"listVideos",'link' : baseLink+"/category/mobile"},"")
	addDirectoryItem('Nintendo DS',{'action':"listVideos",'link' : baseLink+"/category/ds"},baseLink+"/wp-content/themes/BT2/images/ds_nav.png")
	addDirectoryItem('Nintendo Wii',{'action':"listVideos",'link' : baseLink+"/category/wii"},baseLink+"/wp-content/themes/BT2/images/wii_nav.png")
	addDirectoryItem('PC',{'action':"listVideos",'link' : baseLink+"/category/pc"},baseLink+"/wp-content/themes/BT2/images/pc_nav.png")
	addDirectoryItem('Playstation 3',{'action':"listVideos",'link' : baseLink+"/category/ps3"},baseLink+"/wp-content/themes/BT2/images/ps3_nav.png")
	addDirectoryItem('PSP',{'action':"listVideos",'link' : baseLink+"/category/psp"},baseLink+"/wp-content/themes/BT2/images/psp_nav.png")
	addDirectoryItem('Retro',{'action':"listVideos",'link' : baseLink+"/category/retro"},baseLink+"/wp-content/themes/BT2/images/retro_nav.png")
	addDirectoryItem('Xbox 360',{'action':"listVideos",'link' : baseLink+"/category/xbox"},baseLink+"/wp-content/themes/BT2/images/xb360_nav.png")	

def listLatest():
    link = loadPage(baseLink)
    _regex_extractLatest = re.compile("Recent Episodes</span><div ><div(.*?)</div></div></div></div><div",re.DOTALL)
    _regex_extractLatestEpisode = re.compile("src=\"([^\"]*?)\".*?alt=\"([^\"]*?)\".*?href=\"([^\"]*?)\"",re.DOTALL)

    latestDiv = _regex_extractLatest.search(link)
    if latestDiv is not None:
        for latestItem in _regex_extractLatestEpisode.finditer(latestDiv.group(1)):
            url = latestItem.group(3).strip()
            name = latestItem.group(2).strip()
            thumbnail = latestItem.group(1).strip()
            addDirectoryItem(name,{'action':"playEpisode",'link':url},thumbnail,False)

def listVideos(url):
	link = loadPage(url)
	
	_regex_extractEpisode = re.compile("<h1 class=\"post_title\">.*?href=\"(.*?)\".*?>(.*?)</a>.*?src=\"(.*?)\".*?<p>(.*?)</p>.*?class=\"keep-reading\"",re.DOTALL)
	_regex_extractNextPage = re.compile("href=\"(.*?)\" >KEEP READING &raquo;</a>")
    
	for videoItem in _regex_extractEpisode.finditer(link):
		name = videoItem.group(2).strip()
		url = videoItem.group(1)
		description = videoItem.group(4)
		thumbnail = videoItem.group(3)
		name = remove_html_special_chars(name)
		addDirectoryItem(name,{'action':"playEpisode",'link':url},thumbnail,False)
	
	nextPageItem = _regex_extractNextPage.search(link)
	if nextPageItem is not None:
		addDirectoryItem(addon.getLocalizedString(30004),{'action':"listVideos",'link' : nextPageItem.group(1)},"")

def playEpisode(url):
    episode_page = loadPage(url)
    showEpisode.showEpisode(episode_page)

def loadPage(url):
	print url
	try:
		resp = urllib2.urlopen(url)
		contents = resp.read()
	except urllib2.HTTPError, error:
		contents = error.read()
	return contents

def remove_html_special_chars(input):
    input = input.replace("&#8211;","-")
    input = input.replace("&#8217;","'")#\x92
    input = input.replace("&#039;",chr(39))# '
    input = input.replace("&#038;",chr(38))# &
    input = input.replace("&amp;",chr(38))# &
    input = input.replace(r"&quot;", "\"")
    input = input.replace(r"&apos;", "\'")
    input = input.replace(r"&#8216;", "\'")
    input = input.replace(r"&#8217;", "\'")
    input = input.replace(r"&#8230;", "...")
    return input

def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

def addDirectoryItem(name, parameters={}, pic="", folder=True):
    li = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=pic)
    if not folder:
        li.setProperty('IsPlayable', 'true')
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=folder)

if not sys.argv[2]:
    mainPage()
else:
    params=get_params()
    if params['action'] == "listShows":
        listShows()
    elif params['action'] == "listPlatforms":
        listPlatforms()
    elif params['action'] == "listLatest":
        listLatest()
    elif params['action'] == "listVideos":
        listVideos(urllib.unquote(params['link']))
    elif params['action'] == "playEpisode":
        playEpisode(urllib.unquote(params['link']))
    else:
        mainPage()

xbmcplugin.endOfDirectory(int(sys.argv[1]))