import os
import re
import json
import xml.etree.ElementTree as ET
from glob import glob
from datetime import datetime
from btc_embedded import EPRestApi, util
import tempfile
import shutil

def run_mil_tests():
    ep = EPRestApi(version='25.1p0')
    mil_projects = [p for p in glob('test/*.epx') if not p.endswith('_milsil.epx')]
    all_passed = True
    for mil_project in mil_projects:
        is_passed = run_mil_tests_for_project(ep, mil_project)
        if not is_passed:
            all_passed = False
    return all_passed

def run_mil_tests_for_project(ep, project_file):
    project_file = os.path.abspath(project_file)
    project_name = os.path.basename(project_file)[:-4]
    report_dir = os.path.abspath('reports')
    print(f"\nTesting {project_name} (MIL)\n")

    util.run_matlab_script(ep, os.path.abspath('model/init.m'))
    ep.get(f'profiles/{project_file}')
    scopes = ep.get('scopes')
    scope_uids = [scope['uid'] for scope in scopes]
    toplevel_scope_uid = scope_uids[0]
    
    # execute requirements-based tests
    rbt_exec_payload = {
        'UIDs': scope_uids,
        'data' : { 'execConfigNames' : [ 'SL MIL (Toplevel)' ] }
    }
    exec_start_time = datetime.now()
    rbt_response = ep.post('scopes/test-execution-rbt', rbt_exec_payload, message="Executing requirements-based tests")
    util.print_rbt_results(rbt_response)

    # Create project report
    report = ep.post(f"scopes/{toplevel_scope_uid}/project-report", message="Creating test report")
    # export project report to a file called 'report.html'
    ep.post(f"reports/{report['uid']}", { 'exportPath': report_dir, 'newName': 'report' })

    # Dump JUnit XML report
    test_cases = ep.get('test-cases-rbt')
    is_passed = rbt_response['testResults']['SL MIL (Toplevel)']['totalTests'] == rbt_response['testResults']['SL MIL (Toplevel)']['passedTests']
    if not is_passed:
        util.dump_testresults_junitxml(
            rbt_results=rbt_response,
            scopes=scopes,
            test_cases=test_cases,
            start_time=exec_start_time,
            project_name=project_name,
            output_file=os.path.join(report_dir, 'test_results.xml')
        )
    return is_passed

def run_sil_tests():
    ep = EPRestApi(version='25.1p0')

    project_file = os.path.abspath('test/seat_heating_controller_milsil.epp')
    hook_file = os.path.abspath('test/btc_hooks.py')
    project_name = os.path.basename(project_file)[:-4]
    report_dir = os.path.abspath('reports')
    print(f"\nTesting {project_name} (MIL+SIL)\n")
    
    # hook file for enhanced traceability
    ep.put('preferences', [{
        'preferenceName': 'GENERAL_HOOKS_COMMAND',
        'preferenceValue': f'python "{hook_file}"'}])

    # import TargetLink model with relevant subsystems
    relevant_subsystems, subsystems_pattern = get_relevant_subsystems()
    tl_import = {
        'tlModelFile': os.path.abspath('model/seat_heating_controller.slx'),
        'tlInitScript' : os.path.abspath('model/init.m'),
        'subsystemMatcher' : rf'.*/({subsystems_pattern})$'
    }
    ep.post('profiles', { 'path': project_file }, message="Creating test project")
    ep.post('architectures/targetlink', tl_import, message="Analysing model, generating and analysing code")
    
    scopes = ep.get('scopes')
    scope_uids = [scope['uid'] for scope in scopes]
    toplevel_scope_uid = scope_uids[0]

    # import requirements
    import_requirements(ep)

    # import test cases
    import_test_cases(ep, relevant_subsystems, scopes)
   
    # execute requirements-based tests
    rbt_exec_payload = {
        'UIDs': scope_uids,
        'data' : { 'execConfigNames' : [ 'SIL' ] }
    }
    exec_start_time = datetime.now()
    rbt_response = ep.post('scopes/test-execution-rbt', rbt_exec_payload, message="Executing requirements-based tests")
    rbt_coverage = ep.get(f"scopes/{toplevel_scope_uid}/coverage-results-rbt")
    util.print_rbt_results(rbt_response, rbt_coverage)

    publish_results_to_polarion(ep)

    # Create project report
    report = ep.post(f"scopes/{toplevel_scope_uid}/project-report?template-name=rbt-sil-only", message="Creating test report")
    # export project report to a file called 'report.html'
    ep.post(f"reports/{report['uid']}", { 'exportPath': report_dir, 'newName': 'report' })

    # Dump JUnit XML report
    test_cases = ep.get('test-cases-rbt')
    util.dump_testresults_junitxml(
        rbt_results=rbt_response,
        scopes=scopes,
        test_cases=test_cases,
        start_time=exec_start_time,
        project_name=project_name,
        output_file=os.path.join(report_dir, 'test_results.xml')
    )

    # Save *.epp
    ep.put('profiles', { 'path': project_file }, message="Saving test project")

######### HELPER FUNCTIONS ##########

