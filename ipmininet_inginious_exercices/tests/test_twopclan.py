"""This module tests twopclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.twopclan import TwoPCLAN
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_TwoPCLAN_IPv4():
    try:
        family = "6"
        net = IPNet(topo=TwoPCLAN("4", "192.168.1.0", "24") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "192.168.1.1/24"
        itf1.prefixLen == 24
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip = "192.168.1.2/24"
        itf2.prefixLen == 24
        
        net.stop()
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert state == "Success"
    finally:
        cleanup()
        
        
 
@require_root
def test_TwoPCLAN_IPv6():
    try:
        net = IPNet(topo=TwoPCLAN("6", "fc00:0:2::", "48") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip6 = "fc00:0:2::1/48"
        itf1.prefixLen6 == 48
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip6 = "fc00:0:2::2/48"
        itf2.prefixLen6 == 48
       
        net.stop()
        
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()   
        assert state == "Success"
    finally:
        cleanup()
        

@require_root
def test_TwoPCLAN_IPv4_wrongIP():
    try:
        family = "6"
        net = IPNet(topo=TwoPCLAN("4", "192.168.1.0", "24") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "192.168.3.1/24"
        itf1.prefixLen == 24
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip = "192.168.5.2/24"
        itf2.prefixLen == 24
        
        net.stop()
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()    
        assert state == "Failed"
    finally:
        cleanup()
        
        
 
@require_root
def test_TwoPCLAN_IPv6_wrongIP():
    try:
        net = IPNet(topo=TwoPCLAN("6", "fc00:0:2::", "48") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip6 = "fc00:1:4::1/48"
        itf1.prefixLen6 == 48
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip6 = "fc00:2:4::2/48"
        itf2.prefixLen6 == 48
       
        net.stop()
        
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()  
        assert state == "Failed"
    finally:
        cleanup()
        

@require_root
def test_TwoPCLAN_IPv6_wrongPrefixlen():
    try:
        net = IPNet(topo=TwoPCLAN("6", "fc00:0:2::", "48") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip6 = "fc00:0:2::1/64"
        itf1.prefixLen6 == 64
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip6 = "fc00:0:2::2/64"
        itf2.prefixLen6 == 64
       
        net.stop()
        
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()  
        assert state == "Failed"
    finally:
        cleanup()
        

@require_root
def test_TwoPCLAN_IPv4_wrongPrefixlen():
    try:
        family = "6"
        net = IPNet(topo=TwoPCLAN("4", "192.168.1.0", "24") \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "192.168.1.1/26"
        itf1.prefixLen == 26
        
        
        itf2 = net["h2"].intf("h2-eth0")
        itf2.ip = "192.168.1.2/26"
        itf2.prefixLen == 26
        
        net.stop()
        with open('state.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()    
        assert state == "Failed"
    finally:
        cleanup()
