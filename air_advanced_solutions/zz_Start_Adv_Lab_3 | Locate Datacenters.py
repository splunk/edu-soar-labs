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

    # call 'list_demux_1' block
    list_demux_1(container=container)

    return

@phantom.playbook_block()
def geolocate_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("geolocate_ip_1() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    list_demux_1__result = phantom.collect2(container=container, datapath=["list_demux_1:custom_function_result.data.output"])

    parameters = []

    # build parameters list for 'geolocate_ip_1' call
    for list_demux_1__result_item in list_demux_1__result:
        if list_demux_1__result_item[0] is not None:
            parameters.append({
                "ip": list_demux_1__result_item[0],
            })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...

    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("geolocate ip", parameters=parameters, name="geolocate_ip_1", assets=["maxmind"], callback=set_custom_fields_3)

    return


@phantom.playbook_block()
def list_demux_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("list_demux_1() called")

    finding_data = phantom.collect2(container=container, datapath=["finding:consolidated_findings.destinationAddress"])

    parameters = []

    # build parameters list for 'list_demux_1' call
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

    phantom.custom_function(custom_function="community/list_demux", parameters=parameters, name="list_demux_1", callback=geolocate_ip_1)

    return


@phantom.playbook_block()
def set_custom_fields_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None, custom_function=None, loop_state_json=None, **kwargs):
    phantom.debug("set_custom_fields_3() called")

    # phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))

    geolocate_ip_1_result_data = phantom.collect2(container=container, datapath=["geolocate_ip_1:action_result.data.*.continent_name","geolocate_ip_1:action_result.parameter.context.artifact_id"], action_results=results)
    finding_data = phantom.collect2(container=container, datapath=["finding:id"])

    parameters = []

    # build parameters list for 'set_custom_fields_3' call
    for geolocate_ip_1_result_item in geolocate_ip_1_result_data:
        for finding_data_item in finding_data:
            if finding_data_item[0] is not None:
                parameters.append({
                    "pairs": [
                        { "name": "Datacenters", "value": geolocate_ip_1_result_item[0] },
                    ],
                    "incident_id": finding_data_item[0],
                })

    ################################################################################
    ## Custom Code Start
    ################################################################################

    # Write your custom code here...
    
    val = result_csv(geolocate_ip_1_result_data)
    parameters = []
    parameters.append({"pairs": [{"name": "Datacenters", "value": val },
                       ],
                       "incident_id": finding_data_item[0],
                      })
    
    
    ################################################################################
    ## Custom Code End
    ################################################################################

    phantom.act("set custom fields", parameters=parameters, name="set_custom_fields_3", assets=["builtin_mc_connector"])

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