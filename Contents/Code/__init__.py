import commands
import os

VIDEO_PREFIX = "/video/veetle"

NAME = L('Veetle')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART  = 'art-default.jpg'
ICON = 'veetle.jpg'
VEETLE_JSON_URL= 'http://www.veetle.com/channel-listing-cross-site.js'
BASE_URL = 'http://127.0.0.1:'
####################################################################################################

def Start():
    ## make this plugin show up in the 'Video' section
    ## in Plex. The L() function pulls the string out of the strings
    ## file in the Contents/Strings/ folder in the bundle
    ## see also:
    ##  http://dev.plexapp.com/docs/mod_Plugin.html
    ##  http://dev.plexapp.com/docs/Bundle.html#the-strings-directory
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VeetleMainMenu, NAME, ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    ## set some defaults so that you don't have to
    ## pass these parameters to these object types
    ## every single time
    ## see also:
    ##  http://dev.plexapp.com/docs/Objects.html
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = "InfoList"
    MediaContainer.art = R(ART)
    DirectoryItem.thumb = R(ICON)
    VideoItem.thumb = R(ICON)
    HTTP.CacheTime = CACHE_1HOUR    
#### the rest of these are user created functions and
#### are not reserved by the plugin framework.
#### see: http://dev.plexapp.com/docs/Functions.html for
#### a list of reserved functions above
#### firefoxID=os.spawnl(os.P_NOWAIT, "/Applications/Firefox.app/Contents/MacOS/firefox-bin", "-url","http://www.veetle.com/index.php/channel/view#4c64632326c30")


#
# Example main menu referenced in the Start() method
# for the 'Video' prefix handler
#

def VeetleMainMenu():

    # Container acting sort of like a folder on
    # a file system containing other things like
    # "sub-folders", videos, music, etc
    # see:
    #  http://dev.plexapp.com/docs/Objects.html#MediaContainer
    dir = MediaContainer(viewGroup="InfoList")


    # see:
    #  http://dev.plexapp.com/docs/Objects.html#DirectoryItem
    #  http://dev.plexapp.com/docs/Objects.html#function-objects
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="All",
                thumb=R(ICON),
                art=R(ART)
            ), catID="All"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Movies",
                thumb=R(ICON),
                art=R(ART)
            ), catID="10"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="TV Shows",
                thumb=R(ICON),
                art=R(ART)
            ), catID="20"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="News",
                thumb=R(ICON),
                art=R(ART)
            ), catID="30"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Gaming",
                thumb=R(ICON),
                art=R(ART)
            ), catID="40"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Comedy",
                thumb=R(ICON),
                art=R(ART)
            ), catID="50"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Animation",
                thumb=R(ICON),
                art=R(ART)
            ), catID="60"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Music",
                thumb=R(ICON),
                art=R(ART)
            ), catID="70"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Sport",
                thumb=R(ICON),
                art=R(ART)
            ), catID="80"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Education",
                thumb=R(ICON),
                art=R(ART)
            ), catID="90"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Religion",
                thumb=R(ICON),
                art=R(ART)
            ), catID="100"
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                VeetleVideos,
                title="Events",
                thumb=R(ICON),
                art=R(ART)
            ), catID="110"
        )
    )
    # ... and then return the container
    dir.Sort("title")
    return dir
	    
def VeetleVideos(sender, catID):
	    VidCont= MediaContainer(title1=sender.title2)
	    portstring = commands.getoutput('lsof -i |grep firefox-b |grep "(LISTEN)" |awk \'{print $9}\'')
	    if len(portstring) ==0:
	    	return MessageContainer("Firefox not running", "This plugin requires a Veetle channel to be opened in Firefox in order to function. Please start Firefox, load and start a veetle video, then press the power button to stop the veetle video playing and return to Plex.")
	    else:
	    	splitportstring=(portstring.split(":"))
	    	port = splitportstring[1]
	    	dict = JSON.ObjectFromURL(VEETLE_JSON_URL)
	    	for item in dict:
	    		key = BASE_URL + port +'/' + item["chost"] + ',' + item["channelId"] 
	    		thumbs = item["logo"]
	    		thumb=thumbs["sm"]
	    		if catID=='All':
	    			VidCont.Append(VideoItem(title=item["title"], thumb=thumb, ratingKey=key, summary=item["description"], key=key))
	    		else:
	    			if item["categoryId"]==catID:
	    				VidCont.Append(VideoItem(title=item["title"], thumb=thumb, summary=item["description"], key=key))
	    	VidCont.Sort("title")
	    	return VidCont
