import pytest
import json

from ipmininet.ipnet import IPNet
from ipmininet.inginious import IPmininetUnitTest
from mininet.log import lg as log

from ipmininet.topologydb import TopologyDB

class Test_TwoPCLAN:
    """ Test TwoPCLAN exercices """
    def __init__(self, net, family, subnet, prefixlen):
        self.net = net
        self.subnet = subnet
        self.family = family
        self.prefixlen = prefixlen
    
    def getlgprefm(self, k:str, j:str, rbits):
        r = 0
        if rbits > 8:
            nbits = 8
        else:
            nbits = rbits
        for i in range(nbits):
            if k[i] != j[i]:
                return r
            r+=1
        return r
        
    def checksubnet_addr(self):
        for h in self.net.hosts:
            cmd = "ip -j addr show"
            r = h.cmd(cmd)
            jr = json.loads(r)
            for data in jr :
                if data['ifname'] == "lo":
                    continue
                for addrinfo in data['addr_info']:
                    if addrinfo['family'] == self.family:
                        if int(addrinfo['prefixlen']) != int(self.prefixlen):
                            return "Failed", "Prefixlen does not match"
                        ip_blocks = addrinfo['local'].split(".")
                        subnet_blocks = self.subnet.split(".")
                        i = 0
                        ip_blocks_bin = ["0".zfill(8), "0".zfill(8), "0".zfill(8), "0".zfill(8)]
                        subnet_blocks_bin = ["0".zfill(8), "0".zfill(8), "0".zfill(8), "0".zfill(8)]
                        prefm = 0
                        for ip_block, subnet_block in zip(ip_blocks, subnet_blocks):
                            ip_blocks_bin[i] = bin(int(ip_block,10))[2:].zfill(8)
                            subnet_blocks_bin[i] = bin(int(subnet_block,10))[2:].zfill(8)
                            i+=1
                        for k, j in zip(ip_blocks_bin, subnet_blocks_bin) :
                            rbits =  int(self.prefixlen) - prefm
                            r = self.getlgprefm(k, j, rbits)
                            prefm += r
                            if(r != 8):
                                break;
                        if prefm != self.prefixlen:
                            return "Failed", "address prefix does not match"                 
        return "Success", "Bravo"
