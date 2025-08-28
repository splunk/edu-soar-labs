"""
This is the solution playbook for lab 3. This playbook receives a url input and looks it up in http_intel collection. If found, it will return a threat key and date created.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'format_the_json_query_to_find_a_record' block
    format_the_json_query_to_find_a_record(container=container)

    return

@phantom.playbook_block()
def format_the_json_query_to_find_a_record(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_the_json_query_to_find_a_record() called")

    template = """{{\"url\":\"{0}\"}}"""

    # parameter list for template variable replacement
    parameters = [
        "playbook_input:url"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_the_json_query_to_find_a_record")

    format_the_rest_endpoint(container=container)

    return


@phantom.playbook_block()
def format_the_rest_endpoint(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_the_rest_endpoint() called")

    template = """storage/collections/data/http_intel?query=\n{0}\n"""

    # parameter list for template variable replacement
    parameters = [
        "format_the_json_query_to_find_a_record:formatted_data"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_the_rest_endpoint")

    lookup_url_in_http_intel_threat_list(container=container)

    return


@phantom.playbook_block()
def lookup_url_in_http_intel_threat_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("lookup_url_in_http_intel_threat_list() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    format_the_rest_endpoint = phantom.get_format_data(name="format_the_rest_endpoint")

    parameters = []

    if format_the_rest_endpoint is not None:
        parameters.append({
            "location": format_the_rest_endpoint,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("get data", parameters=parameters, name="lookup_url_in_http_intel_threat_list", assets=["splunk es"], callback=debug_1)

    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    lookup_url_in_http_intel_threat_list_result_data = phantom.collect2(container=container, datapath=["lookup_url_in_http_intel_threat_list:action_result.data","lookup_url_in_http_intel_threat_list:action_result.parameter.context.artifact_id"], action_results=results)

    lookup_url_in_http_intel_threat_list_result_item_0 = [item[0] for item in lookup_url_in_http_intel_threat_list_result_data]

    parameters = []

    parameters.append({
        "input_1": lookup_url_in_http_intel_threat_list_result_item_0,
        "input_2": None,
        "input_3": None,
        "input_4": None,
        "input_5": None,
        "input_6": None,
        "input_7": None,
        "input_8": None,
        "input_9": None,
        "input_10": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_1")

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    lookup_url_in_http_intel_threat_list_result_data = phantom.collect2(container=container, datapath=["lookup_url_in_http_intel_threat_list:action_result.data.*.parsed_response_body.*.threat_key","lookup_url_in_http_intel_threat_list:action_result.data.*.parsed_response_body.*.time"])

    lookup_url_in_http_intel_threat_list_result_item_0 = [item[0] for item in lookup_url_in_http_intel_threat_list_result_data]
    lookup_url_in_http_intel_threat_list_result_item_1 = [item[1] for item in lookup_url_in_http_intel_threat_list_result_data]

    output = {
        "threat_key": lookup_url_in_http_intel_threat_list_result_item_0,
        "date_created": lookup_url_in_http_intel_threat_list_result_item_1,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_playbook_output_data(output=output)

    return