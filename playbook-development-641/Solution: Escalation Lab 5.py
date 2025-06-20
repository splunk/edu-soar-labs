"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'compose_report' block
    compose_report(container=container)

    return

@phantom.playbook_block()
def compose_report(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("compose_report() called")

    template = """A file has been detected that has been determined to be potentially malicious. The event has been escalated. \n\n- **Case link**: {0}\n- **Event Name**: {1}\n- **Description**: {2}\n- **Source URL**: {3}\n- **Target Server IP**: {4}\n- **Suspicious File Pat**h: {5}\n- **Reason for promotion**: {6}\n"""

    # parameter list for template variable replacement
    parameters = [
        "container:url",
        "container:name",
        "container:description",
        "artifact:*.cef.sourceDnsDomain",
        "artifact:*.cef.destinationAddress",
        "artifact:*.cef.filePath",
        "playbook_input:escalation_reason"
    ]

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.format(container=container, template=template, parameters=parameters, name="compose_report", drop_none=True)

    add_comment_add_note_set_severity_set_status_1(container=container)

    return


@phantom.playbook_block()
def add_comment_add_note_set_severity_set_status_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("add_comment_add_note_set_severity_set_status_1() called")

    compose_report = phantom.get_format_data(name="compose_report")

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.comment(container=container, comment="Promoted to case")
    phantom.add_note(container=container, content=compose_report, note_format="markdown", note_type="general", title="Incident Report")
    phantom.set_severity(container=container, severity="high")
    phantom.set_status(container=container, status="open")

    container = phantom.get_container(container.get('id', None))

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