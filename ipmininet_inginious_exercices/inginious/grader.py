import pytest
import json
import gettext

from ipmininet.ipnet import IPNet
from ipmininet.inginious import IPmininetUnitTest
from mininet.log import lg as log

from ipmininet.topologydb import TopologyDB

fr = gettext.translation('base', localedir='locales', languages=['fr'])
fr.install()
_ = fr.gettext # french


class Grader:
    """ Test TwoPCLAN exercices """
    def __init__(self, net, family, subnet, prefixlen):
        self.net = net
        self.subnet = subnet
        self.family = family
        self.prefixlen = prefixlen
    
    def getlgprefm(self, k:str, j:str, rbits, rsize):
        r = 0
        if rbits > rsize:
            nbits = rsize
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
                    if self.family == "4":
                        if addrinfo['family'] != "inet":
                            continue
                        if int(addrinfo['prefixlen']) != int(self.prefixlen):
                            return _("Failed"), _("IPV4 Prefixlen does not match")
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
                            r = self.getlgprefm(k, j, rbits, 8)
                            prefm += r
                            if(r != 8):
                                break;
                        if prefm != int(self.prefixlen):
                            return _("Failed"), _("IPV4 address prefix does not match")
                    else:
                        if self.family == "6":
                            if addrinfo['scope'] == 'link':
                                continue
                            if addrinfo['family'] != "inet6":
                                continue
                            if int(addrinfo['prefixlen']) != int(self.prefixlen):
                                return _("Failed"), _("IPV6 Prefixlen does not match")
                            ip_blocks = addrinfo['local'].split(":")
                            subnet_blocks = self.subnet.split(":")
                            i = 7
                            ip_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16)]
                            subnet_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16)]
                            prefm = 0
                            for ip_block, subnet_block in zip(ip_blocks, subnet_blocks):
                                if (ip_block == '') or ( "/" in ip_block )  \
                                  or (subnet_block == '') or ( "/" in subnet_block ):
                                    i = 0
                                    continue
                                ip_blocks_bin[i] = bin(int(ip_block,16))[2:].zfill(16)
                                subnet_blocks_bin[i] = bin(int(subnet_block,16))[2:].zfill(16)
                                i-=1
                            for k, j in zip(ip_blocks_bin, subnet_blocks_bin) :
                                rbits =  int(self.prefixlen) - prefm
                                r = self.getlgprefm(k, j, rbits, 16)
                                prefm += r
                                if(r != 16):
                                    break;
                            if (prefm != int(self.prefixlen)):
                                return _("Failed"), _("IPV6 address prefix does not match")
                        
                        else:
                            return _("Failed"), _("Bad input arguments")                 
        return _("Success"), _("Congratulation")
