#!/bin/bash
#
# Test Envoy load balancer by making multiple requests
#
# Usage:
#   ./test_loadbalancer.sh              # 10 requests to localhost:9097
#   ./test_loadbalancer.sh 20           # 20 requests
#   ./test_loadbalancer.sh 10 localhost:8080  # 10 requests to specific host

NUM_REQUESTS=${1:-10}
TARGET=${2:-localhost:9097}

echo "Sending $NUM_REQUESTS requests to $TARGET"
echo "Press Ctrl+C to stop"
echo ""

for i in $(seq 1 "$NUM_REQUESTS"); do
    echo "Request $i:"
    curl -s "http://$TARGET/" | jq -r '.message // .server_name // .'
    echo ""
    sleep 0.5
done

echo "Done!"
