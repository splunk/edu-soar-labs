"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'source_reputation' block
    source_reputation(container=container)
    # call 'locate_source' block
    locate_source(container=container)
    # call 'virus_search' block
    virus_search(container=container)
    # call 'log_file_hash' block
    log_file_hash(container=container)

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

    phantom.act("geolocate ip", parameters=parameters, name="locate_source", assets=["maxmind"], callback=join_check_positives)

    return


@phantom.playbook_block()
def source_reputation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("source_reputation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.sourceDnsDomain","artifact:*.id"])

    parameters = []

    # build parameters list for 'source_reputation' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
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

    phantom.act("domain reputation", parameters=parameters, name="source_reputation", assets=["virustotal"], callback=join_check_positives)

    return


@phantom.playbook_block()
def virus_search(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("virus_search() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.fileHash","artifact:*.id"])

    parameters = []

    # build parameters list for 'virus_search' call
    for container_artifact_item in container_artifact_data:
        if container_artifact_item[0] is not None:
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

    phantom.act("file reputation", parameters=parameters, name="virus_search", assets=["virustotal"], callback=join_check_positives)

    return


@phantom.playbook_block()
def join_check_positives(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_check_positives() called")

    if phantom.completed(action_names=["locate_source", "source_reputation", "virus_search"], playbook_names=["log_file_hash"]):
        # call connected block "check_positives"
        check_positives(container=container, handle=handle)

    return


@phantom.playbook_block()
def check_positives(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("check_positives() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        logical_operator="or",
        conditions=[
            ["virus_search:action_result.summary.malicious", ">", 0],
            ["source_reputation:action_result.summary.malicious", ">", 0]
        ],
        conditions_dps=[
            ["virus_search:action_result.summary.malicious", ">", 0],
            ["source_reputation:action_result.summary.malicious", ">", 0]
        ],
        name="check_positives:condition_1",
        delimiter=",")

    # call connected blocks if condition 1 matched
    if found_match_1:
        filter_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    add_comment_set_status_5(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def notify_soc_management(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("notify_soc_management() called")

    # set approver and message variables for phantom.prompt call

    user = None
    role = "Automation Engineer"
    message = """A potentially malicious file download has been detected on a local server with IP address {0}. Notify IT team?"""

    # parameter list for template variable replacement
    parameters = [
        "artifact:*.cef.destinationAddress"
    ]

    # responses
    response_types = [
        {
            "prompt": "Notify SOC Management?",
            "options": {
                "type": "list",
                "required": True,
                "choices": [
                    "Yes",
                    "No"
                ],
            },
        },
        {
            "prompt": "Reason",
            "options": {
                "type": "message",
                "required": True,
            },
        }
    ]

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="notify_soc_management", parameters=parameters, response_types=response_types, callback=decision_2, drop_none=False)

    return


@phantom.playbook_block()
def playbook_solution__escalation_lab_6_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_solution__escalation_lab_6_1() called")

    notify_soc_management_result_data = phantom.collect2(container=container, datapath=["notify_soc_management:action_result.summary.responses.1"], action_results=results)

    notify_soc_management_summary_responses_1 = [item[0] for item in notify_soc_management_result_data]

    inputs = {
        "escalation_reason": notify_soc_management_summary_responses_1,
        "hash_history": [],
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/Solution: Escalation Lab 6", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/Solution: Escalation Lab 6", container=container, inputs=inputs)

    return


@phantom.playbook_block()
def pin_add_comment_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("pin_add_comment_3() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.pin(container=container, message="xxx")
    phantom.comment(container=container, comment="xxx")

    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["notify_soc_management:action_result.summary.responses.0", "==", "Yes"]
        ],
        conditions_dps=[
            ["notify_soc_management:action_result.summary.responses.0", "==", "Yes"]
        ],
        name="decision_2:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        playbook_solution__escalation_lab_6_1(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'elif' condition 2
    found_match_2 = phantom.decision(
        container=container,
        conditions=[
            ["notify_soc_management:action_result.status", "!=", "success"]
        ],
        conditions_dps=[
            ["notify_soc_management:action_result.status", "!=", "success"]
        ],
        name="decision_2:condition_2",
        delimiter=None)

    # call connected blocks if condition 2 matched
    if found_match_2:
        pin_add_comment_3(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 3
    add_comment_set_owner_set_status_4(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def add_comment_set_owner_set_status_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_set_owner_set_status_4() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="boo")
    phantom.set_owner(container=container, role="Incident Commander")
    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def add_comment_set_status_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_set_status_5() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="xxx")
    phantom.set_status(container=container, status="closed")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("filter_1() called")

    # collect filtered artifact ids and results for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        conditions=[
            ["locate_source:action_result.data.*.country_name", "in", "custom_list:Banned Countries"]
        ],
        conditions_dps=[
            ["locate_source:action_result.data.*.country_name", "in", "custom_list:Banned Countries"]
        ],
        name="filter_1:condition_1",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        notify_soc_management(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids and results for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        conditions=[
            ["locate_source:action_result.data.*.country_name", "not in", "custom_list:Banned Countries"]
        ],
        conditions_dps=[
            ["locate_source:action_result.data.*.country_name", "not in", "custom_list:Banned Countries"]
        ],
        name="filter_1:condition_2",
        delimiter=None)

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        add_comment_set_owner_set_severity_6(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return


@phantom.playbook_block()
def add_comment_set_owner_set_severity_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_set_owner_set_severity_6() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="Malicious content from low risk source")
    phantom.set_owner(container=container, role="Incident Commander")
    phantom.set_severity(container=container, severity="low")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def log_file_hash(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("log_file_hash() called")

    inputs = {
        "hash": [],
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "local/Solution: Log File Hashes", returns the playbook_run_id
    playbook_run_id = phantom.playbook("local/Solution: Log File Hashes", container=container, name="log_file_hash", callback=join_check_positives, inputs=inputs)

    return


@phantom.playbook_block()
def on_finish(container, summary):
    phantom.debug("on_finish() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # This function is called after all actions are completed.
    # summary of all the action and/or all details of actions
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    ################################################################################
    ## Custom Code End
    ################################################################################

    return