# mock-avs

This repository contains the source code of services and plugin used in the [mock-avs-pkg](https://github.com/NethermindEth/mock-avs-pkg) project.

## Build services images

This repository contains two services: `option-returner` and `health-checker`, to build each of them follow the instructions below.

### Build `option-returner` image

```bash
docker build -t mock-avs-option-returner:v0.2.1 https://github.com/NethermindEth/mock-avs-src.git#v0.2.1:option-returner
```

This command generates the docker image `mock-avs-option-returner:v0.2.1` which can be used to run the service.

### Build `health-checker` image

```bash
docker build -t mock-avs-health-checker:v0.2.1 https://github.com/NethermindEth/mock-avs-src.git#v0.2.1:health-checker
```

This command generates the docker image `mock-avs-health-checker:v0.2.1` which can be used to run the service.

### Build `plugin` image

```bash
docker build -t mock-avs-plugin:v0.2.1 https://github.com/NethermindEth/mock-avs-src.git#v0.2.1:plugin
```

This command generates the docker image `mock-avs-plugin:v0.2.1` which can be used to run the plugin.
