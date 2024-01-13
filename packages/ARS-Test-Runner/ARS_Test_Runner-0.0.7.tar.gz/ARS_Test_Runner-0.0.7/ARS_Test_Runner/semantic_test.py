"""Test ARS et all."""
import json
import os
import ssl
import httpx
import asyncio
import requests
import datetime
import logging
from copy import deepcopy
import datetime
import argparse
from typing import Any, Dict, List
# We really shouldn't be doing this, but just for now...
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
logging.basicConfig(filename="test_ars.log", level=logging.DEBUG)

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
parser = argparse.ArgumentParser(description='Semantic Smoke Test')
parser.add_argument('--env', help='environment to run the analysis on', default='ci')
parser.add_argument('--predicate',help='predicate',default='treats', type=str)
parser.add_argument('--runner_setting', help='creative mode indicator',nargs="*", type=str )
parser.add_argument('--expected_output', help="[TopAnswer'|'Acceptable'|'BadButForgivable'|'NeverShow']",nargs="*", type=str)
parser.add_argument('--input_curie', help='Input Curie', type=str)
parser.add_argument('--output_curie', help='output Curie', nargs="*", type=str)

env_spec = {
    'dev': 'ars-dev',
    'ci': 'ars.ci',
    'test': 'ars.test',
    'prod': 'ars-prod'
}

def get_safe(element, *keys):
    """
    :param element: JSON to be processed
    :param keys: list of keys in order to be traversed. e.g. "fields","data","message","results
    :return: the value of the terminal key if present or None if not
    """
    if element is None:
        return None
    _element = element
    for key in keys:
        try:
            _element = _element[key]
            if _element is None:
                return None
            if key == keys[-1]:
                return _element
        except KeyError:
            return None
    return None

def generate_message(predicate: str, creative: bool ,input_curie: str):
    """Create a message to send to Translator services"""

    template_dir = BASE_PATH + "/templates"
    predicate_list = ['treats','treats_creative','upregulate', 'downregulate']

    if predicate in predicate_list:
        if creative:
            template_name = predicate+'_creative'
        else:
            template_name = predicate
        with open(template_dir+f'/{template_name}.json') as f:
            template = json.load(f)
            # Fill message template with CURIEs
            query = deepcopy(template)
            nodes = get_safe(query, "message", "query_graph", "nodes")
            for node_val in nodes.values():
                if 'ids' in node_val:
                    node_val['ids'].append(input_curie)
    else:
        logging.error("Unknown Query type")

    return query

async def call_ars(payload: Dict[str,any],ARS_URL: str):
    url = ARS_URL+"submit"
    logging.debug("call_ars")

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            url,
            json=payload,
            timeout=60,
        )
    response.raise_for_status()
    return response.json()

async def test_must_have_curie(ARS_URL: str, predicate: str,runner_setting, expected_output: str, input_curie: str, output_curie: List[str], output_filename: str):
    """" Send Concurrent async queries to ARS and get pass/fail report back  """

    if runner_setting == []:
        creative = False
    elif "inferred" in runner_setting:
        creative = True
    logging.debug("Generating query message for %s in creative %s mode" % (input_curie, creative))
    message = generate_message(predicate, creative, input_curie)
    logging.debug("query= " + json.dumps(message, indent=4, sort_keys=True))

    children, merged_data, parent_pk, merged_pk = await get_children(message, ARS_URL)
    report_card = await ARS_semantic_analysis(children, parent_pk, output_curie, expected_output, merged_pk, merged_data)

    # with open(output_filename, "w") as f:
    #     json.dump(report_card, f, indent=4)

    return report_card

