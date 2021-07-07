"""This module tests twopclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.twopclanwithrouter import TwoPCLANWithRouter
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_TwoPCLANWithRouter_IPv4():
    try:
        net = IPNet(topo=TwoPCLANWithRouter("4", "192.168.1.0", "24", \
                  "192.168.1.1", "192.168.2.0", "24", "192.168.2.1")  \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "192.168.1.2/24"
        itf1.prefixLen == 24
        
        
        
        itf2 = net["r"].intf("r-eth0")
        itf2.ip = "192.168.1.1/24"
        itf2.prefixLen == 24
        
        r = net["h1"].cmd("ip route add default via 192.168.1.1")
        
        
        itf3 = net["h2"].intf("h2-eth0")
        itf3.ip = "192.168.2.2/24"
        itf3.prefixLen == 24
        
        
        itf4 = net["r"].intf("r-eth1")
        itf4.ip = "192.168.2.1/24"
        itf4.prefixLen == 24
        
        r = net["h2"].cmd("ip route add default via 192.168.2.1")
         
        net.stop()
        with open('state2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()
        

@require_root
def test_TwoPCLANWithRouter_IPv6():
    try:
        net = IPNet(topo=TwoPCLANWithRouter("6", "fc00:0:1::", "48", \
                  "fc00:0:1::1", "fc00:0:2::", "48", "fc00:0:2::1")  \
                  , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "fc00:0:1::2/48"
        itf1.prefixLen == 48
        
        
        itf2 = net["r"].intf("r-eth0")
        itf2.ip = "fc00:0:1::1/48"
        itf2.prefixLen == 48
        
        r = net["h1"].cmd("ip -6 route add default via fc00:0:1::1")
        
        itf3 = net["h2"].intf("h2-eth0")
        itf3.ip = "fc00:0:2::2/48"
        itf3.prefixLen == 48
        
        
        itf4 = net["r"].intf("r-eth1")
        itf4.ip = "fc00:0:2::1/48"
        itf4.prefixLen == 48
        
        r = net["h2"].cmd("ip -6 route add default via fc00:0:2::1")
        
        net.stop()
        with open('state2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()


@require_root
def test_TwoPCLANWithRouter_IPv4_wrong_gw():
    try:
        net = IPNet(topo=TwoPCLANWithRouter("4", "192.168.1.0", "24", \
                  "192.168.1.1", "192.168.2.0", "24", "192.168.2.1")  \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "192.168.1.2/24"
        itf1.prefixLen == 24
        
        
        
        itf2 = net["r"].intf("r-eth0")
        itf2.ip = "192.168.1.1/24"
        itf2.prefixLen == 24
        
        r = net["h1"].cmd("ip route add default via 192.168.2.1")
        
        
        itf3 = net["h2"].intf("h2-eth0")
        itf3.ip = "192.168.2.2/24"
        itf3.prefixLen == 24
        
        
        itf4 = net["r"].intf("r-eth1")
        itf4.ip = "192.168.2.1/24"
        itf4.prefixLen == 24
        
        r = net["h2"].cmd("ip route add default via 192.168.1.1")
         
        net.stop()
        with open('state2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" in state
    finally:
        cleanup()
        
        
@require_root
def test_TwoPCLANWithRouter_IPv6_wrong_gw():
    try:
        net = IPNet(topo=TwoPCLANWithRouter("6", "fc00:0:1::", "48", \
                  "fc00:0:1::1", "fc00:0:2::", "48", "fc00:0:2::1")  \
                  , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "fc00:0:1::2/48"
        itf1.prefixLen == 48
        
        
        itf2 = net["r"].intf("r-eth0")
        itf2.ip = "fc00:0:1::1/48"
        itf2.prefixLen == 48
        
        r = net["h1"].cmd("ip -6 route add default via fc00:0:2::1")
        
        itf3 = net["h2"].intf("h2-eth0")
        itf3.ip = "fc00:0:2::2/48"
        itf3.prefixLen == 48
        
        
        itf4 = net["r"].intf("r-eth1")
        itf4.ip = "fc00:0:2::1/48"
        itf4.prefixLen == 48
        
        r = net["h2"].cmd("ip -6 route add default via fc00:0:1::1")
        
        net.stop()
        with open('state2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" in state
    finally:
        cleanup()
