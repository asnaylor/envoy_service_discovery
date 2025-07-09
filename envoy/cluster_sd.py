from flask import Flask, jsonify, request
import socket


app = Flask(__name__)

#endpoint_dict = {
#                'endpoint' : {
#                    'address': {
#                        'socket_address': {
#                            'address': '128.55.64.36',
#                            'port_value': 9089
#                            }
#                    }
#                }
#}

endpoints = []

@app.route('/v3/discovery:clusters', methods=['POST'])
def envoy_get_cluster_config():
    response = {
        'version_info': '1',
        'resources': [
            {
                '@type': 'type.googleapis.com/envoy.config.cluster.v3.Cluster',
                'name': 'test-cluster',
                'connect_timeout': '0.25s',
                'lb_policy': 'round_robin',
                'load_assignment': {
                    'cluster_name': 'test-cluster',
                    'endpoints': {'lb_endpoints': endpoints}
                }
            }
        ]
    }
    return jsonify(response), 200

@app.route('/cluster-config', methods=['POST'])
def update_cluster_config():
    global endpoints
    address = request.json.get('address')
    port = request.json.get('port')

    if address and port:
        ip = socket.gethostbyname(address)
        if not ip:
            return jsoninfy(endpoints), 404
        endpoints.append({'endpoint': {'address':{'socket_address':{'address': f'{ip}', 'port_value':f'{port}'}}}})
        return jsonify(endpoints), 200

    return jsoninfy(endpoints), 404
    

@app.route('/reset', methods=['POST'])
def clear_hosts():
    global endpoints
    endpoints = []
    return 'done!', 200

if __name__ == '__main__':
    app.run()