async def ARS_semantic_analysis(children: List[List], pk: str, output_curie: List[str], expected_output: str, merged_pk: str, merged_data: Dict[str,any]):
    """" function to perform pass fail analysis on individual ARA's results """
    report_card={}
    report_card['pks']={}
    report_card['pks']['parent_pk'] = pk
    if merged_data is not None:
        report_card['pks']['merged_pk'] = merged_pk

    report_card['results'] = []
    #report_card[pk]['merged_data'] = merged_data
    for idx, out_curie in enumerate(output_curie):
        if not out_curie:
            empty_mesg = {"error": "No output id is provided"}
            report_card['results'].append(empty_mesg)
        else:
            expect_output = expected_output[idx]
            report={}
            #report[out_curie]={}
            for data in children:
                infores = data[0]
                agent = infores.split('-')[1]
                child = data[1]
                child_pk = data[2]
                results = get_safe(child, "fields", "data", "message", "results")
                if results is not None and infores.startswith('ara-'):
                    report_card['pks'][agent] = child_pk
                    report = await pass_fail_analysis(report, agent, results, out_curie, expect_output)
            #adding the merged data to the report
            if merged_data is not None:
                agent='ars'
                ARS_results = get_safe(merged_data, "fields", "data", "message", "results")
                report = await pass_fail_analysis(report, agent, ARS_results, out_curie, expect_output)
            report_card['results'].append(report)
    return report_card

async def pass_fail_analysis(report: Dict[str,any], agent: str, results: List[Dict[str,any]], out_curie: str, expect_output: str):
    """" function to run pass fail analysis on individual results"""
    #get the top_n result's ids
    try:
        res_sort = sorted(results, key=lambda x: x['normalized_score'], reverse=True)
        all_ids=[]
        for res in res_sort:
            for res_node, res_value in res["node_bindings"].items():
                for val in res_value:
                    ids = str(val["id"])
                    if ids not in all_ids:
                        all_ids.append(ids)
        total_num_res = len(all_ids)
        if expect_output == 'TopAnswer':
            if total_num_res <= 10:
                n_perc_res = res_sort[::]
            else:
                n_perc_res = res_sort[0:int(len(res_sort) * (float(10) / 100))]
        elif expect_output == 'Acceptable':
            n_perc_res = res_sort[0:int(len(res_sort) * (float(50) / 100))]
        elif expect_output == 'BadButForgivable':
            n_perc_res = res_sort[int(len(res_sort) * (float(50) / 100)):]
        elif expect_output == 'NeverShow':
            n_perc_res = res_sort
        else:
            logging.error("you have indicated a wrong category for expected output")
        n_perc_ids=[]
        for res in n_perc_res:
            for res_value in res["node_bindings"].values():
                for val in res_value:
                    ids=str(val["id"])
                    if ids not in n_perc_ids:
                        n_perc_ids.append(ids)

        if expect_output in ['TopAnswer', 'Acceptable','BadButForgivable']:
            if out_curie in n_perc_ids:
                report[agent] = 'PASSED'
            else:
                report[agent] = 'FAILED'
        elif expect_output == 'NeverShow':
            if out_curie in n_perc_ids:
                report[agent] = 'FAILED'
            else:
                report[agent] = 'PASSED'

        #case where the drug not even in the results
        if out_curie not in all_ids:
            if expect_output in ['TopAnswer', 'Acceptable']:
                report[agent] = 'FAILED'
            elif expect_output in ['NeverShow','BadButForgivable']:
                report[agent] = 'PASSED'

    except Exception as e:
        report[agent] = f'error: {type(e), str(e)}'

    return report

async def get_children(query: Dict[str,Any], ARS_URL: str, timeout=None):
    logging.debug("get_children")
    children = []
    response = await call_ars(query, ARS_URL)
    await asyncio.sleep(300)
    parent_pk = response["pk"]
    logging.debug("parent_pk for query {}  is {} ".format(query, str(parent_pk)))
    url = ARS_URL + "messages/" + parent_pk + "?trace=y"
    if timeout is None:
        timeout = 60
    async with httpx.AsyncClient(verify=False) as client:
        r = await client.get(
            url,
            timeout=60,
        )
    data = r.json()
    for child in data["children"]:
        agent = child["actor"]["agent"]
        childPk = child["message"]
        logging.debug("---Checking child for " + agent + ", pk=" + parent_pk)
        childData = await get_child(childPk, ARS_URL)
        if childData is None:
            pass
        else:
            # append each child with its results
            children.append([agent, childData, childPk])

    #getting merged data
    merged_pk = data['merged_version']
    merged_data = await get_merged_data(ARS_URL, merged_pk, time_out=120)

    return children, merged_data, parent_pk, merged_pk

