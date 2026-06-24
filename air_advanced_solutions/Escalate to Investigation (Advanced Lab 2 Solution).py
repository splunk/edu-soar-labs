"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'find_open_investigation' block
    find_open_investigation(container=container)

    return

@phantom.playbook_block()
def find_open_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("find_open_investigation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    parameters = []

    parameters.append({
        "status": "In Progress",
        "investigation_search_term": "infection on host",
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("list investigations", parameters=parameters, name="find_open_investigation", assets=["builtin_mc_connector"], callback=decision_1)

    return


@phantom.playbook_block()
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["find_open_investigation:action_result.data.*.name", "is None"]
        ],
        conditions_dps=[
            ["find_open_investigation:action_result.data.*.name", "is None"]
        ],
        name="decision_1:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        start_investigations_2(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    add_finding_to_investigation_4(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def start_investigations_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("start_investigations_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'start_investigations_2' call
    for finding_data_item in finding_data:
        parameters.append({
            "name": "Infection on host",
            "status": "In Progress",
            "finding_ids": [
                finding_data_item[0],
            ],
            "inherit_fields": "f",
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.save_block_result(key="investigation_state", value="new")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("start investigations", parameters=parameters, name="start_investigations_2", assets=["builtin_mc_connector"], callback=join_list_merge_1)

    return


@phantom.playbook_block()
def add_finding_to_investigation_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_finding_to_investigation_4() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    find_open_investigation_result_data = phantom.collect2(container=container, datapath=["find_open_investigation:action_result.data.*.investigation_id","find_open_investigation:action_result.parameter.context.artifact_id"], action_results=results)
    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'add_finding_to_investigation_4' call
    for find_open_investigation_result_item in find_open_investigation_result_data:
        for finding_data_item in finding_data:
            if find_open_investigation_result_item[0] is not None:
                parameters.append({
                    "id": find_open_investigation_result_item[0],
                    "incident_ids": [
                        finding_data_item[0],
                    ],
                    "inherit_fields": 0,
                    "context": {'artifact_id': find_open_investigation_result_item[1]},
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.save_block_result(key="investigation_state", value="add")
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add finding to investigation", parameters=parameters, name="add_finding_to_investigation_4", assets=["builtin_mc_connector"], callback=join_list_merge_1)

    return


@phantom.playbook_block()
def add_finding_or_investigation_note_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_finding_or_investigation_note_6() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    list_merge_1__result = phantom.collect2(container=container, datapath=["list_merge_1:custom_function_result.data.item"])
    playbook_input_note_title = phantom.collect2(container=container, datapath=["playbook_input:note_title"])
    playbook_input_note_body = phantom.collect2(container=container, datapath=["playbook_input:note_body"])

    parameters = []

    # build parameters list for 'add_finding_or_investigation_note_6' call
    for list_merge_1__result_item in list_merge_1__result:
        for playbook_input_note_title_item in playbook_input_note_title:
            for playbook_input_note_body_item in playbook_input_note_body:
                if list_merge_1__result_item[0] is not None and playbook_input_note_body_item[0] is not None:
                    parameters.append({
                        "id": list_merge_1__result_item[0],
                        "title": playbook_input_note_title_item[0],
                        "content": playbook_input_note_body_item[0],
                    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug(parameters)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add finding or investigation note", parameters=parameters, name="add_finding_or_investigation_note_6", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def join_list_merge_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_list_merge_1() called")

    if phantom.completed(action_names=["start_investigations_2", "add_finding_to_investigation_4"]):
        # call connected block "list_merge_1"
        list_merge_1(container=container, handle=handle)

    return


@phantom.playbook_block()
def list_merge_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("list_merge_1() called")

    start_investigations_2_result_data = phantom.collect2(container=container, datapath=["start_investigations_2:action_result.data.*.id","start_investigations_2:action_result.parameter.context.artifact_id"], action_results=results)
    add_finding_to_investigation_4_result_data = phantom.collect2(container=container, datapath=["add_finding_to_investigation_4:action_result.data.*.id","add_finding_to_investigation_4:action_result.parameter.context.artifact_id"], action_results=results)

    start_investigations_2_result_item_0 = [item[0] for item in start_investigations_2_result_data]
    add_finding_to_investigation_4_result_item_0 = [item[0] for item in add_finding_to_investigation_4_result_data]

    parameters = []

    parameters.append({
        "input_1": start_investigations_2_result_item_0,
        "input_2": add_finding_to_investigation_4_result_item_0,
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

    phantom.custom_function(custom_function="community/list_merge", parameters=parameters, name="list_merge_1", callback=add_finding_or_investigation_note_6)

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