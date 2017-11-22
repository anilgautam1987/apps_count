## Synopsis

This tool will provide the statistics of all the application success rate.

## Code Example
 Usage of this tool is pretty simple, as this tool is made of REST API where any developer can write their own client and based on that you can generate the statistics.

## Motivation

Removing the manual work and can be used to generate the daily report.

## Installation

python setup.py install

## API Reference
Run Server : <br>
python server.py <br>
server api endpoint:
    http://127.0.0.1:9999/{server_name}/status/ <br>
client:<br>
     pull request by applicatin name
     python client.py --app_name=Cache1 <br>
     python client.py