async def get_merged_data(ARS_URL: str, merged_pk: str, time_out):
    """ function to retrieve completed merged data """
    wait_time=10
    merged_url = ARS_URL + "messages/" + merged_pk
    async with httpx.AsyncClient(verify=False) as client:
        rr = await client.get(
            merged_url,
            timeout=60,
        )
    rr.raise_for_status()
    merged_data = rr.json()
    status = get_safe(merged_data, "fields", "status")
    #print(f'the merged data status is {status}')
    if status is not None:
        if status == "Done":
            #print(f'merged_data status is Done, returning')
            return merged_data
        elif status == 'Running':
            #print(f'merged_data still running, sleep for 10 sec and continue')
            if time_out > 0:
                logging.debug(
                    "Query merged response is still running\n"
                    + "Wait time remaining is now "
                    + str(time_out)
                    + "\n"
                    + "What we have so far is: "
                    + json.dumps(merged_data, indent=4, sort_keys=True)
                )
                await asyncio.sleep(wait_time)
                remaining_time = time_out - wait_time
                #print(f'going to try getting merged_data for remaining time of {remaining_time}')
                return await get_merged_data(ARS_URL,merged_pk, remaining_time)
        else:
            #print(f"even after timeout {merged_pk} is still Running, Returning None")
            logging.debug("even after timeout" +merged_pk+ "is still Running") # sorry bud, time's up
            return None

async def get_child(pk: str, ARS_URL: str, timeout=60):
    logging.debug("get_child(" + pk + ")")
    wait_time = 10  # amount of seconds to wait between checks for a Running query result
    url = ARS_URL + "messages/" + pk
    async with httpx.AsyncClient(verify=False) as client:
        child_response = await client.get(
            url,
            timeout=60.0
        )
    data = child_response.json()
    status = get_safe(data, "fields", "status")
    result_count = get_safe(data, "fields", "result_count")
    if status is not None:
        if status == "Done" and result_count is not None:
            if  result_count > 0:
                logging.debug("get_child for " +pk+ "returned"+ str(result_count )+"results")
                return data
            elif result_count == 0:
                logging.debug("get_child for " +pk+ "returned 0 results")
                return None
        elif status == "Running":
            if timeout > 0:
                logging.debug(
                    "Query response is still running\n"
                    + "Wait time remaining is now "
                    + str(timeout)
                    + "\n"
                    + "What we have so far is: "
                    + json.dumps(data, indent=4, sort_keys=True)
                )
                await asyncio.sleep(wait_time)
                return await get_child(pk, ARS_URL, timeout - wait_time)
            else:
                logging.debug("even after timeout" +pk+ "is still Running") # sorry bud, time's up
                return None
        else:
            # status must be some manner of error
            logging.debug(
                "Error status found in get_child for "
                + pk
                + "\n"
                + "Status is "
                + status
                + "\n"
                + json.dumps(data, indent=4, sort_keys=True)
            )
            return None
    else:
        # Should I be throwing an exception here instead?
        logging.error("Status in get_child for " + pk + " was no retrievable")
        logging.error(json.dumps(data, indent=4, sort_keys=True))
    # We shouldn't get here
    logging.error("Error in get_child for \n" + pk + "\n No child retrievable")
    return None


async def run_semantic_test(env: str, predicate: str, runner_setting: List[str], expected_output: str, input_curie: List[str], output_curie: List[str]):

    ars_env = env_spec[env]
    ARS_URL = f'https://{ars_env}.transltr.io/ars/api/'
    timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    output_filename = f"ARS_smoke_test_{timestamp}.json"

    report_card = await test_must_have_curie(ARS_URL, predicate, runner_setting, expected_output, input_curie, output_curie,output_filename)
    return report_card

if __name__ == "__main__":

    args = parser.parse_args()
    env = getattr(args, "env")
    predicate = getattr(args, "predicate")
    runner_setting = getattr(args,"runner_setting")
    expected_output = getattr(args, "expected_output")
    input_curie = getattr(args, "input_curie")
    output_curie = getattr(args, "output_curie")

    current_time = datetime.datetime.now()
    formatted_start_time = current_time.strftime('%H:%M:%S')
    print(f"started performing ARS_Test pass/fail Analysis at {formatted_start_time}")
    print(asyncio.run(run_semantic_test(env,predicate, runner_setting, expected_output, input_curie, output_curie)))
    endtime = datetime.datetime.now()
    formatted_end_time = endtime.strftime('%H:%M:%S')
    print(f"finished running the analysis at {formatted_end_time}")
