#!/usr/bin/env python3
"""
Simple Flask backend server for testing Envoy load balancing.

Usage:
    python backend_server.py --port 8080 --name "Backend-1"
    python backend_server.py -p 8081 -n "Backend-2"
"""

import argparse
import socket
from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# Global variables set by command line args
SERVER_NAME = "Backend-Server"
SERVER_PORT = 8080


@app.route('/', methods=['GET'])
def home():
    """Root endpoint - returns server information."""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    response = {
        'server_name': SERVER_NAME,
        'port': SERVER_PORT,
        'hostname': hostname,
        'ip_address': local_ip,
        'timestamp': datetime.now().isoformat(),
        'message': f'Hello from {SERVER_NAME} on port {SERVER_PORT}!'
    }
    
    print(f"[{datetime.now()}] Request from {request.remote_addr} -> {SERVER_NAME}:{SERVER_PORT}")
    
    return jsonify(response), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'server': SERVER_NAME,
        'port': SERVER_PORT
    }), 200


@app.route('/echo', methods=['GET', 'POST'])
def echo():
    """Echo endpoint - returns request details."""
    response = {
        'server_name': SERVER_NAME,
        'port': SERVER_PORT,
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers),
        'args': dict(request.args),
        'remote_addr': request.remote_addr,
        'timestamp': datetime.now().isoformat()
    }
    
    if request.method == 'POST':
        if request.is_json:
            response['json_data'] = request.get_json()
        else:
            response['body'] = request.get_data(as_text=True)
    
    return jsonify(response), 200


@app.route('/api/data', methods=['GET'])
def api_data():
    """Sample API endpoint."""
    return jsonify({
        'server': SERVER_NAME,
        'port': SERVER_PORT,
        'data': [
            {'id': 1, 'value': 'Item 1'},
            {'id': 2, 'value': 'Item 2'},
            {'id': 3, 'value': 'Item 3'}
        ]
    }), 200


def main():
    """Main entry point."""
    global SERVER_NAME, SERVER_PORT
    
    parser = argparse.ArgumentParser(
        description='Simple Flask backend server for testing Envoy load balancing'
    )
    parser.add_argument(
        '-p', '--port',
        type=int,
        default=8080,
        help='Port to run the server on (default: 8080)'
    )
    parser.add_argument(
        '-n', '--name',
        type=str,
        default='Backend-Server',
        help='Name of the server (default: Backend-Server)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='0.0.0.0',
        help='Host to bind to (default: 0.0.0.0)'
    )
    
    args = parser.parse_args()
    
    SERVER_NAME = args.name
    SERVER_PORT = args.port
    
    print("=" * 60)
    print(f"Starting {SERVER_NAME}")
    print(f"Host: {args.host}")
    print(f"Port: {SERVER_PORT}")
    print("=" * 60)
    print("\nEndpoints:")
    print(f"  GET  /           - Server info")
    print(f"  GET  /health     - Health check")
    print(f"  GET  /echo       - Echo request details")
    print(f"  POST /echo       - Echo request with body")
    print(f"  GET  /api/data   - Sample API data")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host=args.host, port=SERVER_PORT, debug=False)


if __name__ == '__main__':
    main()
