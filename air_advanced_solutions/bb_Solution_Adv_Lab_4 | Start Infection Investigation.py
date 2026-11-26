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
        "investigation_search_term": "Infection on host",
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
        new_investigation(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    existing_investigation(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def new_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("new_investigation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'new_investigation' call
    for finding_data_item in finding_data:
        parameters.append({
            "name": "Infection on host",
            "status": "In Progress",
            "finding_ids": [
                finding_data_item[0],
            ],
            "inherit_fields": 0,
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.save_block_result(key="investigation_state", value="new")

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("start investigations", parameters=parameters, name="new_investigation", assets=["builtin_mc_connector"], callback=join_select_id)

    return


@phantom.playbook_block()
def existing_investigation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("existing_investigation() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    find_open_investigation_result_data = phantom.collect2(container=container, datapath=["find_open_investigation:action_result.data.*.investigation_id","find_open_investigation:action_result.parameter.context.artifact_id"], action_results=results)
    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'existing_investigation' call
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

    phantom.act("add finding to investigation", parameters=parameters, name="existing_investigation", assets=["builtin_mc_connector"], callback=join_select_id)

    return


@phantom.playbook_block()
def add_finding_or_investigation_note_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_finding_or_investigation_note_6() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    playbook_input_note_title = phantom.collect2(container=container, datapath=["playbook_input:note_title"])
    playbook_input_note_body = phantom.collect2(container=container, datapath=["playbook_input:note_body"])
    select_id__id = json.loads(_ if (_ := phantom.get_run_data(key="select_id:id")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'add_finding_or_investigation_note_6' call
    for playbook_input_note_title_item in playbook_input_note_title:
        for playbook_input_note_body_item in playbook_input_note_body:
            if select_id__id is not None and playbook_input_note_body_item[0] is not None:
                parameters.append({
                    "id": select_id__id,
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
def join_select_id(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("join_select_id() called")

    # if the joined function has already been called, do nothing
    if phantom.get_run_data(key="join_select_id_called"):
        return

    # save the state that the joined function has now been called
    phantom.save_block_result(key="join_select_id_called", value="select_id")

    # call connected block "select_id"
    select_id(container=container, handle=handle)

    return


@phantom.playbook_block()
def select_id(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("select_id() called")

    select_id__id = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    id_result = None
    state = phantom.get_block_result("investigation_state")

    if state == "new":
        result_data = phantom.collect2(
            container=container, 
            datapath=["new_investigation:action_result.data.*.id"], 
            action_results=results
        )
    elif state == "add":
        result_data = phantom.collect2(
            container=container, 
            datapath=["existing_investigation:action_result.data.*.id"], 
            action_results=results
        )
    else: 
        phantom.debug("no match")
        result_data = []

    id_result = [item[0] for item in result_data]
    if id_result:
        select_id__id = id_result[0]

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_block_result(key="select_id:id", value=json.dumps(select_id__id))

    phantom.save_block_result(key="select_id_called", value="True")

    add_finding_or_investigation_note_6(container=container)

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