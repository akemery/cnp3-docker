"""This module tests twopclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.asymetricrouting import AsymetricRouting
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_AsymetricRouting():
    subnet=["192.168.1.0", "192.168.2.0", "192.168.3.0", "192.168.4.0", \
             "192.168.5.0", "192.168.6.0"]
    prefixlen=["24", "24", "24", "24", "24", "24"]
    gw=["192.168.1.1", "192.168.2.1"]
    try:
        net = IPNet(topo=AsymetricRouting("4", subnet, prefixlen, gw) \
                 , use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        
        net["A"].cmd("ip route add default via 192.168.1.1")
        net["B"].cmd("ip route add default via 192.168.1.1")
         
        net["R1"].cmd("ip route add 192.168.2.0/24 dev R1-eth1 via 192.168.3.2")
        net["R1"].cmd("ip route add 192.168.4.0/24 dev R1-eth1 via 192.168.3.2")
        net["R1"].cmd("ip route add 192.168.5.0/24 dev R1-eth2 via 192.168.6.2")
        
        net["R2"].cmd("ip route add 192.168.1.0/24 dev R2-eth0 via 192.168.3.1")
        net["R2"].cmd("ip route add 192.168.2.0/24 dev R2-eth1 via 192.168.4.2")
        net["R2"].cmd("ip route add 192.168.5.0/24 dev R2-eth1 via 192.168.4.2")
        net["R2"].cmd("ip route add 192.168.6.0/24 dev R2-eth0 via 192.168.3.1")
        
        net["R3"].cmd("ip route add 192.168.1.0/24 dev R3-eth0 via 192.168.6.1")
        net["R3"].cmd("ip route add 192.168.2.0/24 dev R3-eth1 via 192.168.5.2")
        net["R3"].cmd("ip route add 192.168.3.0/24 dev R3-eth0 via 192.168.6.1")
        net["R3"].cmd("ip route add 192.168.4.0/24 dev R3-eth1 via 192.168.5.2")
        
        net["R4"].cmd("ip route add 192.168.1.0/24 dev R4-eth2 via 192.168.5.1")
        net["R4"].cmd("ip route add 192.168.3.0/24 dev R4-eth1 via 192.168.4.1")
        net["R4"].cmd("ip route add 192.168.6.0/24 dev R4-eth2 via 192.168.5.1")
        
        
        net.stop()
        with open('state3.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()
"""        
@require_root
def test_LANWith3Routers_IPv6():
    subnet=["fc00:0:1::", "fc00:0:2::", "fc00:0:3::", "fc00:0:4::", \
             "fc00:0:5::", "fc00:0:6::"]
    prefixlen=["48", "48", "48", "48", "48", "48"]
    gw=["fc00:0:1::1", "fc00:0:2::1", "fc00:0:3::1"]
    try:
        net = IPNet(topo=LANWith3Routers("6", subnet, prefixlen, gw)  \
                  , use_v4=False, use_v6=False, allocate_IPs=False)
                  
        net.start()
        
        itf1 = net["h1"].intf("h1-eth0")
        itf1.ip = "fc00:0:1::2/48"
        itf1.prefixLen == 48
        
        
        itf2 = net["r1"].intf("r1-eth0")
        itf2.ip = "fc00:0:1::1/48"
        itf2.prefixLen == 48
        
        net["h1"].cmd("ip -6 route add default via fc00:0:1::1")
        
        itf3 = net["h2"].intf("h2-eth0")
        itf3.ip = "fc00:0:2::2/48"
        itf3.prefixLen == 48
        
        
        itf4 = net["r2"].intf("r2-eth0")
        itf4.ip = "fc00:0:2::1/48"
        itf4.prefixLen == 48
        
        net["h2"].cmd("ip -6 route add default via fc00:0:2::1")
        
        
        itf5 = net["h3"].intf("h3-eth0")
        itf5.ip = "fc00:0:3::2/48"
        itf5.prefixLen == 48
        
        
        itf6 = net["r3"].intf("r3-eth0")
        itf6.ip = "fc00:0:3::1/48"
        itf6.prefixLen == 48
        
        net["h3"].cmd("ip -6 route add default via fc00:0:3::1")
        
        
        itf7 = net["r1"].intf("r1-eth1")
        itf7.ip = "fc00:0:4::1/48"
        itf7.prefixLen == 48
        
        itf8 = net["r2"].intf("r2-eth1")
        itf8.ip = "fc00:0:4::2/48"
        itf8.prefixLen == 48
        
        itf9 = net["r2"].intf("r2-eth2")
        itf9.ip = "fc00:0:5::1/48"
        itf9.prefixLen == 48
        
        itf10 = net["r3"].intf("r3-eth1")
        itf10.ip = "fc00:0:5::2/48"
        itf10.prefixLen == 48
        
        itf11 = net["r1"].intf("r1-eth2")
        itf11.ip = "fc00:0:6::1/48"
        itf11.prefixLen == 48
        
        itf10 = net["r3"].intf("r3-eth2")
        itf10.ip = "fc00:0:6::2/48"
        itf10.prefixLen == 48
        
        net.stop()
        with open('state3.txt', 'r') as f:
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
        
"""
