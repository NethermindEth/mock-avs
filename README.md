# mock-avs-src

This repository contains the source code of services used in the [mock-avs](https://github.com/NethermindEth/mock-avs) project.

## Build services images

This repository contains two services: `option-returner` and `health-checker`, to build each of them follow the instructions below.

### Build `option-returner` image

```bash
docker build -t mock-avs-option-returner:latest https://github.com/NethermindEth/mock-avs-src.git#main:option-returner
```

This command generates the docker image `mock-avs-option-returner:latest` which can be used to run the service.

### Build `health-checker` image

```bash
docker build -t mock-avs-health-checker:latest https://github.com/NethermindEth/mock-avs-src.git#main:health-checker
```

This command generates the docker image `mock-avs-health-checker:latest` which can be used to run the service.
