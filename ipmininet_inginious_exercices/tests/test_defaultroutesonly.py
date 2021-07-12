"""This module tests twopclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.defaultroutesonly import DefaultRoutesOnly
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_DefaultRoutesOnly_firstsolution():
    """ First solution
            R1 has R3 as default route
            R3 has R2 as default route
            R2 has R1 as default route"""
              
    subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
    prefixlen=["24", "24", "24", "24", "24", "24"]
    gw=["192.168.1.1", "192.168.2.1", "192.168.3.1", "192.168.6.2", "192.168.5.1", \
    "192.168.4.1"]
    try:
        net = IPNet(topo=DefaultRoutesOnly("4", subnet, prefixlen, gw) \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net["A"].cmd("ip route add default via 192.168.1.1")
        net["B"].cmd("ip route add default via 192.168.2.1")
        net["C"].cmd("ip route add default via 192.168.3.1")
                 
        net["R1"].cmd("ip route add default via 192.168.6.2")
        net["R3"].cmd("ip route add default via 192.168.5.1")
        net["R2"].cmd("ip route add default via 192.168.4.1")
        
        r = net.pingAll()
        
        print(r)
       
        net.stop()
        with open('state6.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()

@require_root
def test_DefaultRoutesOnly_secondsolution():
    """ Second solution
            R1 has R2 as default route
            R2 has R3 as default route
            R3 has R1 as default route"""
            
    subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
    prefixlen=["24", "24", "24", "24", "24", "24"]
    gw=["192.168.1.1", "192.168.2.1", "192.168.3.1", "192.168.4.2", "192.168.6.1", "192.168.5.2"]
    try:
        net = IPNet(topo=DefaultRoutesOnly("4", subnet, prefixlen, gw) \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net["A"].cmd("ip route add default via 192.168.1.1")
        net["B"].cmd("ip route add default via 192.168.2.1")
        net["C"].cmd("ip route add default via 192.168.3.1")
                 
        net["R1"].cmd("ip route add default via 192.168.4.2")
        net["R3"].cmd("ip route add default via 192.168.6.1")
        net["R2"].cmd("ip route add default via 192.168.5.2")
        
        
        r = net.pingAll()
        
        print(r)
       
        net.stop()
        with open('state6.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()


@require_root
def test_DefaultRoutesOnly_wrong():
    """ Second solution
            R1 has R2 as default route
            R2 has R3 as default route
            R3 has R1 as default route"""
            
    subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
    prefixlen=["24", "24", "24", "24", "24", "24"]
    gw=["192.168.1.1", "192.168.2.1", "192.168.3.1", "192.168.4.2", "192.168.6.1", "192.168.5.2"]
    try:
        net = IPNet(topo=DefaultRoutesOnly("4", subnet, prefixlen, gw) \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net["A"].cmd("ip route add default via 192.168.1.1")
        net["B"].cmd("ip route add default via 192.168.2.1")
        net["C"].cmd("ip route add default via 192.168.3.1")
                 
        
        net["R1"].cmd("ip route add 192.168.2.0/24 dev R1-eth1 via 192.168.4.2")
        net["R1"].cmd("ip route add 192.168.3.0/24 dev R1-eth2 via 192.168.6.2")
        
        net["R2"].cmd("ip route add 192.168.1.0/24 dev R2-eth1 via 192.168.4.1")
        net["R2"].cmd("ip route add 192.168.3.0/24 dev R2-eth2 via 192.168.5.2")
        
        net["R3"].cmd("ip route add 192.168.1.0/24 dev R3-eth2 via 192.168.6.1")
        net["R3"].cmd("ip route add 192.168.2.0/24 dev R3-eth1 via 192.168.5.1")
        r = net.pingAll()
        
        print(r)
       
        net.stop()
        with open('state6.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" in state
    finally:
        cleanup()
