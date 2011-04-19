import commands

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
                VeetleVideos("All","All"),
                "All",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                MovieVeetleVideos,
                "Movies",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                TVVeetleVideos,
                "TV Shows",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                NewsVeetleVideos,
                "News",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                GamingVeetleVideos,
                "Gaming",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                ComedyVeetleVideos,
                "Comedy",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                AnimationVeetleVideos,
                "Animation",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                MusicVeetleVideos,
                "Music",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                SportVeetleVideos,
                "Sport",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                EducationVeetleVideos,
                "Education",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                ReligionVeetleVideos,
                "Religion",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    dir.Append(
        Function(
            DirectoryItem(
                EventsVeetleVideos,
                "Events",
                thumb=R(ICON),
                art=R(ART)
            )
        )
    )
    # ... and then return the container
    dir.Sort("title")
    return dir
	    
def VeetleVideos(sender, title, catID):
	    VidCont= MediaContainer(title1=title)
	    portstring = commands.getoutput('lsof -i |grep firefox-b |grep "(LISTEN)" |awk \'{print $9}\'')
	    splitportstring=(portstring.split(":"))
	    port = splitportstring[1]
	    dict = JSON.ObjectFromURL(VEETLE_JSON_URL)
	    for item in dict:
	    	key = BASE_URL + port +'/' + item["chost"] + ',' + item["channelId"] 
	    	thumbs = item["logo"]
	    	thumb=thumbs["sm"]
	    	if catID=='All':
	    		allVidCont.Append(VideoItem(title=item["title"], thumb=thumb, ratingKey=key, summary=item["description"], key=key))
	    	else
	    		if item["categoryId"]==catID:
	    			allVidCont.Append(VideoItem(title=item["title"], thumb=thumb, summary=item["description"], key=key))
	    VidCont.Sort("title")
	    return allVidCont
