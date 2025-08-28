"""
This is the solution playbook for lab 5. This playbook receives url, threat key, and date created as input.  It will create a record in the http_intel collection with the inputs.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'format_json_for_http_intel_record' block
    format_json_for_http_intel_record(container=container)

    return

@phantom.playbook_block()
def format_json_for_http_intel_record(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_json_for_http_intel_record() called")

    template = """{{\"_key\": \"{0}\", \"url\": \"{0}\", \"threat_key\": \"{1}\", \"time\": {2} }}"""

    # parameter list for template variable replacement
    parameters = [
        "playbook_input:url",
        "playbook_input:threat_key",
        "playbook_input:time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_json_for_http_intel_record")

    format_endpoint_to_update_collection(container=container)

    return


@phantom.playbook_block()
def format_endpoint_to_update_collection(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_endpoint_to_update_collection() called")

    template = """storage/collections/data/http_intel"""

    # parameter list for template variable replacement
    parameters = []

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_endpoint_to_update_collection")

    format_headers(container=container)

    return


@phantom.playbook_block()
def format_headers(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_headers() called")

    template = """{\"Content-Type\": \"application/json\"}\n"""

    # parameter list for template variable replacement
    parameters = []

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_headers")

    update_http_intel_with_new_threat(container=container)

    return


@phantom.playbook_block()
def update_http_intel_with_new_threat(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("update_http_intel_with_new_threat() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    format_json_for_http_intel_record = phantom.get_format_data(name="format_json_for_http_intel_record")
    format_headers = phantom.get_format_data(name="format_headers")
    format_endpoint_to_update_collection = phantom.get_format_data(name="format_endpoint_to_update_collection")

    parameters = []

    if format_endpoint_to_update_collection is not None:
        parameters.append({
            "body": format_json_for_http_intel_record,
            "headers": format_headers,
            "location": format_endpoint_to_update_collection,
            "verify_certificate": False,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("post data", parameters=parameters, name="update_http_intel_with_new_threat", assets=["splunk es"])

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    update_http_intel_with_new_threat_result_data = phantom.collect2(container=container, datapath=["update_http_intel_with_new_threat:action_result.summary.status_code"])

    update_http_intel_with_new_threat_summary_status_code = [item[0] for item in update_http_intel_with_new_threat_result_data]

    output = {
        "update_kv_store_status": update_http_intel_with_new_threat_summary_status_code,
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