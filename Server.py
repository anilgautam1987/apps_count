import sys
import json
import flask

app = flask.Flask(__name__)

SERVER_HEALTH = {}

def _load_servers():
  """ Load entries from servers.txt """
  with open('servers.txt') as fd:
    return fd.readlines()

def _load_responses():
  """ Load entries from responses.txt """
  return json.loads(open('responses.txt').read())

def _map_servers_to_responses():
  """ Map each server against its response """
  servers = _load_servers()
  responses = _load_responses()

  global SERVER_HEALTH

  for i in range(len(servers)):
    SERVER_HEALTH[servers[i].strip()] = responses[i]

@app.errorhandler(404)
def server_not_found(err):
  """ 404 handler """
  response = flask.jsonify(error=404, text=str(err))
  response.status_code = 404
  return response

@app.route('/<server>/status', methods=['GET'])
def get_server_status(server):
  """ Return server's status from SERVER_HEALTH map """
  if server not in SERVER_HEALTH:
    return server_not_found('Invalid server - %s - does not exist' % server)

  return flask.jsonify({server: SERVER_HEALTH[server]})

def main(args):
  """ Main function """
  _map_servers_to_responses()
  app.run(host='127.0.0.1', port=9999, debug=True)
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))