"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'request_finding_evaluation' block
    request_finding_evaluation(container=container)

    return

@phantom.playbook_block()
def request_finding_evaluation(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("request_finding_evaluation() called")

    # set approver and message variables for phantom.prompt call

    user = "admin"
    role = None
    message = """Please examine finding and set the appropriate urgency and owner """

    # parameter list for template variable replacement
    parameters = []

    phantom.prompt2(container=container, user=user, role=role, message=message, respond_in_mins=30, name="request_finding_evaluation", parameters=parameters, callback=refresh_finding_or_investigation_2)

    return


@phantom.playbook_block()
def format_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("format_1() called")

    template = """Responder comment:\n{0}\n\nNew finding Urgency: {1}\nNew finding Owner: {2}\nNew status: {3}\n"""

    # parameter list for template variable replacement
    parameters = [
        "request_finding_evaluation:action_result.summary.responses.0",
        "refresh_finding_or_investigation_2:action_result.data.*.data.urgency",
        "refresh_finding_or_investigation_2:action_result.data.*.data.owner",
        "finding:status"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="format_1")

    add_finding_or_investigation_note_1(container=container)

    return


@phantom.playbook_block()
def add_finding_or_investigation_note_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_finding_or_investigation_note_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])
    format_1 = phantom.get_format_data(name="format_1")

    parameters = []

    # build parameters list for 'add_finding_or_investigation_note_1' call
    for finding_data_item in finding_data:
        if finding_data_item[0] is not None and format_1 is not None:
            parameters.append({
                "id": finding_data_item[0],
                "title": "Responder update",
                "content": format_1,
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("add finding or investigation note", parameters=parameters, name="add_finding_or_investigation_note_1", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def refresh_finding_or_investigation_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("refresh_finding_or_investigation_2() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'refresh_finding_or_investigation_2' call
    for finding_data_item in finding_data:
        if finding_data_item[0] is not None:
            parameters.append({
                "id": finding_data_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("refresh finding or investigation", parameters=parameters, name="refresh_finding_or_investigation_2", assets=["builtin_mc_connector"], callback=format_1)

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