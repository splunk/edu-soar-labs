"""

"""


import phantom.rules as phantom
import json
from datetime import datetime, timedelta


################################################################################
## Global Custom Code Start
################################################################################


def result_csv(result_list):
    simple_list = []
    for item in result_list:
        simple_list.append(item[0])
    dedup = list(dict.fromkeys(simple_list))
    return ", ".join(dedup)

################################################################################
## Global Custom Code End
################################################################################

@phantom.playbook_block()
def on_start(container):
    phantom.debug('on_start() called')

    # call 'list_finding_fields_1' block
    list_finding_fields_1(container=container)

    return

@phantom.playbook_block()
def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("geolocate_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    list_finding_fields_1__result = phantom.collect2(container=container, datapath=["list_finding_fields_1:custom_function_result.data.output"])

    parameters = []

    # build parameters list for 'geolocate_ip_1' call
    for list_finding_fields_1__result_item in list_finding_fields_1__result:
        if list_finding_fields_1__result_item[0] is not None:
            parameters.append({
                "ip": list_finding_fields_1__result_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("geolocate ip", parameters=parameters, name="geolocate_ip_1", assets=["maxmind"], callback=result_list)

    return


@phantom.playbook_block()
def list_finding_fields_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("list_finding_fields_1() called")

    finding_data = phantom.collect2(container=container, datapath=["finding:consolidated_findings.destinationAddress"])

    parameters = []

    # build parameters list for 'list_finding_fields_1' call
    for finding_data_item in finding_data:
        parameters.append({
            "input_list": finding_data_item[0],
        })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.custom_function(custom_function="local/list_finding_fields", parameters=parameters, name="list_finding_fields_1", callback=geolocate_ip_1)

    return


@phantom.playbook_block()
def set_custom_fields_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_custom_fields_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    finding_data = phantom.collect2(container=container, datapath=["finding:id"])
    result_list__result_list = json.loads(_ if (_ := phantom.get_run_data(key="result_list:result_list")) != "" else "null")  # pylint: disable=used-before-assignment

    parameters = []

    # build parameters list for 'set_custom_fields_1' call
    for finding_data_item in finding_data:
        if finding_data_item[0] is not None:
            parameters.append({
                "incident_id": finding_data_item[0],
                "pairs": [
                    { "name": "Datacenter", "value": result_list__result_list },
                ],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug(parameters)

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("set custom fields", parameters=parameters, name="set_custom_fields_1", assets=["builtin_mc_connector"])

    return


@phantom.playbook_block()
def result_list(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("result_list() called")

    geolocate_ip_1_result_data = phantom.collect2(container=container, datapath=["geolocate_ip_1:action_result.data.*.continent_name"], action_results=results)

    geolocate_ip_1_result_item_0 = [item[0] for item in geolocate_ip_1_result_data]

    result_list__result_list = None

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    phantom.debug(geolocate_ip_1_result_data )
    result_list__result_list = result_csv(geolocate_ip_1_result_data)
    phantom.debug(result_list__result_list)
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.save_block_result(key="result_list__inputs:0:geolocate_ip_1:action_result.data.*.continent_name", value=json.dumps(geolocate_ip_1_result_item_0))

    phantom.save_block_result(key="result_list:result_list", value=json.dumps(result_list__result_list))

    phantom.save_block_result(key="result_list_called", value="True")

    set_custom_fields_1(container=container)

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