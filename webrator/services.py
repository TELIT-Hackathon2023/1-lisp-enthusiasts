import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

MAX_DEPTH = 1

def get_web_type_from_users(json_data):
    users = list(json_data.keys())
    prompt = ", ".join(user.split(". ")[1] for user in users)
    prompt += "\n"
    prompt += "I would like to help this groups of people by creating a website for them. I have three websites, one for technical people, one for non technical people and one for artists. On average, which website do you think this group of people would like most ? I need to divide them on average it doesnt need to be precise. Answer with only one word with one of the three websites i mentioned. That means technical, non-technical or artists Thank you"
    
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ])

    return(completion['choices'][0]['message']['content'])


def get_text_and_html_from_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text(separator=' ')
        cleaned_text = ' '.join(text_content.split())
        return cleaned_text, response.text
    else:
        print(f"Error: Unable to fetch content from {url}. Status code: {response.status_code}")
        return None, None
    

def is_valid_url(url):
    ignored_file_extensions = ['.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.zip', '.rar']
    return not any(url.endswith(ext) for ext in ignored_file_extensions)


def get_text_from_website(current_url, start_url, visited_urls, depth=0, max_depth=MAX_DEPTH):
    if depth > MAX_DEPTH or current_url in visited_urls:
        return ""

    visited_urls.add(current_url)
    cleaned_text, page_html = get_text_and_html_from_page(current_url)

    if cleaned_text:
        soup = BeautifulSoup(page_html, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            absolute_url = urljoin(current_url, link['href'])
            if is_valid_url(absolute_url) and urlparse(absolute_url).netloc == urlparse(start_url).netloc:
                cleaned_text += get_text_from_website(absolute_url, start_url, visited_urls, depth + 1, max_depth)

    return cleaned_text
    
def parse_json(final):
    final_json = {}
    if "loadingExperience" in final:
        if "metrics" in final["loadingExperience"]:
            fcp = final["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["percentile"] #into seconds (/1000)
            fid = final["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["percentile"] #into seconds (/1000)
            lcp = final["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["percentile"]
            cls = final["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["percentile"]/100

            fcp_score = final["loadingExperience"]["metrics"]["FIRST_CONTENTFUL_PAINT_MS"]["category"]
            fid_score = final["loadingExperience"]["metrics"]["FIRST_INPUT_DELAY_MS"]["category"]
            lcp_score = final["loadingExperience"]["metrics"]["LARGEST_CONTENTFUL_PAINT_MS"]["category"]
            cls_score = final["loadingExperience"]["metrics"]["CUMULATIVE_LAYOUT_SHIFT_SCORE"]["category"]

            final_json["fcp"] = fcp
            final_json["fid"] = fid
            final_json["lcp"] = lcp
            final_json["cls"] = cls
            final_json["fcp_category"] = fcp_score
            final_json["fid_category"] = fid_score
            final_json["lcp_category"] = lcp_score
            final_json["cls_category"] = cls_score

    overall_score = final["lighthouseResult"]["categories"]["performance"]["score"] * 100

    final_json["overall_score"] = overall_score

    total_tasks = final["lighthouseResult"]["audits"]["diagnostics"]["details"]["items"][0]["numTasks"]
    total_tasks_time = final["lighthouseResult"]["audits"]["diagnostics"]["details"]["items"][0]["totalTaskTime"]
    
    
    final_json["total_tasks"] = total_tasks
    final_json["total_tasks_time"] = total_tasks_time


    #NETWORK REQUESTS
    num_requests = len(final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"])
    final_json["num_requests"] = num_requests
    final_json["num_requests_description"] = final["lighthouseResult"]["audits"]["network-requests"]["description"]
    listrequests = []
    for x in range (num_requests):
        endtime = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["networkEndTime"]
        starttime = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["networkRequestTime"]
        transfersize = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["transferSize"]
        resourcesize = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["resourceSize"]
        url = final["lighthouseResult"]["audits"]["network-requests"]["details"]["items"][x]["url"]
        list1 = [endtime, starttime, transfersize, resourcesize, url]
        listrequests.append(list1)
 
    final_json["list_requests"] = listrequests
    #MAINTHREAD WORK

    mainthread_score = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["score"]
    mainthread_duration = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["displayValue"]
    final_json["mainthread_description"] = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["description"]
   
    final_json["mainthread_score"] = mainthread_score
    final_json["mainthread_duration"] = mainthread_duration
    listprocesses = []
    for x in range (len(final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"])):
        duration = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"][x]["duration"]
        process = final["lighthouseResult"]["audits"]["mainthread-work-breakdown"]["details"]["items"][x]["groupLabel"]
        list1 = [duration,process]
        listprocesses.append(list1)
    
    final_json["listprocesses"] = listprocesses
    #EVENT LISTENERS
    event_listeners_score = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["score"]
    final_json["event_listeners_description"] = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["description"]
    print("Event listeners score: " + str(event_listeners_score))
    final_json["event_listeners_score"] = event_listeners_score
    listevents = []
    for x in range (len(final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"][x]["url"]
        line = final["lighthouseResult"]["audits"]["uses-passive-event-listeners"]["details"]["items"][x]["label"]
        list1 = [url, line]
        listevents.append(list1)
    final_json["listevents"] = listevents
    #DOM SIZE

    dom_size_score = final["lighthouseResult"]["audits"]["dom-size"]["score"]
    dom_size_elements = final["lighthouseResult"]["audits"]["dom-size"]["displayValue"]
    final_json["dom_size_description"] = final["lighthouseResult"]["audits"]["dom-size"]["description"]
    final_json["dom_size_score"] = dom_size_score
    final_json["dom_size_elements"] = dom_size_elements
    #Offscreen images

    offscreen_images_score = final["lighthouseResult"]["audits"]["offscreen-images"]["score"]
    offscreen_images_val = len(final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"])
    final_json["offscreen-images_description"] = final["lighthouseResult"]["audits"]["offscreen-images"]["description"]
    final_json["offscreen_images_score"] = offscreen_images_score
    final_json["offscreen_images_elements"] = offscreen_images_val


    listoffscreenimages = []
    for x in range (offscreen_images_val):
        url = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["url"]
        totalbytes = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["totalBytes"]
        wastedbytes = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["wastedBytes"]
        wastedpercent = final["lighthouseResult"]["audits"]["offscreen-images"]["details"]["items"][x]["wastedPercent"]
        list1 = [url, totalbytes, wastedbytes, wastedpercent]
        listoffscreenimages.append(list1)

    final_json["listoffscreenimages"] = listoffscreenimages

    

    listchains = []
    print("Number of critical requests: " + str(len(final["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"].keys())))
    final_json["critical_req"] = str(len(final["lighthouseResult"]["audits"]["critical-request-chains"]["details"]["chains"].keys()))
    final_json["critical_req_description"] = final["lighthouseResult"]["audits"]["critical-request-chains"]["description"]
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
    final_json["listchains"] = listchains
    #BYTES

    bytes_weight_score = final["lighthouseResult"]["audits"]["total-byte-weight"]["score"]
    bytes_weight = final["lighthouseResult"]["audits"]["total-byte-weight"]["displayValue"]
    final_json["bytes_weight_description"] = final["lighthouseResult"]["audits"]["total-byte-weight"]["description"]
    
    final_json["bytes_weight_score"] = bytes_weight_score
    final_json["bytes_weight"] = bytes_weight
    listbytes = []
    for x in range (len(final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"][x]["url"]
        bytes_total = final["lighthouseResult"]["audits"]["total-byte-weight"]["details"]["items"][x]["totalBytes"]
        list1 = [url, bytes_total]
        listbytes.append(list1)
    final_json["listbytes"] = listbytes
    #Responsive images

    responsive_images_score = final["lighthouseResult"]["audits"]["uses-responsive-images"]["score"]
    final_json["responsive_images_description"] = final["lighthouseResult"]["audits"]["uses-responsive-images"]["description"]
    final_json["responsive_images_score"] = responsive_images_score
    try:
        responsive_image_savings = final["lighthouseResult"]["audits"]["uses-responsive-images"]["displayValue"]
        final_json["responsive_image_savings"] = responsive_image_savings

    except:
        final_json["responsive_image_savings"] = ""

        
    listresponsivesavings = []
    for x in range (len(final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["url"]
        wastedbytes = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["wastedBytes"]
        totalbytes = final["lighthouseResult"]["audits"]["uses-responsive-images"]["details"]["items"][x]["totalBytes"]
        list1 = [url, wastedbytes, totalbytes]
        listresponsivesavings.append(list1)

    final_json["listresponsivesavings"] = listresponsivesavings
    #Blocking resources
    blocking_resources_score = final["lighthouseResult"]["audits"]["render-blocking-resources"]["score"]
    #blocking_resoures_savings = final["lighthouseResult"]["audits"]["render-blocking-resources"]["displayValue"]
    final_json["blocking_resources_score"] = blocking_resources_score 
    final_json["blocking_resources_description"] = final["lighthouseResult"]["audits"]["render-blocking-resources"]["description"]

    listblockingresources = []
    for x in range (len(final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["url"]
        totalbytes = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["totalBytes"]
        wastedbytes = final["lighthouseResult"]["audits"]["render-blocking-resources"]["details"]["items"][x]["wastedMs"]
        list1 = [url, totalbytes, wastedbytes]
        listblockingresources.append(list1)

    final_json["listblockingresources"] = listblockingresources 

    #REL preload use

    rel_preload_score = final["lighthouseResult"]["audits"]["uses-rel-preload"]["score"]
    final_json["rel_preload_description"] = final["lighthouseResult"]["audits"]["uses-rel-preload"]["description"]
    #rel_preload_savings = final["lighthouseResult"]["audits"]["uses-rel-preload"]["displayValue"]
    final_json["rel_preload_score"] = rel_preload_score 
    listrelpreload = []
    for x in range (len(final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"][x]["url"]
        wastedms = final["lighthouseResult"]["audits"]["uses-rel-preload"]["details"]["items"][x]["wastedMs"]
        list1 = [url, wastedms]
        listrelpreload.append(list1)   
    final_json["listrelpreload"] = listrelpreload
    #Redirects
    redirects_score = final["lighthouseResult"]["audits"]["redirects"]["score"]
    final_json["redirects_description"] = final["lighthouseResult"]["audits"]["redirects"]["description"]
    num_redirects = len(final["lighthouseResult"]["audits"]["redirects"]["details"]["items"])
    final_json["redirects_score"] = redirects_score
    final_json["num_redirects"] = num_redirects

    listredirects = []
    for x in range (num_redirects):
        url = final["lighthouseResult"]["audits"]["redirects"]["details"]["items"][x]["url"]
        wastedms = final["lighthouseResult"]["audits"]["redirects"]["details"]["items"][x]["wastedMs"]
        list1 = [url,wastedms]
        listredirects.append(list1)

    final_json["listredirects"] = listredirects
    #Unused JS

    unused_js_score = final["lighthouseResult"]["audits"]["unused-javascript"]["score"]
    num_unused_js = len(final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"])
    final_json["unused_js_description"] = final["lighthouseResult"]["audits"]["unused-javascript"]["description"]
    final_json["unused_js_score"] = unused_js_score
    final_json["num_unused_js"] = num_unused_js

    listunusedjavascript = []
    for x in range (num_unused_js):
        url = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["url"]
        totalbytes = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["totalBytes"]
        wastedbytes = final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["wastedBytes"]
        wastedpercentage= final["lighthouseResult"]["audits"]["unused-javascript"]["details"]["items"][x]["wastedPercent"]
        list1 = [url, totalbytes, wastedbytes, wastedpercentage]
        listunusedjavascript.append(list1)

    final_json["listunusedjavascript"] = listunusedjavascript
    #Blocking time

    blocking_time_score = final["lighthouseResult"]["audits"]["total-blocking-time"]["score"]
    final_json["blocking_time_description"] = final["lighthouseResult"]["audits"]["total-blocking-time"]["description"]
    try:
        blocking_time_duration = final["lighthouseResult"]["audits"]["total-blocking-time"]["displayValue"]
        final_json["blocking_time_duration"] = blocking_time_duration
    except:
        final_json["blocking_time_duration"] = ""
    final_json["blocking_time_score"] = blocking_time_score

    #First meaningful Paint

    fmp_score = final["lighthouseResult"]["audits"]["first-meaningful-paint"]["score"]
    final_json["fmp_score_description"] = final["lighthouseResult"]["audits"]["first-meaningful-paint"]["description"]
    final_json["fmp_score_audit"] = fmp_score
    try:
        fmp = final["lighthouseResult"]["audits"]["first-meaningful-paint"]["displayValue"]
        final_json["fmp_audit"] = fmp
        
    except:
        final_json["fmp_audit"] = ""

        

    #Cumulative layout shift

    cls_score = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["score"]
    final_json["cls_score_description"] = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["description"]
    final_json["cls_score_audit"] = cls_score
    try:
        cls = final["lighthouseResult"]["audits"]["cumulative-layout-shift"]["displayValue"]
        final_json["cls_audit"] = cls_score
    except:
        final_json["cls_audit"] = ""


    #Network Round trip times

    network_rtt = final["lighthouseResult"]["audits"]["network-rtt"]["displayValue"]
    final_json["network_rtt_description"] = final["lighthouseResult"]["audits"]["network-rtt"]["description"]
    final_json["network_rtt"] = network_rtt

    #Speed index

    speed_index_score = final["lighthouseResult"]["audits"]["speed-index"]["score"]
    final_json["speed_index_description"] = final["lighthouseResult"]["audits"]["speed-index"]["description"]
    speed_index = final["lighthouseResult"]["audits"]["speed-index"]["displayValue"]
    final_json["speed_index_score"] = speed_index_score
    final_json["speed_index"] = speed_index

    #Use of rel preconnect

    rel_preconnect_score = final["lighthouseResult"]["audits"]["uses-rel-preconnect"]["score"]
    final_json["rel_preconnect_description"] = final["lighthouseResult"]["audits"]["uses-rel-preconnect"]["description"]
    rel_preconnect_warning = final["lighthouseResult"]["audits"]["uses-rel-preconnect"]["warnings"]

    final_json["rel_preconnect_score"] = rel_preconnect_score
    final_json["rel_preconnect_warning"] = rel_preconnect_warning

    # Optimized images

    optimized_images_score = final["lighthouseResult"]["audits"]["uses-optimized-images"]["score"]
    final_json["optimized_images_description"] = final["lighthouseResult"]["audits"]["uses-optimized-images"]["description"]
    optimized_images = final["lighthouseResult"]["audits"]["uses-optimized-images"]["displayValue"]
    

    final_json["optimized_images_score"] = optimized_images_score
    final_json["optimized_images"] = optimized_images

    listoptimisedimages = []
    for x in range (len(final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["url"]
        wastedbytes = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["wastedBytes"]
        totalbytes = final["lighthouseResult"]["audits"]["uses-optimized-images"]["details"]["items"][x]["totalBytes"]
        list1 = [url, wastedbytes, totalbytes]
        listoptimisedimages.append(list1)

    final_json["listoptimisedimages"] = listoptimisedimages
    #Unminiified JS

    unminified_javascript_score = final["lighthouseResult"]["audits"]["unminified-javascript"]["score"]
    final_json["unminified_javascript_description"] = final["lighthouseResult"]["audits"]["unminified-javascript"]["description"]
    #unminified_javascript_savings = final["lighthouseResult"]["audits"]["unminified-javascript"]["displayValue"]
    final_json["unminified_javascript_score"] = unminified_javascript_score

    listunminifiedjavascript = []
    for x in range (len(final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["url"]
        wastedbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["wastedBytes"]
        totalbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["totalBytes"]
        wastedpercent = totalbytes = final["lighthouseResult"]["audits"]["unminified-javascript"]["details"]["items"][x]["wastedPercent"]
        list1 = [url, wastedbytes, totalbytes, wastedpercent]
        listunminifiedjavascript.append(list1)

    final_json["listunminifiedjavascript"] = listunminifiedjavascript
    #Font display

    font_display_score = final["lighthouseResult"]["audits"]["font-display"]["score"]
    final_json["font_display_description"] = final["lighthouseResult"]["audits"]["font-display"]["description"]
    final_json["font_display_score"] = font_display_score

    listfonts = []
    for x in range (len(final["lighthouseResult"]["audits"]["font-display"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["font-display"]["details"]["items"][x]["url"]
        wasted_ms = final["lighthouseResult"]["audits"]["font-display"]["details"]["items"][x]["wastedMs"]
        list1 = [url, wasted_ms]
        listfonts.append(list1)
    final_json["listfonts"] = listfonts
    #No document write

    no_document_write_score = final["lighthouseResult"]["audits"]["no-document-write"]["score"]
    final_json["no_document_write_description"] = final["lighthouseResult"]["audits"]["no-document-write"]["description"]
    final_json["no_document_write_score"] = no_document_write_score
    
    listnodocumentwrite = []
    for x in range (len(final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"][x]["url"]
        line = final["lighthouseResult"]["audits"]["no-document-write"]["details"]["items"][x]["label"]
        list1 = [url, line]
        listnodocumentwrite.append(list1)
    final_json["listnodocumentwrite"] = listnodocumentwrite
    #Text compression

    text_compression_score = final["lighthouseResult"]["audits"]["uses-text-compression"]["score"]
    final_json["text_compression_description"] = final["lighthouseResult"]["audits"]["uses-text-compression"]["description"]
    final_json["text_compression_score"] = text_compression_score
    list_compressions_texts = []
    for x in final["lighthouseResult"]["audits"]["uses-text-compression"]["details"]["items"]:
        list_compressions_texts.append(x)

    final_json["list_compressions_texts"] = list_compressions_texts

    #LCP
    lcp_elements = final["lighthouseResult"]["audits"]["largest-contentful-paint-element"]["displayValue"]
    final_json["lcp_elements_description"] = final["lighthouseResult"]["audits"]["largest-contentful-paint-element"]["description"]
    final_json["lcp_elements"] = lcp_elements


    #Animated content score

    animated_content_score = final["lighthouseResult"]["audits"]["efficient-animated-content"]["score"]
    final_json["animated_content_description"] = final["lighthouseResult"]["audits"]["efficient-animated-content"]["description"]
    final_json["animated_content_score"] = animated_content_score
    #Unused CSS rules

    unused_css_score = final["lighthouseResult"]["audits"]["unused-css-rules"]["score"]
    final_json["unused_css_description"] = final["lighthouseResult"]["audits"]["unused-css-rules"]["description"]
    final_json["unused_css_score"] = unused_css_score
    try:
        unused_css_savings = final["lighthouseResult"]["audits"]["unused-css-rules"]["displayValue"]
        
        final_json["unused_css_savings"] = unused_css_savings
    except:
        final_json["unused_css_savings"] = ""
    try:
        css_total_bytes = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["totalBytes"]
        css_wasted_bytes = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["wastedBytes"]
        css_wasted_percentage = final["lighthouseResult"]["audits"]["unused-css-rules"]["details"]["items"][0]["wastedPercent"]
        final_json["css_wasted_percentage"] = css_wasted_percentage
    except:
        final_json["css_wasted_percentage"] = ""
       



    #Image thumbnails

    import base64
    
    for x in range (len(final["lighthouseResult"]["audits"]["screenshot-thumbnails"]["details"]["items"])):
        img_data = final["lighthouseResult"]["audits"]["screenshot-thumbnails"]["details"]["items"][x]["data"].replace("data:image/jpeg;base64,","")
    final_json["thumbnails"] = img_data
    #NEEDS TO BE DECODED if wanna use base64.b64decode(img_data)

    #Network server latency

    network_server_latency = final["lighthouseResult"]["audits"]["network-server-latency"]["displayValue"]
    final_json["network_server_latency_description"] = final["lighthouseResult"]["audits"]["network-server-latency"]["description"]
    final_json["network_server_latency"] = network_server_latency


    #Cache memory
    cache_memory_score = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["score"]
    final_json["cache_memory_description"] = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["description"]
    final_json["cache_memory_score"] = cache_memory_score
    try:
        resources_to_cache = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["displayValue"]
        final_json["resources_to_cache"] = resources_to_cache
    except:
        final_json["resources_to_cache"] = ""

    listcache = []
    for x in range (len(final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["details"]["items"])):
        cachelifetime = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["details"]["items"][x]["cacheLifetimeMs"]
        totalbytes = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["details"]["items"][x]["totalBytes"]
        wastedbytes = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["details"]["items"][x]["wastedBytes"]
        url = final["lighthouseResult"]["audits"]["uses-long-cache-ttl"]["details"]["items"][x]["url"]
        list1 = [cachelifetime, totalbytes, wastedbytes, url]
        listcache.append(list1)

    final_json["listcache"] = listcache


    #FID
    max_potential_fid = final["lighthouseResult"]["audits"]["max-potential-fid"]["score"]
    max_potential_fid_value = final["lighthouseResult"]["audits"]["max-potential-fid"]["displayValue"]
    final_json["max_potential_fid_description"] = final["lighthouseResult"]["audits"]["max-potential-fid"]["description"]
    final_json["max_potential_fid"] = max_potential_fid
    final_json["max_potential_fid_value"] = max_potential_fid_value
 

    #Server response time

    server_response_time_score = final["lighthouseResult"]["audits"]["server-response-time"]["score"]
    final_json["server_response_time_description"] = final["lighthouseResult"]["audits"]["server-response-time"]["description"]
    server_response_time = final["lighthouseResult"]["audits"]["server-response-time"]["displayValue"]

    final_json["server_response_time_score"] = server_response_time_score
    final_json["server_response_time"] = server_response_time


    #Time to interactive

    time_interactive_score = final["lighthouseResult"]["audits"]["interactive"]["score"]
    final_json["time_interactive_description"] = final["lighthouseResult"]["audits"]["interactive"]["description"]
    time_interactive = final["lighthouseResult"]["audits"]["interactive"]["displayValue"]

    final_json["time_interactive_score"] = time_interactive_score
    final_json["time_interactive"] = time_interactive


    #Uminified CSS

    unminified_css = final["lighthouseResult"]["audits"]["unminified-css"]["score"]
    final_json["unminified_css_description"] = final["lighthouseResult"]["audits"]["unminified-css"]["description"]
    unminified_css_savings = final["lighthouseResult"]["audits"]["unminified-css"]["details"]["overallSavingsMs"]

    final_json["unminified_css"] = unminified_css
    final_json["unminified_css_savings"] = unminified_css_savings

    #Bootup time

    bootup_time_score = final["lighthouseResult"]["audits"]["bootup-time"]["score"]
    final_json["bootup_time_description"] = final["lighthouseResult"]["audits"]["bootup-time"]["description"]

    final_json["bootup_time_score"] = bootup_time_score


    #Modern images

    modern_images_score = final["lighthouseResult"]["audits"]["modern-image-formats"]["score"]
    final_json["modern_images_description"] = final["lighthouseResult"]["audits"]["modern-image-formats"]["description"]
    modern_images_savings = final["lighthouseResult"]["audits"]["modern-image-formats"]["displayValue"]

    final_json["modern_images_score"] = modern_images_score
    final_json["modern_images_savings"] = modern_images_savings 

    listmodernimages = []
    for x in range (len(final["lighthouseResult"]["audits"]["modern-image-formats"]["details"]["items"])):
        url = final["lighthouseResult"]["audits"]["modern-image-formats"]["details"]["items"][x]["url"]
        wastedbytes = final["lighthouseResult"]["audits"]["modern-image-formats"]["details"]["items"][x]["wastedBytes"]
        totalbytes = final["lighthouseResult"]["audits"]["modern-image-formats"]["details"]["items"][x]["totalBytes"]
        list1 = [url, wastedbytes, totalbytes]
        listmodernimages.append(list1)

    final_json["listmodernimages"] = listmodernimages 
    #third party entity

    third_party_score = final["lighthouseResult"]["audits"]["third-party-summary"]["score"]
    final_json["third_party_description"] = final["lighthouseResult"]["audits"]["third-party-summary"]["description"]
    final_json["third_party_score"] = third_party_score 

    #Final screen of page

    import base64
    
    img_data_final = final["lighthouseResult"]["audits"]["final-screenshot"]["details"]["data"].replace("data:image/jpeg;base64,","")
    
    final_json["final_load_img"] = img_data_final
    #NEEDS TO BE DECODED base64.b64decode(img_data_final)

    #LCP lazily loaded 

    lcp_lazy_loaded = final["lighthouseResult"]["audits"]["lcp-lazy-loaded"]["score"]
    final_json["lcp_lazy_loaded_description"] = final["lighthouseResult"]["audits"]["lcp-lazy-loaded"]["description"]
    final_json["lcp_lazy_loaded"] = lcp_lazy_loaded


    try:
        list_lcp_lazy_loaded = []
        for x in final["lighthouseResult"]["audits"]["lcp-lazy-loaded"]["details"]["items"]:
            nodes = x["node"]["nodeLabel"]
            snippet = x["node"]["snippet"]
            list_lcp_lazy_loaded.append([nodes,snippet])

        final_json["list_lcp_lazy_loaded"] = list_lcp_lazy_loaded
    except:
        final_json["list_lcp_lazy_loaded"] = ""
    #Duplicated JS

    duplicated_javascript = final["lighthouseResult"]["audits"]["duplicated-javascript"]["score"]
    final_json["duplicated_javascript_description"] = final["lighthouseResult"]["audits"]["duplicated-javascript"]["description"]
    final_json["duplicated_javascript"] = duplicated_javascript

    list_duplicated_javascript = []
    for x in final["lighthouseResult"]["audits"]["duplicated-javascript"]["details"]["items"]:
        list_duplicated_javascript.append(x)
    final_json["list_duplicated_javascript"] = list_duplicated_javascript
    #Non Composited animations
    non_composited_animations = final["lighthouseResult"]["audits"]["non-composited-animations"]["score"]
    final_json["non_composited_animations_description"] = final["lighthouseResult"]["audits"]["non-composited-animations"]["description"]
    final_json["non_composited_animations"] = non_composited_animations
    list_composited_animations = []
    for x in final["lighthouseResult"]["audits"]["non-composited-animations"]["details"]["items"]:
        animation = x["subItems"]["items"][0]["animation"]
        failure = x["subItems"]["items"][0]["failureReason"]
        list_composited_animations.append([animation,failure])
    final_json["list_composited_animations"] = list_composited_animations
    #Legacy JS

    legacy_js = final["lighthouseResult"]["audits"]["legacy-javascript"]["score"]
    final_json["legacy_js_description"] = final["lighthouseResult"]["audits"]["legacy-javascript"]["description"]
    final_json["legacy_js"] = legacy_js


    urls_legacy_js = []
    for x in final["lighthouseResult"]["audits"]["legacy-javascript"]["details"]["items"]:
        for y in x["subItems"]["items"]:
            urls_legacy_js.append([y["location"]["url"]])

    final_json["urls_legacy_js"] = urls_legacy_js
    #Unsized images

    unsized_images = final["lighthouseResult"]["audits"]["unsized-images"]["score"]
    final_json["unsized_images_description"] = final["lighthouseResult"]["audits"]["unsized-images"]["description"]
    final_json["unsized_images"] = unsized_images
    

    unsized_images_list = []
    for x in final["lighthouseResult"]["audits"]["unsized-images"]["details"]["items"]:
        unsized_images_list.append([x["url"], x["node"]["snippet"]])
    final_json["unsized_images_list"] = unsized_images_list
    #TREEMAP 
    list_apps = []
    for x in final["lighthouseResult"]["audits"]["script-treemap-data"]["details"]["nodes"]:
        try:
            list_apps.append([x["name"],x["resourceBytes"], x["unusedBytes"]])
        except:
            list_apps.append([x["name"],x["resourceBytes"], 0])   

    #Third party facade
    final_json["list_apps"] = list_apps
    third_party_facade = final["lighthouseResult"]["audits"]["third-party-facades"]["score"]
    final_json["third_party_facade_description"] = final["lighthouseResult"]["audits"]["third-party-facades"]["description"]

    final_json["third_party_facade"] = third_party_facade

    #Preload LCP image
    preload_lcp_image = final["lighthouseResult"]["audits"]["prioritize-lcp-image"]["score"]
    final_json["preload_lcp_image_description"] = final["lighthouseResult"]["audits"]["prioritize-lcp-image"]["description"]
    final_json["preload_lcp_image"] = preload_lcp_image
    list_preload_lcp_images = []
    for x in final["lighthouseResult"]["audits"]["prioritize-lcp-image"]["details"]["items"]:
        list_preload_lcp_images.append(x)
    final_json["list_preload_lcp_images"] = list_preload_lcp_images
    return final_json