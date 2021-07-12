"""This module tests debugtraceroute.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.debugtraceroute import DebugTraceroute
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_DebugTraceroute_ipv6_1():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.51.0.0", "10.62.0.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=DebugTraceroute(ipv6addr, ipv4addr, "debugT1.txt", "debugF1.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip -6 route add 2042:2b::/64 nexthop via 2042:12::2")
        net["r2"].cmd("ip -6 route add 2042:2b::/64 nexthop via 2042:23::3")
    
        net["r2"].cmd("ip -6 route add 2042:1a::/64 nexthop via 2042:12::1")

        net["r3"].cmd("ip -6 route add 2042:1a::/64 nexthop via 2042:13::1")
        
        net["r1"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.12.0.2")
        net["r2"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.23.0.3")
    
        net["r2"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.12.0.1")
        net["r3"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.13.0.1")

        net.stop()
        with open('debugT1.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()
        

@require_root
def test_DebugTraceroute_ipv6_2():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.51.0.0", "10.62.0.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=DebugTraceroute(ipv6addr, ipv4addr, "debugT2.txt", "debugF2.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip -6 route add 2042:2b::/64 nexthop via 2042:12::2")
        net["r2"].cmd("ip -6 route add 2042:2b::/64 nexthop via 2042:23::3")
    
        net["r3"].cmd("ip -6 route add 2042:1a::/64 nexthop via 2042:13::1")
        
        net["r1"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.12.0.2")
        net["r2"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.23.0.3")
    
        net["r3"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.13.0.1")

        net.stop()
        with open('debugT2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" in state
    finally:
        cleanup()
        
"""
@require_root
def test_DebugTraceroute_ipv4_1():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.51.0.0", "10.62.0.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=DebugTraceroute(ipv6addr, ipv4addr, "debugT4.txt", "debugF4.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.12.0.2")
        net["r2"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.23.0.3")
    
        net["r2"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.12.0.1")
        net["r3"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.13.0.1")

        net.stop()
        with open('debugT3.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()
        

@require_root
def test_DebugTraceroute_ipv4_2():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.51.0.0", "10.62.0.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=DebugTraceroute(ipv6addr, ipv4addr, "debugT4.txt", "debugF4.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.12.0.2")
        net["r2"].cmd("ip  route add 10.62.0.0/24 nexthop via 10.23.0.3")
    
        net["r3"].cmd("ip  route add 10.51.0.0/24 nexthop via 10.13.0.1")

        net.stop()
        with open('debugT4.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" in state
    finally:
        cleanup()
"""
