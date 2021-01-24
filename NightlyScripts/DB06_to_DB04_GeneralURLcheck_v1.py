import urllib2
import time

###############################################################time & log setup###########################################################################################
#Time##
timestream = time.strftime("%m%d%y")
propmonth = time.strftime('%B')
propday = time.strftime('%d')
propyear = time.strftime('%Y')
militaryhour = time.strftime('%H')
propminute = time.strftime('%M')
propsecond = time.strftime('%S')
dytextdate = propmonth + ' ' + propday + ', ' + propyear
HMStextdate = militaryhour + ':' + propminute + ' ' + propsecond + ' Seconds '
fulltime = 'Date: ' + dytextdate + ' Time: ' + HMStextdate
begin_time = time.time()

script_working = r'C:\Nightly Scripts\DB6_to_DB4_Log'
logtime = script_working + '\\DB06_to_DB04_v42' + timestream + '.txt'

#Start Log
track = open(logtime,"a") 
Header = 'Start DB06_to_DB04_v4 General URL check'
print('Start DB06_to_DB04_v4 General URL check' + fulltime + '\n')
track.write('\n' + '\n' + '\n' + '\n' + '\n' + Header + '\n' + fulltime + '\n')

############################################### URL list #####################################################################
urllist = ['http://www.google.com',
           'http://192.146.148.33/Freeance/Client/PublicAccess1/index.html?appconfig=PublicWeb',
           'https://maps.spartanburgcounty.org/arcgis/apps/webappviewer/index.html?id=6881d692298041bc91caeca0465f2efc',
           'https://maps.spartanburgcounty.org/arcgis/apps/webappviewer/index.html?id=02903b3fc2764fdc8016a03d3292167b',
           'https://www.greercpw.com/greer-water',
           'https://www.sjwd.com/',
           'https://wrwd.org//',
           'https://www.spartanburgwater.org/',
           'https://www.icwd.org/index.php',
           'http://www.metrobwater.com/home.html',
           'https://www.lcfwd.com/',
           'https://www.mrrwc.com/',
           'https://www.spartanburgcounty.org/161/Registrations-and-Elections',
           'https://websoilsurvey.sc.egov.usda.gov/App/HomePage.htm',
           'https://msc.fema.gov/portal/advanceSearch#searchresultsanchor',
           'https://www.fema.gov/flood-maps/tutorials',
           'https://www.cityofspartanburg.org/city-council/districts',
           'http://www.spart1.org/',
           'https://www.spart2.org/',
           'https://www.spartanburg3.org/',
           'https://www.spartanburg4.org/',
           'https://www.spart5.net/',
           'https://www.spart6.org/',
           'https://www.spartanburg7.org/',
           'http://www.tygerriver.org/tyger-10-park.php',
           'https://www.spartanburgconservation.org/cottonwood-trail',
           'https://www.spartanburgconservation.org/glendale-shoals-preserve',
           'https://www.sctrails.net/trails/trail/pacolet-river-heritage-preserve',
           'https://www.sctrails.net/trails/trail/peters-creek-heritage-preserve',
           'http://www.cityofchesnee.org/default.asp?sec_id=180007731',
           'https://www.townofcampobellosc.com/',
           'https://www.lymansc.gov/news_detail_T6_R43.php',
           'https://www.sctrails.net/trails/trail/milliken-arboretum',
           "https://www.uscupstate.edu/about-the-university/community/facilities-and-venues/susan-jacobs-arboretum/#:~:text=Susan%20Jacobs%20Arboretum,University's%20328%2Dacre%20master%20plan.",
           'https://www.sctrails.net/trails/trail/boiling-springs-community-park',
           'https://www.wofford.edu/',
           'https://www.active-living.org/',
           'https://www.facebook.com/SpartanburgParks/?hc_ref=ARRoEPTNnOziiXjOEOCfH7kANTFjv0o_b7hq2gNy_Pd15FabRzODbCb8T7cAyJKf_SI&amp;ref=nf_target&amp;__tn__=kC-R',
           'https://www.sctrails.net/trails/search-results?q=&f%5Bcounties%5D=43',
           'https://www.cityofspartanburg.org/parks-and-recreation/reserve-a-space',
           'https://townofduncansc.com/stone-ledge-park-shelter-rentals/',
           'https://secure.rec1.com/SC/spartanburg-county-parks-dept/catalog',
           'https://reserve.southcarolinaparks.com/croft',
           'http://www.infodepot.org/',
           'http://www.cityofgreer.org/404/Facility-Rentals',
           'https://www.spartanburgconservation.org/cottonwood-trail',
           'https://www.spartanburgconservation.org/glendale-shoals-preserve',
           'https://www.lymansc.gov/news_detail_T6_R43.php',
           'https://www.spartanburgwater.org/Bowen-directions-contact',
           'https://www.sjwd.com/recreation/about-our-lakes/',
           'https://www.shipwreckcovewaterpark.com/admission.php#park_hours',
           'https://www.hatchergarden.org/plan-your-visit',
           'https://www.cityofspartanburg.org/parks-and-recreation/skate-park',
           'https://www.cityofspartanburg.org/parks-and-recreation/parks',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/DocumentCenter/View/128/Park-Hours-PDF?bidId=',
           'https://southcarolinaparks.com/croft',
           'http://www.cityofgreer.org/168/Parks-Facilities',
           'http://www.infodepot.org/Using-the-Library',
           'https://www.shipwreckcovewaterpark.com/rules.php',
           'https://www.spartanburgwater.org/Blalock-policies-guidance',
           'https://www.spartanburgwater.org/bowen-permits',
           'http://spartanburgparks.org/facilities/facility/details/cowpensveteransmemorialpark-50',
           'https://www.hatchergarden.org/',
           'https://southcarolinaparks.com/croft',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Willow-Oaks-Park-104',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Wards-Creek-Park-103',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Victor-Heights-Neighborhood-Park-101',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/VaDuMar-McMillan-Park-187',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Tyger-10-Nature-Park-98',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Susan-Jacobs-Arboretum-at-USC-Upstate-97',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Summer-Hill-Park-96',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Stoneledge-Park-95',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Stewart-Park-185',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Stevens-Ball-Field-94',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/St-Matthews-Park-161',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Shipwreck-Cove-Water-Park-93',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Sealy-Park-92',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Roger-Milliken-Arboretum-at-Wofford-Coll-80',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Richardson-Park-90',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Rail-Trail-Dog-Park-88',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Priscilla-Rumley-Park-86',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Peters-Creek-Heritage-Preserve-85',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Pacolet-River-Heritage-Preserve-83',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Pacolet-Park-82',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Old-Canaan-Park-184',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/North-Spartanburg-Park-183',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Milliken-Campus-Arboretum-182',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Mabry-Park-68',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Lyman-Park-77',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Little-Africa-Park-76',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Linville-Hills-Park-75',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Leroy-Mathis-Park-74',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Lake-Lyman-Park-and-Lodge-73',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Lake-Blalock-Park-71',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Inman-Mills-Park-67',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Hub-City-Art-Park-66',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Holston-Creek-Park-180',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Greer-Veterans-Park-59',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Greentown-Park-58',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Gordon-Henry-Park-49',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Glenn-Greenway-57',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Glendale-Shoals-Preserve-56',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Gib-Gosnel-Park-55',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/FairmontLarkin-Park-54',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Edwin-M-Griffin-Nature-Preserve-Home-of--52',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Downtown-Pocket-Park-51',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Downtown-Library-Park-Inside-Spartanburg-63',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Clifton-Park-Beach-46',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Chesnee-Park-43',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/CADA-Park-40',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/BP-Edwards-Park-37',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Boiling-Springs-Community-Park-Old-39',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Boiling-Springs-Community-Park-New-163',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Berry-Field-166',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Beech-Springs-Tennis-Complex-36',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Barnet-Park-165',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Arkwright-Park-35',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Anchor-Park-34',
           'https://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/295-Park-164',
           'http://spartanburgparks.org/facilities/facility/details/wrmckinneypark-105',
           'http://spartanburgparks.org/facilities/facility/details/uscupstatesoccercomplex-100',
           'http://spartanburgparks.org/facilities/facility/details/southconversestreetpark-91',
           'http://spartanburgparks.org/facilities/facility/details/northwestcommunitycenter-112',
           'http://spartanburgparks.org/facilities/facility/details/middletygercommunitycenter-115',
           'http://spartanburgparks.org/facilities/facility/details/maryhwrightgreenway-121',
           'http://spartanburgparks.org/facilities/facility/details/irwinpark-69',
           'http://spartanburgparks.org/facilities/facility/details/hillcrestpark-64',
           'http://spartanburgparks.org/facilities/facility/details/happyhollowpark-61',
           'http://spartanburgparks.org/facilities/facility/details/fairgroundsbasketballcourts-53',
           'http://spartanburgparks.org/facilities/facility/details/duncanpark-178',
           'http://spartanburgparks.org/facilities/facility/details/cowpensveteransmemorialpark-50',
           'http://spartanburgparks.org/facilities/facility/details/cliffdaleballfield-45',
           'http://spartanburgparks.org/facilities/facility/details/chapelstreetpark-42',
           'http://spartanburgparks.org/facilities/facility/details/ccwoodsoncommunitycenter-107',
           'http://spartanburgparks.org/facilities/facility/details/cannonsballfield-41',
           'http://spartanburgparks.org/facilities/facility/details/brookwoodpark-38',
           'http://spartanburgparks.org/facilities/facility/details/andrewsfarmpark-33',
           'http://spartanburgparks.org/facilities/facility/details/adamspark-32',
           'http://spartanburgparks.org/343/Tyger-River-Park',
           'http://spartanburgparks.org/308/Lake-Cooley-Outdoor-Education-Center',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Woodruff-Leisure-Center-109',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/TW-Edwards-Center-108',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Timken-Community-Center-111',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Inman-Recreation-Center-157',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Cleveland-Park-169',
           'http://sc-spartanburgcountyparksandrec.civicplus.com/Facilities/Facility/Details/Chesnee-Community-Center-110',
           'http://hotspotskatepark.com/',         
           'http://www.townofcampobello.com/']
