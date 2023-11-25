import requests
import json

line = "https://marian.mach.website.tuke.sk/"
#line = "https://telekom.sk/"
x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}'
print(f'Requesting {x}...')

r = requests.get(x)
final = r.json()
#print(final["loadingExperience"]["metrics"])
if "loadingExperience" in final:
    if "metrics" in final["loadingExperience"]:
        print("USER DATA:")
        fcp = final["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"] #into seconds (/1000)
        fid = final["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"] #into seconds (/1000)
        lcp = final["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
        cls = final["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100

        fcp_score = final["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["category"]
        fid_score = final["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["category"]
        lcp_score = final["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["category"]
        cls_score = final["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["category"]

        print("FCP: " + str(fcp) + " Category:" + str(fcp_score))
        print("FID: " + str(fid) + " Category:" + str(fid_score))
        print("LCP: " + str(lcp) + " Category:" + str(lcp_score))
        print("CLS: " + str(cls) + " Category:" + str(cls_score))

overall_score = final["lighthouseResult"]["categories"]["performance"]["score"] * 100

print("OVERALL SCORE: " + str(overall_score))


total_tasks = final["lighthouseResult"]["audits"]["diagnostics"]["details"]["items"][0]["numTasks"]
total_tasks_time = final["lighthouseResult"]["audits"]["diagnostics"]["details"]["items"][0]["totalTaskTime"]

print("Long tasks number: " + str(total_tasks))
print("Long task time (in ms): " + str(total_tasks_time))

print("Audit data:")

#NETWORK REQUESTS
num_requests = len(final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"])
print("Number of network requests: " + str(num_requests))

listrequests = []
for x in range (num_requests):
    endtime = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["networkEndTime"]
    starttime = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["networkRequestTime"]
    transfersize = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["transferSize"]
    resourcesize = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["resourceSize"]
    url = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["url"]
    list1 = [endtime, starttime, transfersize, resourcesize, url]
    listrequests.append(list1)
print("All of them stored in listrequests list!")
print("Example request:")
print(listrequests[0])

#MAINTHREAD WORK

mainthread_score = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["score"]
mainthread_duration = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["displayValue"]
print("Main thread score: " + str(mainthread_score))
print("Main thread duration: " + str(mainthread_duration))

listprocesses = []
for x in range (len(final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"])):
    duration = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"][x]["duration"]
    process = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"][x]["groupLabel"]
    list1 = [duration,process]
    listprocesses.append(list1)
print("ALL in listprocesses")
print("Example:")
print(listprocesses[0])

#EVENT LISTENERS
event_listeners_score = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["score"]

print("Event listeners score: " + str(event_listeners_score))
listevents = []
for x in range (len(final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"][x]["url"]
    line = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"][x]["label"]
    list1 = [url, line]
    listevents.append(list1)
print("ALL in listevents")
print("Example:")
if listevents != []:
    print(listevents[0])
else:
    print("No entries!")

#DOM SIZE

dom_size_score = final["lighthouseResult"]["audits"]["dom-size"]["score"]
dom_size_elements = final["lighthouseResult"]["audits"]["dom-size"]["displayValue"]

print("DOM size (sum of all tags in HTML) score: " + str(dom_size_score))
print("DOM elements: " + str(dom_size_elements))

#Offscreen images

offscreen_images_score = final["lighthouseResult"]["audits"]["offscreen-images"]["score"]
offscreen_images_val = len(final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"])


print("Offscreen images score: " + str(offscreen_images_score))
print("Offscreen images elements: " + str(offscreen_images_val))

listoffscreenimages = []
for x in range (offscreen_images_val):
    url = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["url"]
    totalbytes = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["totalBytes"]
    wastedbytes = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["wastedBytes"]
    wastedpercent = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["wastedPercent"]
    list1 = [url, totalbytes, wastedbytes, wastedpercent]
    listoffscreenimages.append(list1)
print("ALL in listoffscreenimages")
print("Example:")
if listoffscreenimages != []:
    print(listoffscreenimages[0])
else:
    print("No entries!")


 

listchains = []
print("Number of critical requests: " + str(len(final["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"].keys())))
for keys in final["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"].keys():
    try: 
        for values in final["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"][keys]["children"].values():
            url = values["request"]["url"]
            startime = values["request"]["startTime"]
            endtime = values["request"]["endTime"]
            transfersize = values["request"]["transferSize"]
            list1 = [url,startime,endtime,transfersize, keys]
            listchains.append(list1)
    except:
        continue
print("ALL in listchains")
print("Example:")
if listchains != []:
    print(listchains[0])
else:
    print("No entries!")

#BYTES

bytes_weight_score = final["lighthouseResult"]["audits"]["total-byte-weight"]["score"]
bytes_weight = final["lighthouseResult"]["audits"]["total-byte-weight"]["displayValue"]
print("Bytes weight score: " + str(bytes_weight_score))
print("Bytes weight: " + str(bytes_weight))
listbytes = []
for x in range (len(final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"][x]["url"]
    bytes_total = final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"][x]["totalBytes"]
    list1 = [url, bytes_total]
    listbytes.append(list1)

print("ALL in listbytes")
print("Example:")
if listbytes != []:
    print(listbytes[0])
else:
    print("No entries!")

#Responsive images

responsive_images_score = final["lighthouseResult"]["audits"]["uses-responsive-images"]["score"]
responsive_image_savings = final["lighthouseResult"]["audits"]["uses-responsive-images"]["displayValue"]
 
print("Responsive image score: " + str(responsive_images_score))
print("Responsive images savings: " + str(responsive_image_savings)) 
listresponsivesavings = []
for x in range (len(final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["url"]
    wastedbytes = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["wastedBytes"]
    totalbytes = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["totalBytes"]
    list1 = [url, wastedbytes, totalbytes]
    listresponsivesavings.append(list1)

print("ALL in listresponsivesavings")
print("Example:")
if listresponsivesavings != []:
    print(listresponsivesavings[0])
else:
    print("No entries!")

#Blocking resources
blocking_resources_score = final["lighthouseResult"]["audits"]["render-blocking-resources"]["score"]
#blocking_resoures_savings = final["lighthouseResult"]["audits"]["render-blocking-resources"]["displayValue"]
 
print("Blocking resources score: " + str(blocking_resources_score)) 

listblockingresources = []
for x in range (len(final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["url"]
    totalbytes = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["totalBytes"]
    wastedbytes = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["wastedMs"]
    list1 = [url, totalbytes, wastedbytes]
    listblockingresources.append(list1)

print("ALL in listblockingresources")
print("Example:")
if listblockingresources != []:
    print(listblockingresources[0])
else:
    print("No entries!")


#REL preload use

rel_preload_score = final["lighthouseResult"]["audits"]["uses-rel-preload"]["score"]
#rel_preload_savings = final["lighthouseResult"]["audits"]["uses-rel-preload"]["displayValue"]
print("Rel preload score: " + str(rel_preload_score)) 
listrelpreload = []
for x in range (len(final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"][x]["url"]
    wastedms = final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"][x]["wastedMs"]
    list1 = [url, wastedms]
    listrelpreload.append(list1)   

print("ALL in listrelpreload")
print("Example:")
if listrelpreload != []:
    print(listrelpreload[0])
else:
    print("No entries!")
#Redirects
redirects_score = final["lighthouseResult"]["audits"]["redirects"]["score"]
num_redirects = len(final["lighthouseResult"]["audits"]["redirects"]["details"]["items"])
 
print("Redirects score: " + str(redirects_score))
print("Redirects number: " + str(num_redirects))  
listredirects = []
for x in range (num_redirects):
    url = final["lighthouseResult"]["audits"]["redirects"]["details"]["items"][x]["url"]
    wastedms = final["lighthouseResult"]["audits"]["redirects"]["details"]["items"][x]["wastedMs"]
    list1 = [url,wastedms]
    listredirects.append(list1)

print("ALL in listredirects")
print("Example:")
if listredirects != []:
    print(listredirects[0])
else:
    print("No entries!")

#Unused JS

unused_js_score = final["lighthouseResult"]["audits"]["unused-javascript"]["score"]
num_unused_js = len(final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"])
 
print("Unused JS score: " + str(unused_js_score))
print("Unused JS number: " + str(num_unused_js))  

listunusedjavascript = []
for x in range (num_unused_js):
    url = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["url"]
    totalbytes = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["totalBytes"]
    wastedbytes = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["wastedBytes"]
    wastedpercentage= final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["wastedPercent"]
    list1 = [url, totalbytes, wastedbytes, wastedpercentage]
    listunusedjavascript.append(list1)

print("ALL in listunusedjavascript")
print("Example:")
if listunusedjavascript != []:
    print(listunusedjavascript[0])
else:
    print("No entries!")

#Blocking time

blocking_time_score = final["lighthouseResult"]["audits"]["total-blocking-time"]["score"]
blocking_time_duration = final["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"]

print("Blocking time score: " + str(blocking_time_score))
print("Blocking time: " + str(blocking_time_duration))  

#First meaningful Paint

fmp_score = final["lighthouseResult"]["audits"]["first-meaningful-paint"]["score"]
fmp = final["lighthouseResult"]["audits"]["first-meaningful-paint"]["displayValue"]

print("FMP score: " + str(fmp_score))
print("FMP time: " + str(fmp)) 

#Cumulative layout shift

cls_score = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"]
cls = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]

print("CLS score: " + str(cls_score))
print("CLS time: " + str(cls)) 

#Network Round trip times

network_rtt = final["lighthouseResult"]["audits"]["network-rtt"]["displayValue"]

print("RTT: " + str(network_rtt)) 

#Speed index

speed_index_score = final["lighthouseResult"]["audits"]["speed-index"]["score"]
speed_index = final["lighthouseResult"]["audits"]["speed-index"]["displayValue"]

print("Speed index score: " + str(speed_index_score))
print("Speed index: " + str(speed_index)) 

#Use of rel preconnect

rel_preconnect_score = final["lighthouseResult"]["audits"]["uses-rel-preconnect"]["score"]
rel_preconnect_warning = final["lighthouseResult"]["audits"]["uses-rel-preconnect"]["warnings"]

print("Rel preconnect score: " + str(rel_preconnect_score))
print("Rel preconnect warnings: " + str(rel_preconnect_warning)) 

# Optimized images

optimized_images_score = final["lighthouseResult"]["audits"]["uses-optimized-images"]["score"]
optimized_images = final["lighthouseResult"]["audits"]["uses-optimized-images"]["displayValue"]
 
print("Optimized images score: " + str(optimized_images_score))
print("Savings: " + str(optimized_images)) 

listoptimisedimages = []
for x in range (len(final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["url"]
    wastedbytes = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["wastedBytes"]
    totalbytes = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["totalBytes"]
    list1 = [url, wastedbytes, totalbytes]
    listoptimisedimages.append(list1)

print("ALL in listoptimisedimages")
print("Example:")
if listoptimisedimages != []:
    print(listoptimisedimages[0])
else:
    print("No entries!")

#Unminiified JS

unminified_javascript_score = final["lighthouseResult"]["audits"]["unminified-javascript"]["score"]
#unminified_javascript_savings = final["lighthouseResult"]["audits"]["unminified-javascript"]["displayValue"]
 
print("Unminified JS score: " + str(unminified_javascript_score))

listunminifiedjavascript = []
for x in range (len(final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["url"]
    wastedbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["wastedBytes"]
    totalbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["totalBytes"]
    wastedpercent = totalbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["wastedPercent"]
    list1 = [url, wastedbytes, totalbytes, wastedpercent]
    listunminifiedjavascript.append(list1)

print("ALL in listunminifiedjavascript")
print("Example:")
if listunminifiedjavascript != []:
    print(listunminifiedjavascript[0])
else:
    print("No entries!")

#Font display

font_display_score = final["lighthouseResult"]["audits"]["font-display"]["score"]

print("Font display score: " + str(font_display_score))

listfonts = []
for x in range (len(final["lighthouseResult"]["audits"]["font-display"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["font-display"]["details"]["items"][x]["url"]
    wasted_ms = final["lighthouseResult"]["audits"]["font-display"]["details"]["items"][x]["wastedMs"]
    list1 = [url, wasted_ms]
    listfonts.append(list1)

#No document write

no_document_write_score = final["lighthouseResult"]["audits"]["no-document-write"]["score"]

print("No document write score: " + str(no_document_write_score))

listnodocumentwrite = []
for x in range (len(final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"])):
    url = final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"][x]["url"]
    line = final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"][x]["label"]
    list1 = [url, line]
    listnodocumentwrite.append(list1)

print("ALL in listnodocumentwrite")
print("Example:")
if listnodocumentwrite != []:
    print(listnodocumentwrite[0])
else:
    print("No entries!")

#Text compression

text_compression_score = final["lighthouseResult"]["audits"]["uses-text-compression"]["score"]
print("Text compression score: " + str(no_document_write_score))

list_compressions_texts = []
for x in final["lighthouseResult"]["audits"]["uses-text-compression"]["details"]["items"]:
    list_compressions_texts.append(x)


print("ALL in list_compressions_texts")
print("Example:")
if list_compressions_texts != []:
    print(list_compressions_texts[0])
else:
    print("No entries!")


#LCP
lcp_elements = final["lighthouseResult"]["audits"]["largest-contentful-paint-element"]["displayValue"]


print("LCP load: " + str(lcp_elements))

#Animated content score

animated_content_score = final["lighthouseResult"]["audits"]["efficient-animated-content"]["score"]
print("Animated content score: " + str(animated_content_score))

#Unused CSS rules

unused_css_score = final["lighthouseResult"]["audits"]["unused-css-rules"]["score"]
#unused_css_savings = final["lighthouseResult"]["audits"]["unused-css-rules"]["displayValue"]
try:
    css_total_bytes = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["totalBytes"]
    css_wasted_bytes = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["wastedBytes"]
    css_wasted_percentage = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["wastedPercent"]
    print("CSS wasted percentage: " + str(css_wasted_percentage))
except:
    print("No wasted bytes")
print("Unused CSS score: " + str(unused_css_score))
#print("Unused CSS savings: " + str(unused_css_savings)) 

#Image thumbnails

import base64
 
for x in range (len(final["lighthouseResult"]["audits"]["screenshot-thumbnails"]["details"]["items"])):
    img_data = final["lighthouseResult"]["audits"]["screenshot-thumbnails"]["details"]["items"][x]["data"].replace("data:image/jpeg;base64,","")

#NEEDS TO BE DECODED if wanna use base64.b64decode(img_data)

#Network server latency

network_server_latency = final["lighthouseResult"]["audits"]["network-server-latency"]["displayValue"]

print("Network latency: " + network_server_latency)

#Layout shift elements
#layout_shift_elements = final["lighthouseResult"]["audits"]["layout-shift-elements"]["displayValue"]

#print()
#listpath_selector = []
#for x in range (len(final["lighthouseResult"]["audits"]["layout-shift-elements"]["details"]["items"])):
#    path = final["lighthouseResult"]["audits"]["layout-shift-elements"]["details"]["items"][x]["node"]["path"]
#    selector = final["lighthouseResult"]["audits"]["layout-shift-elements"]["details"]["items"][x]["node"]["selector"]
#    list1 = [path, selector]
#    listpath_selector.append(list1)



"""
for k, v in final['lighthouseResult']['audits'].items():
    try:
       if(v["score"] < 1):
              print(v["title"])
              print(v["description"])
              print(v["displayValue"])
              print(v["score"] * 100 + '%')
              print('-------------------------------------------------------')
    except:
          
         try: 
            print(v["displayValue"])
         except:
               print("KEY: " + k)
with open("sample_audit.json", "w") as outfile:
    json.dump(final['lighthouseResult']['audits'], outfile)
try:
        urlid = final['id']
        split = urlid.split('?') # This splits the absolute url from the api key parameter
        urlid = split[0] # This reassigns urlid to the absolute url
        ID = f'URL ~ {urlid}'
        ID2 = str(urlid)
        urlfcp = final['lighthouseResult']['audits']['first-contentful-paint']['displayValue']
        FCP = f'First Contentful Paint ~ {str(urlfcp)}'
        FCP2 = str(urlfcp)
        urlfi = final['lighthouseResult']['audits']['interactive']['displayValue']
        FI = f'First Interactive ~ {str(urlfi)}'
        FI2 = str(urlfi)
except KeyError:
        print(f'<KeyError> One or more keys not found {line}.')

try:
        print(ID) 
        print(FCP)
        print(FI)
except NameError:
        print(f'<NameError> Failing because of KeyError {line}.')

"""