def get_relevant_subsystems():
    sl_arch_files = glob('test/*_btcdata/model/simulink_toplevel/slArch.xml')
    relevant_subsystems = []
    for arch_file in sl_arch_files:
        tree = ET.parse(arch_file)
        root = tree.getroot()
        subsystem = root.find('.//subsystem')
        if subsystem is not None and 'name' in subsystem.attrib:
            subsystem_name = subsystem.attrib['name']
            if subsystem_name.startswith('Wrapper_'):
                subsystem_name = subsystem_name[8:]
            relevant_subsystems.append(subsystem_name)

    subsystem_pattern = '|'.join([re.escape(f"{name}") for name in relevant_subsystems])

    return relevant_subsystems, subsystem_pattern

def import_test_cases(ep, relevant_subsystems, scopes):
    arch_name = ep.get('architectures?architecture-kind=TargetLink')[0]['name']
    # import test cases
    for subsystem in relevant_subsystems:
        test_cases = glob(f'test/{subsystem}_btcdata/testcases/*.tc.json')

        # Copy all test case files to the temporary directory
        temp_dir = tempfile.mkdtemp()
        for test_case in test_cases:
            shutil.copy(test_case, temp_dir)
        # filter out ui_settings.tc.json files
        relevant_scope = next((scope for scope in scopes if scope['name'] == subsystem), None)
        if relevant_scope is None:
            print(f"Subsystem {subsystem} not found.")
            continue
        signal_uids = [sig['uid'] for sig in ep.get(f'scopes/{relevant_scope["uid"]}/signals')]
        signal_names_by_kind = {
            'inputs': [],
            'parameters': [],
            'locals': [],
            'outputs': [],
        }
        for sig in signal_uids:
            signal = ep.get(f'signals/{sig}/signal-datatype-information')
            key = signal['kind'].lower() + 's'
            signal_names_by_kind[key].append(signal['name'])
        tc_files = [os.path.join(temp_dir, os.path.basename(tc)) for tc in test_cases if not tc.endswith('.ui_settings.tc.json')]
        # adapt the MLI json file to TL target architecture
        for tc_file in tc_files:
            with open(tc_file, 'r') as f:
                tc_data = json.load(f)
                tc_data['metaData']['architecture'] = arch_name
                tc_data['metaData']['scopePath'] = relevant_scope['path']
                tc_data['interface'] = signal_names_by_kind
                with open(tc_file, 'w') as f:
                    json.dump(tc_data, f, indent=4)
        
        tc_import_payload = { "paths": tc_files, 'overwritePolicy' : 'OVERWRITE'}
        ep.put('test-cases-rbt', tc_import_payload, message=f"Importing test cases for {subsystem}")
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

def import_requirements(ep):
    def get_by_key(list, key):
        return next((item['value'] for item in list if item['key'] == key), None)

    req_json_files = glob('test/*_btcdata/requirements/*.json')
    req_json_file = next((f for f in req_json_files if 'milsil_btcdata' not in f), None) 
    if req_json_file:
        with open(req_json_file, 'r') as f: req_data = json.load(f)
        settings = [
            { 'key': 'project_id', 'value': get_by_key(req_data['importOptions'], 'Project URL') },
            { 'key': 'username', 'value': os.environ.get('POLARION_USERNAME') },
            { 'key': 'pwd', 'value': os.environ.get('POLARION_PWD') },
            { 'key': 'host', 'value': get_by_key(req_data['importOptions'], 'Host') },
            { 'key': 'port', 'value': get_by_key(req_data['importOptions'], 'Port') },
            { 'key': 'filter', 'value': 'type:requirement' }
            
        ]
        req_import_payload = {
            'kind' : req_data['metaData']['kind'].upper(),
            'nameAttribute' : get_by_key(req_data['importOptions'], 'name_attr_value'),
            'descriptionAttribute' : get_by_key(req_data['importOptions'], 'desc_attr_value'),
            'additionalAttributes' : req_data['metaData']['additionalAttributes'],
            'settings' : settings,
        }
        ep.post('requirements-import', req_import_payload, message="Importing requirements from Polarion")

def publish_results_to_polarion(ep):
    req_src = ep.get('requirements-sources')[0]
    project_url = next((setting['value'] for setting in req_src['settings'] if setting['key'] == 'project_url'), None)
    host = next((setting['value'] for setting in req_src['settings'] if setting['key'] == 'host'), None)
    port = next((setting['value'] for setting in req_src['settings'] if setting['key'] == 'port'), None)
    payload = {
        "settings" : [
            { "key": "Project ID", "value": project_url},
            { "key": "Host", "value": host },
            { "key": "Port", "value": port },
            { "key": "username", "value": os.environ.get('POLARION_USERNAME') },
            { "key": "pwd", "value": os.environ.get('POLARION_PWD') },
            { "key": "Linked Requirement Role", "value": "verifies" },
            { "key": "Work Item Types", "value": "Test Case" }
        ],
        "execConfigNames" : [ "SIL" ],
        "requirementsSourceUid" : req_src['uid'],
        "syncMode" : "EP",
        "testStepsConsidered" : True
    }
    ep.post('test-case-source-sync', payload, message="Publishing test results to Polarion")

def announce(message: str):
    print(f"\n{'#' * 80}\n\n{message}\n\n{'#' * 80}\n")

if __name__ == '__main__':
    announce("Running tests on MIL")
    success = run_mil_tests()
    if success:
        announce("MIL tests passed, now running tests on SIL")
        success = run_sil_tests()
    else:
        announce("MIL tests failed. Skipping SIL tests, coverage, etc.")
