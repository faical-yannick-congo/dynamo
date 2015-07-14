#!/bin/bash

echo "Launching component: Derived..."
#Run all the in types: serial, tcp, udp, telnet and ssh
#Then run
cd core
sudo python GeneratedComponent.py
cd ..