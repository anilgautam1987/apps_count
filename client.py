import json
import sys
import re
import argparse
import requests
from server import _load_servers
from prettytable import PrettyTable
import constant as C

"""
client module to fetch the server computation reports
"""
def get_request(servername):
   """ : request to flask api
       : hostname - get status for server name
   """
   api_endpoint = 'http://' + '{0}:{1}/{2}/status'.format(C.default_host,C.default_port, servername)
   header_info = {
       'cache-control': 'no-cache',
       'accept': 'application/json',
       'content-type': 'application/json'
   }
   response = requests.get(api_endpoint, headers=header_info)
   server_data = None
   if response.status_code == C.success_code:
       server_data = response.content
       server_data = server_data.replace('\n' , '')
       server_data = re.sub(' +',' ',server_data)
   return server_data

app_main_dict = dict()
def prepare_data_structure(jdata):
    """ prepare data structure for all application or by application name
        : jdata - list of sever response in dict format
    """
    for app_dict in jdata:
        if not app_dict['Application'] in app_main_dict.keys():
            app_main_dict[app_dict['Application']] = dict()

        if not app_dict['Version'] in app_main_dict[app_dict['Application']].keys():
            app_main_dict[app_dict['Application']][app_dict['Version']] = dict()

        if not app_main_dict[app_dict['Application']][app_dict['Version']].has_key('Request_Count'):
            app_main_dict[app_dict['Application']][app_dict['Version']]['Request_Count'] = 0
        if not app_main_dict[app_dict['Application']][app_dict['Version']].has_key('Success_Count'):
            app_main_dict[app_dict['Application']][app_dict['Version']]['Success_Count'] = 0
        if not app_main_dict[app_dict['Application']][app_dict['Version']].has_key('Error_Count'):
            app_main_dict[app_dict['Application']][app_dict['Version']]['Error_Count'] = 0

        app_main_dict[app_dict['Application']][app_dict['Version']]['Request_Count'] += app_dict['Request_Count']
        app_main_dict[app_dict['Application']][app_dict['Version']]['Success_Count'] += app_dict['Success_Count']
        app_main_dict[app_dict['Application']][app_dict['Version']]['Error_Count'] += app_dict['Error_Count']
    return app_main_dict

def print_result(**params):
    """ print humen readable format and dump the data to json file
        : params - application name or list of server response in dict format
    """
    if not params['app_computed_dict']:
        return 'please send the data.!!!'

    application_name = None
    if 'app_name' in params:
        application_name = params['app_name']

    success_rate = None
    app_computed_dict = params['app_computed_dict']
    x = PrettyTable(["Application Name", "Version", "Success Rate"])
    x.align["Application Name"] = "l"

    if application_name:
        for app_version , app_name_dict in app_computed_dict[application_name].iteritems():
            success_rate = (float(app_computed_dict[application_name][app_version]['Success_Count']) / float(app_computed_dict[application_name][app_version]['Request_Count'])) * 100
            x.add_row([application_name, app_version, "{0:.2f}%".format(success_rate)])
        print(x)
    else:
        for application_name, app_name_dict in app_computed_dict.iteritems():
            for app_version, app_version_count in app_name_dict.iteritems():
                success_rate = (float(app_computed_dict[application_name][app_version]['Success_Count']) / float(app_computed_dict[application_name][app_version]['Request_Count'])) * 100
                x.add_row([application_name, app_version, "{0:.2f}%".format(success_rate)])
        print(x)

def generate_report_file(**params):
    """ create a report file in json format
       : app_computed_dict - list of server response in dictionary format
    """
    app_computed_dict = params['app_computed_dict']
    with open('app_count_report.json', 'w') as fp:
        json.dump(app_computed_dict, fp)

def compute_server_statistics(application_by_name):
    """ compute server statistics
       : server - read list of servers from txt file
       : print result - prints reports in humen readable format
       : generate report - created report in json file format
    """
    servers = [s.strip() for s in _load_servers()]
    host_data = []
    for host in servers:
        response = get_request(servername=host)
        if response:
            response = json.loads(response)
            response = response.values()[0]
            host_data.append(response)

    print '******************** Parsed Data Structure ***************'
    app_computed_dict = prepare_data_structure(host_data)
    print_result(**{'app_computed_dict': app_computed_dict, 'app_name': application_by_name})
    #print_result(**{'app_computed_dict': app_computed_dict})
    generate_report_file(**{'app_computed_dict': app_computed_dict})

if __name__ == '__main__':
    """test client"""
    parser = argparse.ArgumentParser(description="application aggregate report")
    parser.add_argument('-n', '--app_name', type=str, required=False)
    args = parser.parse_args()
    compute_server_statistics(application_by_name = args.app_name)