###################################################################################################################################


#Test broken URLs (townofduncan site crashes script, I'm not sure how to fix this)
#'https://www.townofduncan.sc.gov/'
#'http://www.townofcampobello.com/',



hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


for url in urllist:
    try:
        polite = urllib2.Request(url, headers=hdr)
        quote = urllib2.urlopen(polite)
        the_page = quote.read()
        print(url + ' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ GOOD ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
        track.write(url + ' ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ GOOD ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^' + '\n'+ '\n')
    except ValueError, ex:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ' + url + ' value error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        track.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ' + url + ' value error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' + '\n'+ '\n')
    except urllib2.URLError as e:
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ' + url + ' URL error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        track.write('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  ' + url + ' URL error !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(e.reason)
        track.write(str(e.reason))
        track.write('\n' + '\n')
        if e.reason == 'Forbidden':
            print('\n' + '\n' + 'but seems to be there so cool' + '\n' + '\n')
            track.write('\n' + '\n' + 'but seems to be there so cool' + '\n' + '\n')

#####Cleanup##########################################################################################################################################################################################################
track.write('\n' + '\n' + 'TokenGeneralURLcheck' + '\n' + '\n')    
track.write('\n' + '\n' + 'DB06_to_DB04_v4, General URL check completed %s total seconds' % (round((time.time() - begin_time)/60,2))
    + '\n' + '\n' + fulltime)
track.close()
print('%s total seconds' % (round((time.time() - begin_time)/60,2)))
print('DB06_to_DB04_v4, General URL check completed')
#Written by Michael Shoop 
#Version #4 completed 08/21/20 #DB06_to_DB04_GeneralURLcheck

