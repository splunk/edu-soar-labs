import phantom.rules as phantom
#import json
#from datetime import datetime, timedelta

def clean_closed_containers():
    # deletes all finding containers in status_name == "Closed"
        
    containers_url = phantom.build_phantom_rest_url('container') + "?page_size=0&_filter_data__status_name=\"Closed\""
    response = phantom.requests.get(containers_url, verify=False)
    containers = response.json().get('data', [])
    
    if len(containers)==0:
        phantom.debug("Did not find any closed containers")
        return
    
    phantom.debug(f"Found {len(containers)} closed containers, deleting...")
    
    for container in containers:
        delete_url = phantom.build_phantom_rest_url('container', container["id"])
        delete_response = phantom.requests.delete(delete_url, verify=False)

def on_start(container):
    phantom.debug('on_start() called')
    clean_closed_containers()

def on_finish(container, summary):
    phantom.debug("on_finish() called")