# AVS Mock Plugin

The plugin receives a `host` and a `port` arguments. Makes a GET request to the `/eigen/node/health` endpoint of the AVS instance running at `http://<host>:<port>`. The plugin should run in the same docker network as the AVS instance and using the docker-compose service name for `host` is preferred.

## Default values

```
host: "main-service"
port: 8080
```

## How to build the image

Execute the following command from the plugin folder:

```bash
docker build . -t <image_tag>
```

Replace `<image_tag>` with the desired tag for the plugin image.

## How to run the plugin container

```bash
docker run --rm -p <your_port>:8045 --network <avs_docker_network> --host <host> --port <port>
```

Make sure to replace `<your_port>` with the port you want to expose in your machine. `<avs_docker_network>` must be the same docker network that the AVS instance you want to check is using.

For a quick run, you can check a mock AVS instance running with the default values of the `health-checker` profile:

```bash
docker build . -t avs-plugin
docker run --rm -p 8045:8045 --network eigenlayer avs-plugin --host main-service --port 8090
```

## Check files and directories existence inside plugin container

For testing purposes, you can check the existence of a list of files and directories inside a container by using the --check-paths flag and passing a path to a JSON file that contains the list of paths to check. The JSON file must be bound as a volume inside the container. If one of the paths does not exist, the process will end with a status code of 1. The JSON file must be formatted as follows:

```json
[
    "/path/to/file",
    "/path/to/dir"
]
```

**Example:**

Assuming that the `check.json`` file is located in the working directory, containing the following:

```json
[
    "/tmp",
    "/tmp/check.json"
]
```

You can run the following command:

```bash
docker run --rm -v $(pwd)/check.json:/tmp/check.json mock-avs-plugin:latest --check-paths /tmp/check.json
```

This example is a self-check of the `check.json` file.

> Note: The paths must be absolute paths inside the container.
