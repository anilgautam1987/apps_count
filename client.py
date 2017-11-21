import json
import requests
import sys
import re
from Server import _load_servers
from pprint import pprint
from prettytable import PrettyTable

"""
client module to fetch the server computation reports
"""
def get_request(hostname):
   """ : request to flask api """
   api_endpoint = 'http://127.0.0.1:9999/{0}/status'.format(hostname)
   header_info = {
       'cache-control': 'no-cache',
       'accept': 'application/json',
       'content-type': 'application/json'
   }
   response = requests.get(api_endpoint, headers=header_info)
   server_data = None
   if response.status_code == 200:
       server_data = response.content
       server_data = server_data.replace('\n' , '')
       server_data = re.sub(' +',' ',server_data)
   return server_data

app_main_dict = dict()
def prepare_data_structure(jdata):
    """ prepare data structure for all application or by application name"""
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
    """ print humen readable format and dump the data to json file """
    if not params['app_computed_dict']:
        return 'please send the data.!!!'

    app_name = None
    if 'app_name' in params:
        app_name = params['app_name']

    success_rate = None
    app_computed_dict = params['app_computed_dict']
    x = PrettyTable(["Application Name", "Version", "Success Rate"])
    x.align["Application Name"] = "l"

    # looping through the data structure and printing in humen-readable format
    if app_name:
        for app_version , app_name_dict in app_computed_dict[app_name].iteritems():
            success_rate = (float(app_computed_dict[app_name][app_version]['Success_Count']) / float(app_computed_dict[app_name][app_version]['Request_Count'])) * 100
            x.add_row([app_name, app_version, "{0:.2f}%".format(success_rate)])
        print(x)
    else:
        for app_name, app_name_dict in app_computed_dict.iteritems():
            for app_version, app_version_count in app_name_dict.iteritems():
                success_rate = (float(app_computed_dict[app_name][app_version]['Success_Count']) / float(app_computed_dict[app_name][app_version]['Request_Count'])) * 100
                x.add_row([app_name, app_version, "{0:.2f}%".format(success_rate)])
        print(x)

def generate_report_file(**params):
    # write data to local json file
    app_computed_dict = params['app_computed_dict']
    with open('app_count_report.json', 'w') as fp:
        json.dump(app_computed_dict, fp)

def main():
    """ Main Function """
    servers = [s.strip() for s in _load_servers()]
    host_data = []
    for host in servers:
        response = get_request(hostname=host)
        if response:
            response = json.loads(response)
            response = response.values()[0]
            host_data.append(response)

    print '******************** Parsed Data Structure ***************'
    app_computed_dict = prepare_data_structure(host_data)
    #print_result(**{'app_computed_dict': app_computed_dict, 'app_name': 'Webapp2'})
    print_result(**{'app_computed_dict': app_computed_dict})
    generate_report_file(**{'app_computed_dict': app_computed_dict})

if __name__ == '__main__':
    """test client"""
    main()