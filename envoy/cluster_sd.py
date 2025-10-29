from flask import Flask, jsonify, request
import socket


class Endpoints:
    def __init__(self):
        self._endpoints = {}

    def add(self, address, port):
        ip = socket.gethostbyname(address)
        if not ip:
            return False
        self._endpoints[f"{address}:{port}"] = {
            'endpoint': {
                'address': {
                    'socket_address': {
                        'address': ip,
                        'port_value': int(port)
                    }
                }
            }
        }
        return True

    def remove(self, address, port):
        if f"{address}:{port}" in self._endpoints:
            del self._endpoints[f"{address}:{port}"]
            return True
        return False

    def clear(self):
        self._endpoints.clear()

    def list(self):
        return list(self._endpoints.values())

    def json(self):
        return jsonify(list(self._endpoints.values()))


app = Flask(__name__)
endpoints = Endpoints()

@app.route('/v3/discovery:endpoints', methods=['POST'])
def envoy_get_cluster_config():
    """Envoy EDS endpoint - returns ClusterLoadAssignment for endpoint discovery."""
    response = {
        'version_info': '1',
        'resources': [
            {
                '@type': 'type.googleapis.com/envoy.config.endpoint.v3.ClusterLoadAssignment',
                'cluster_name': 'test-cluster',
                'endpoints': [
                    {
                        'lb_endpoints': endpoints.list()
                    }
                ]
            }
        ]
    }
    return jsonify(response), 200

@app.route('/cluster-config', methods=['POST'])
def update_cluster_config():
    address = request.json.get('address')
    port = request.json.get('port')

    if address and port:
        if endpoints.add(address, port):
            return endpoints.json(), 200

    return endpoints.json(), 404

@app.route('/remove-endpoint', methods=['POST'])
def remove_endpoint():
    address = request.json.get('address')
    port = request.json.get('port')

    if endpoints.remove(address, port):
        return endpoints.json(), 200

    return endpoints.json(), 404

@app.route('/reset', methods=['POST'])
def clear_hosts():
    endpoints.clear()
    return 'done!', 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5123)

