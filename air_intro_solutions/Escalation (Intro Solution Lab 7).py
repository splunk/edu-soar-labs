"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'update_finding_or_investigation_1' block
    update_finding_or_investigation_1(container=container)

    return

@phantom.playbook_block()
def update_finding_or_investigation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("update_finding_or_investigation_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])
    playbook_input_note_title = phantom.collect2(container=container, datapath=["playbook_input:note_title"])
    playbook_input_note_body = phantom.collect2(container=container, datapath=["playbook_input:note_body"])

    parameters = []

    # build parameters list for 'update_finding_or_investigation_1' call
    for finding_data_item in finding_data:
        for playbook_input_note_title_item in playbook_input_note_title:
            for playbook_input_note_body_item in playbook_input_note_body:
                if finding_data_item[0] is not None:
                    parameters.append({
                        "id": finding_data_item[0],
                        "urgency": "High",
                        "incident_note": {
                            "title": playbook_input_note_title_item[0],
                            "content": playbook_input_note_body_item[0],
                        },
                    })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("update finding or investigation", parameters=parameters, name="update_finding_or_investigation_1", assets=["builtin_mc_connector"])

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