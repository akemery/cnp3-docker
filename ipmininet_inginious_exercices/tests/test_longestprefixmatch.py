"""This module tests debugtraceroute.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.longestprefixmatch import LongestPrefixMatch
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo


@require_root
def test_LongestPrefixMatch_ipv4_1():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:3c::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.1.4.0", "10.1.5.0", "10.1.6.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=LongestPrefixMatch(ipv6addr, ipv4addr, "logT1.txt", "logF1.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip -4 route add  10.1.5.0/24 via 10.12.0.2")
        net["r1"].cmd("ip -4 route add  10.1.6.0/24 via 10.13.0.3")
        net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
        net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
        net["r3"].cmd("ip -4 route add  10.1.4.0/24 via 10.13.0.1")
        net["r3"].cmd("ip -4 route add  10.1.5.0/24 via 10.23.0.2")
        net.stop()
        with open('logT1.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed" not in state
    finally:
        cleanup()

@require_root
def test_LongestPrefixMatch_failed_1():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:3c::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.1.4.0", "10.1.5.0", "10.1.6.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=LongestPrefixMatch(ipv6addr, ipv4addr, "logFT1.txt", "logFF1.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip -4 route add  10.1.4.0/22 via 10.12.0.2")
        net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
        net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
        net["r3"].cmd("ip -4 route add  10.1.4.0/22 via 10.23.0.2")
        net.stop()
        with open('logFT1.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed"  in state
    finally:
        cleanup()
        
        
@require_root
def test_LongestPrefixMatch_failed_2():
    ipv6addr = [ "2042:1a::", "2042:2b::", "2042:3c::", "2042:12::", "2042:13::", "2042:23::"]
    ipv4addr = [ "10.1.4.0", "10.1.5.0", "10.1.6.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
    net = IPNet(topo=LongestPrefixMatch(ipv6addr, ipv4addr, "logFT2.txt", "logFF2.txt"), allocate_IPs=False)  
    try:
        net.start()
        net["r1"].cmd("ip -4 route add  10.1.4.0/22 via 10.12.0.2")
        net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
        net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
        net["r3"].cmd("ip -4 route add  10.1.4.0/24 via 10.13.0.1")
        net["r3"].cmd("ip -4 route add  10.1.5.0/24 via 10.23.0.2")
        net.stop()
        with open('logFT2.txt', 'r') as f:
            state = f.read().replace('\n', '')
        f.close()
        assert "Failed"  in state
    finally:
        cleanup()
        
