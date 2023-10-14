# DDOS-detection
DDOS Detection using ML 

Installation steps:
* Install Virtual Box 
* Install Mininet VM 
* Install Ubuntu
* Install Ryu-controller
* Git clone this repo 
* cd ddos_detection 
* Install Python 
* Create a Python env 
```bash
    pip install virtualenv
    virtualenv env 
    virtualenv -p /usr/bin/python3 env 
    source virtualenv_name/bin/activate
```
* Install the modules from requirements.txt
```bash
    pip install -r requirements.txt
```
* Download dataset csv from https://drive.google.com/file/d/1OZR9B-PXhgC3aZEraTCv2IIjXGSzkHzN/view?usp=sharing and save it in the data directory.

How to run:
Open terminal and type the below commands

```bash
ifcongif
```
Copy the ip and replace it (192.168.0.101) with your ip(ex: 10.0.x.x) in topology, create_benign_traffic, create_ddos_traffic files. 
Run the random forests file to create a trained model 

```bash
    python3 src/classification/random_forests.py
```

This will create the FlowStatsfile.csv with normal and ddos traffic
Creates the normal traffic 
```bash
  ryu-manager src/controller/collect_benign_traffic.py
```

Open another terminal and type 
```bash
  python3 toplogy create_benign_traffic.py
```

Creates the DDOS traffic 
```bash
  ryu-manager src/collect_ddos_traffic.py
```

Open another terminal and type 

```bash
  python3 toplogy create_ddos_traffic.py
```



This command provides the execute permission for the run script
```bash
 chmod +x ./run.sh
```
To run the script

```bash
 ./run.sh
```
Type 1 for running the controller 

Once the controller starts running 
Open another terminal and run the script again 
```bash
 ./run.sh
```
Type 2 for running the mininet topology  
For creating normal traffic 
```bash
 xterm h1_1 
 xterm h1_2 
```
Open the first node terminal and type 
```bash
ifconfig 
```
Open the second node terminal and type 
```bash
ping 10.0.x.x
```
 Use any of the below Hping cmd to create the DDOS traffic
```bash
# icmp flood
h1_2 hping3 -1 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.4

# syn flood
h2_5 hping3 -S -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.6

# udp flood
h1_3 hping3 -2 -V -d 120 -w 64 -p 80 --rand-source --flood 10.0.0.5








