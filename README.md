# Social Network Part of the Network Project

Make sure to clone the DeathStarBench first!

After cloning DeathStarBench, follow their socialNetwork guides to set everything up. And then put the baseline_benchmark.py in ./DeadthStarBench/socialNetwork for in order to generate loads. 

Here is a more detailed descriptions of each file:

- `baseline_benchmark.py`: This file is used to generate loads for the social network benchmark. It should be placed in the `./DeadthStarBench/socialNetwork` directory.

- `nginx-thrift-service-profile.yaml`: This is the service provider we used. You can modify the timeout and retry settings according to your preferences.

- `./data`: This is the folder where we stored all the socialNetwork data that we generated for this project.

- `./Setup/install.sh`: the scipted we used to setup the kubernetes environment on CloudLab. 

- `./Setup/linkerd_setup.sh`: the scipted we used to setup the Linkerd service mesh and injecting sidecars. 

