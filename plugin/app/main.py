import requests

host = "main-service"
port = 8080

def health_check(avs_target: str):
    # Make request to AVS health check endpoint
    # If AVS is up, return 200
    # If AVS is down, raise 503
    # If AVS is up but not ready, return 206
    try:
        resp = requests.get(f"http://{avs_target}/eigen/node/health")
        if resp.status_code == 200:
            print("AVS is up")
        elif resp.status_code == 206:
            print("AVS is up but not ready")
        elif resp.status_code == 503:
            print("AVS is down")
        else:
            print("AVS is in an unknown state")
    except Exception as e:
        print(f"AVS is down, got exception: {e}")

if __name__ == "__main__":
    # Get arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default=host)
    parser.add_argument("--port", type=int, default=port)
    args = parser.parse_args()
    host = args.host
    port = args.port
    health_check(f"{host}:{port}")