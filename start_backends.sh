#!/bin/bash
#
# Start multiple backend servers for testing Envoy load balancing
#
# Usage:
#   ./start_backends.sh         # Start 3 default backends
#   ./start_backends.sh 5       # Start 5 backends

set -e

NUM_BACKENDS=${1:-3}
START_PORT=8080
HOST="0.0.0.0"

echo "Starting $NUM_BACKENDS backend servers..."
echo ""

PIDS=()

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping all backend servers..."
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            echo "Stopped backend server (PID: $pid)"
        fi
    done
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Start backend servers
for i in $(seq 1 "$NUM_BACKENDS"); do
    PORT=$((START_PORT + i - 1))
    NAME="Backend-$i"
    
    echo "Starting $NAME on port $PORT..."
    python3 backend_server.py --port "$PORT" --name "$NAME" --host "$HOST" &
    PID=$!
    PIDS+=("$PID")
    
    # Give it a moment to start
    sleep 0.5
done

echo ""
echo "All backend servers started!"
echo ""
echo "Backend servers:"
for i in $(seq 1 "$NUM_BACKENDS"); do
    PORT=$((START_PORT + i - 1))
    echo "  Backend-$i: http://localhost:$PORT (PID: ${PIDS[$((i-1))]})"
done

echo ""
echo "Test endpoints:"
echo "  curl http://localhost:$START_PORT/"
echo "  curl http://localhost:$START_PORT/health"
echo "  curl http://localhost:$START_PORT/echo"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for all background processes
wait
