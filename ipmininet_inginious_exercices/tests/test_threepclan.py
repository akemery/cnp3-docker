"""This module tests threepclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.threepclan import ThreePCLAN
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo



@require_root
def test_ThreePCLAN_Success():
    try:
        net = IPNet(topo=ThreePCLAN(), use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net["h3"].cmd("ip addr del 10.0.0.67/25 dev h3-eth0")
        net["h3"].cmd("ip addr add 10.0.0.2/24 dev h3-eth0")
      
        net.stop()
        with open('state4.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert state == "Success"
    finally:
        cleanup()
        
 
@require_root
def test_ThreePCLAN_Failed():
    try:
        net = IPNet(topo=ThreePCLAN(), use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net.stop()
        with open('state4.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert state == "Failed"
    finally:
        cleanup()
