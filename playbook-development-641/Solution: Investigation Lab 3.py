"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'locate_source' block
    locate_source(container=container)
    # call 'source_reputation' block
    source_reputation(container=container)
    # call 'virus_search' block
    virus_search(container=container)

    return

@phantom.playbook_block()
def locate_source(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("locate_source() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceAddress","artifact:*.id"])

    parameters = []

    # build parameters list for 'locate_source' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
            parameters.append({
                "ip": container_artifact_item[0],
                "context": {'artifact_id': container_artifact_item[1]},
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("geolocate ip", parameters=parameters, name="locate_source", assets=["maxmind"], callback=join_check_reports)

    return


@phantom.playbook_block()
def source_reputation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("source_reputation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceDnsDomain","artifact:*.id"])

    parameters = []

    # build parameters list for 'source_reputation' call
    for container_artifact_item in container_artifact_data:
        parameters.append({
            "domain": container_artifact_item[0],
            "context": {'artifact_id': container_artifact_item[1]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("domain reputation", parameters=parameters, name="source_reputation", assets=["virustotal"], callback=join_check_reports)

    return


@phantom.playbook_block()
def virus_search(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("virus_search() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.fileHash","artifact:*.id"])

    parameters = []

    # build parameters list for 'virus_search' call
    for container_artifact_item in container_artifact_data:
        parameters.append({
            "hash": container_artifact_item[0],
            "context": {'artifact_id': container_artifact_item[1]},
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("file reputation", parameters=parameters, name="virus_search", assets=["virustotal"], callback=join_check_reports)

    return


@phantom.playbook_block()
def join_check_reports(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_check_reports() called")

    if phantom.completed(action_names=["locate_source", "source_reputation", "virus_search"]):
        # call connected block "check_reports"
        check_reports(container=container, handle=handle)

    return


@phantom.playbook_block()
def check_reports(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("check_reports() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="or",
        conditions=[
            ["source_reputation:action_result.summary.malicious", ">", 0],
            ["virus_search:action_result.summary.malicious", ">", 0]
        ],
        conditions_dps=[
            ["source_reputation:action_result.summary.malicious", ">", 0],
            ["virus_search:action_result.summary.malicious", ">", 0]
        ],
        name="check_reports:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        notify_soc_management(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def notify_soc_management(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("notify_soc_management() called")

    # set approver and message variables for phantom.prompt call

    user = None
    role = "Automation Engineer"
    message = """A potentially malicious file download has been detected on a local server with IP address {0}."""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.destinationAddress"
    ]

    # responses
    response_types = [
        {
            "prompt": "Notify SOC management?",
            "options": {
                "type": "list",
                "required": True,
                "choices": [
                    "Yes",
                    "No"
                ],
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="notify_soc_management", parameters=parameters, response_types=response_types)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    return