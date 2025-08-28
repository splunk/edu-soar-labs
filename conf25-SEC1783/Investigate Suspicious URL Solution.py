"""
This is the solution playbook for lab 6. This playbook uses both input playbooks you created in lab 3 and 5.  It also uses a prompt block to let the analyst choose to add the url to the http_intel list.
"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'playbook_string_split_extract_url_1' block
    playbook_string_split_extract_url_1(container=container)

    return

@phantom.playbook_block()
def playbook_lookup_url_in_es_http_intel_collection_solution_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_lookup_url_in_es_http_intel_collection_solution_1() called")

    playbook_string_split_extract_url_1_output_url = phantom.collect2(container=container, datapath=["playbook_string_split_extract_url_1:playbook_output:url"])

    playbook_string_split_extract_url_1_output_url_values = [item[0] for item in playbook_string_split_extract_url_1_output_url]

    inputs = {
        "url": playbook_string_split_extract_url_1_output_url_values,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "conf25/Lookup url in ES http_intel collection Solution", returns the playbook_run_id
    playbook_run_id = phantom.playbook("conf25/Lookup url in ES http_intel collection Solution", container=container, name="playbook_lookup_url_in_es_http_intel_collection_solution_1", callback=playbook_lookup_url_in_es_http_intel_collection_solution_1_callback, inputs=inputs)

    return


@phantom.playbook_block()
def playbook_lookup_url_in_es_http_intel_collection_solution_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_lookup_url_in_es_http_intel_collection_solution_1_callback() called")

    
    debug_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    decision_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def debug_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_1() called")

    playbook_lookup_url_in_es_http_intel_collection_solution_1_output_threat_key = phantom.collect2(container=container, datapath=["playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_output:threat_key"])

    playbook_lookup_url_in_es_http_intel_collection_solution_1_output_threat_key_values = [item[0] for item in playbook_lookup_url_in_es_http_intel_collection_solution_1_output_threat_key]

    parameters = []

    parameters.append({
        "input_1": playbook_lookup_url_in_es_http_intel_collection_solution_1_output_threat_key_values,
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
def decision_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_1() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_output:threat_key", "==", None]
        ],
        conditions_dps=[
            ["playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_output:threat_key", "==", None]
        ],
        name="decision_1:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        format_url_not_found_msg(action=action, success=success, container=container, results=results, handle=handle)
        return

    # check for 'else' condition 2
    format_warning_msg(action=action, success=success, container=container, results=results, handle=handle)

    return


@phantom.playbook_block()
def format_warning_msg(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_warning_msg() called")

    template = """WARNING! URL Found in http_intel threat list!!!\n\nURL: {0}\nThreat Key: {1}\nTime Created: {2}"""

    # parameter list for template variable replacement
    parameters = [
        "playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_input:url",
        "playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_output:threat_key",
        "playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_output:date_created"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_warning_msg")

    add_comment_3(container=container)

    return


@phantom.playbook_block()
def add_comment_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_3() called")

    format_warning_msg = phantom.get_format_data(name="format_warning_msg")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment=format_warning_msg)

    set_severity_5(container=container)

    return


@phantom.playbook_block()
def format_url_not_found_msg(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_url_not_found_msg() called")

    template = """URL not found in http_intel threat list.\n\nURL: {0}"""

    # parameter list for template variable replacement
    parameters = [
        "playbook_lookup_url_in_es_http_intel_collection_solution_1:playbook_input:url"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_url_not_found_msg")

    add_comment_4(container=container)

    return


@phantom.playbook_block()
def add_comment_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_4() called")

    format_url_not_found_msg = phantom.get_format_data(name="format_url_not_found_msg")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment=format_url_not_found_msg)

    ask_to_add_to_threat_list(container=container)

    return


@phantom.playbook_block()
def set_severity_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_severity_5() called")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.set_severity(container=container, severity="high")

    container = phantom.get_container(container.get('id', None))

    return


@phantom.playbook_block()
def ask_to_add_to_threat_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ask_to_add_to_threat_list() called")

    # set approver and message variables for phantom.prompt call

    user = None
    role = "Administrator"
    message = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "format_url_not_found_msg:formatted_data"
    ]

    # responses
    response_types = [
        {
            "prompt": "Would you like to add the URL to the http_intel threat list?",
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

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=5, name="ask_to_add_to_threat_list", parameters=parameters, response_types=response_types, callback=ask_to_add_to_threat_list_callback)

    return


@phantom.playbook_block()
def ask_to_add_to_threat_list_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("ask_to_add_to_threat_list_callback() called")

    
    decision_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    debug_from_prompt(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def decision_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("decision_2() called")

    # check for 'if' condition 1
    found_match_1 = phantom.decision(
        container=container,
        conditions=[
            ["ask_to_add_to_threat_list:action_result.summary.responses.0", "==", "Yes"]
        ],
        conditions_dps=[
            ["ask_to_add_to_threat_list:action_result.summary.responses.0", "==", "Yes"]
        ],
        name="decision_2:condition_1",
        delimiter=None)

    # call connected blocks if condition 1 matched
    if found_match_1:
        format_threat_key_value(action=action, success=success, container=container, results=results, handle=handle)
        return

    return


@phantom.playbook_block()
def playbook_create_record_for_http_intel_collection_solution_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_create_record_for_http_intel_collection_solution_1() called")

    playbook_string_split_extract_url_1_output_url = phantom.collect2(container=container, datapath=["playbook_string_split_extract_url_1:playbook_output:url"])
    format_threat_key_value = phantom.get_format_data(name="format_threat_key_value")
    format_time = phantom.get_format_data(name="format_time")

    playbook_string_split_extract_url_1_output_url_values = [item[0] for item in playbook_string_split_extract_url_1_output_url]

    inputs = {
        "url": playbook_string_split_extract_url_1_output_url_values,
        "threat_key": format_threat_key_value,
        "time": format_time,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "conf25/Create record for http_intel collection Solution", returns the playbook_run_id
    playbook_run_id = phantom.playbook("conf25/Create record for http_intel collection Solution", container=container, name="playbook_create_record_for_http_intel_collection_solution_1", callback=playbook_create_record_for_http_intel_collection_solution_1_callback, inputs=inputs)

    return


@phantom.playbook_block()
def playbook_create_record_for_http_intel_collection_solution_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_create_record_for_http_intel_collection_solution_1_callback() called")

    
    # Downstream End block cannot be called directly, since execution will call on_finish automatically.
    # Using placeholder callback function so child playbook is run synchronously.


    return


@phantom.playbook_block()
def format_threat_key_value(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_threat_key_value() called")

    template = """local intel"""

    # parameter list for template variable replacement
    parameters = []

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_threat_key_value")

    format_record_user_field(container=container)

    return


@phantom.playbook_block()
def format_record_user_field(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_record_user_field() called")

    template = """nobody"""

    # parameter list for template variable replacement
    parameters = []

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_record_user_field")

    datetime_modify_7(container=container)

    return


@phantom.playbook_block()
def debug_from_prompt(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_from_prompt() called")

    ask_to_add_to_threat_list_result_data = phantom.collect2(container=container, datapath=["ask_to_add_to_threat_list:action_result.summary.user","ask_to_add_to_threat_list:action_result.summary.answered_at","ask_to_add_to_threat_list:action_result.summary.sent_at","ask_to_add_to_threat_list:action_result.parameter.context.artifact_id"], action_results=results)

    ask_to_add_to_threat_list_summary_user = [item[0] for item in ask_to_add_to_threat_list_result_data]
    ask_to_add_to_threat_list_summary_answered_at = [item[1] for item in ask_to_add_to_threat_list_result_data]
    ask_to_add_to_threat_list_summary_sent_at = [item[2] for item in ask_to_add_to_threat_list_result_data]

    parameters = []

    parameters.append({
        "input_1": ask_to_add_to_threat_list_summary_user,
        "input_2": ask_to_add_to_threat_list_summary_answered_at,
        "input_3": ask_to_add_to_threat_list_summary_sent_at,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_from_prompt")

    return


@phantom.playbook_block()
def datetime_modify_7(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("datetime_modify_7() called")

    parameters = []

    parameters.append({
        "input_datetime": None,
        "amount_to_modify": None,
        "modification_unit": None,
        "input_format_string": None,
        "output_format_string": None,
    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="community/datetime_modify", parameters=parameters, name="datetime_modify_7", callback=datetime_modify_7_callback)

    return


@phantom.playbook_block()
def datetime_modify_7_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("datetime_modify_7_callback() called")

    
    debug_date_time(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)
    format_time(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=filtered_artifacts, filtered_results=filtered_results)


    return


@phantom.playbook_block()
def debug_date_time(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("debug_date_time() called")

    datetime_modify_7__result = phantom.collect2(container=container, datapath=["datetime_modify_7:custom_function_result.data.datetime_string","datetime_modify_7:custom_function_result.data.epoch_time","datetime_modify_7:custom_function_result.data.seconds_modified","datetime_modify_7:custom_function_result.success","datetime_modify_7:custom_function_result.message"])

    datetime_modify_7_data_datetime_string = [item[0] for item in datetime_modify_7__result]
    datetime_modify_7_data_epoch_time = [item[1] for item in datetime_modify_7__result]
    datetime_modify_7_data_seconds_modified = [item[2] for item in datetime_modify_7__result]
    datetime_modify_7_success = [item[3] for item in datetime_modify_7__result]
    datetime_modify_7_message = [item[4] for item in datetime_modify_7__result]

    parameters = []

    parameters.append({
        "input_1": datetime_modify_7_data_datetime_string,
        "input_2": datetime_modify_7_data_epoch_time,
        "input_3": datetime_modify_7_data_seconds_modified,
        "input_4": datetime_modify_7_success,
        "input_5": datetime_modify_7_message,
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

    phantom.custom_function(custom_function="community/debug", parameters=parameters, name="debug_date_time")

    return


@phantom.playbook_block()
def format_time(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_time() called")

    template = """{0}"""

    # parameter list for template variable replacement
    parameters = [
        "datetime_modify_7:custom_function_result.data.epoch_time"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_time")

    playbook_create_record_for_http_intel_collection_solution_1(container=container)

    return


@phantom.playbook_block()
def playbook_string_split_extract_url_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("playbook_string_split_extract_url_1() called")

    container_artifact_data = phantom.collect2(container=container, datapath=["artifact:*.cef.requestURL"])

    container_artifact_cef_item_0 = [item[0] for item in container_artifact_data]

    inputs = {
        "url": container_artifact_cef_item_0,
    }

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    # call playbook "conf25/String_split_extract_url", returns the playbook_run_id
    playbook_run_id = phantom.playbook("conf25/String_split_extract_url", container=container, name="playbook_string_split_extract_url_1", callback=playbook_lookup_url_in_es_http_intel_collection_solution_1, inputs=inputs)

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