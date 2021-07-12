"""This module tests threepclan.py host ip configuration exercice """
import pytest
import time 

from ipmininet.clean import cleanup
from . import require_root
from exercices.ospfcost import OSPFCost
from ipmininet.ipnet import IPNet
from ipmininet.iptopo import IPTopo



@require_root
def test_OSPFCost_Success():
    try:
        net = IPNet(topo=OSPFCost(), use_v4=False, use_v6=False, allocate_IPs=False)
        net.start()
        time.sleep(20)
        net.stop()
    finally:
        cleanup()
        

