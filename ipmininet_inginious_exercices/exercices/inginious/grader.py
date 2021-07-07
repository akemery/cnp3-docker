import pytest
import json
import gettext

from ipmininet.ipnet import IPNet
from mininet.log import lg as log


"""
fr = gettext.translation('base', localedir='locales', languages=['fr'])
fr.install()
_ = fr.gettext # french
"""
_ = gettext.gettext

class Grader:
    """ Test TwoPCLAN exercices """
    def __init__(self, net):
        self.net = net
    
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
        
    def getprefixlenmatch (self, family, ipaddr, subnet_addr, prefixlen):
        prefm = 0
        if family == "inet":
            ip_blocks = ipaddr.split(".")
            subnet_blocks = subnet_addr.split(".")
            i = 0
            ip_blocks_bin = ["0".zfill(8), "0".zfill(8), "0".zfill(8), "0".zfill(8)]
            subnet_blocks_bin = ["0".zfill(8), "0".zfill(8), "0".zfill(8), "0".zfill(8)]
            for ip_block, subnet_block in zip(ip_blocks, subnet_blocks):
                ip_blocks_bin[i] = bin(int(ip_block,10))[2:].zfill(8)
                subnet_blocks_bin[i] = bin(int(subnet_block,10))[2:].zfill(8)
                i+=1
            for k, j in zip(ip_blocks_bin, subnet_blocks_bin) :
                rbits =  int(prefixlen) - prefm
                r = self.getlgprefm(k, j, rbits, 8)
                prefm += r
                if(r != 8):
                    break;
        else :
            ip_blocks = ipaddr.split(":")
            subnet_blocks = subnet_addr.split(":")
            i = 7
            ip_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                             "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                             "0".zfill(16), "0".zfill(16)]
            subnet_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                 "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                 "0".zfill(16), "0".zfill(16)]
            for ip_block, subnet_block in zip(ip_blocks, subnet_blocks):
                if (ip_block == '') or ( "/" in ip_block )  \
                    or (subnet_block == '') or ( "/" in subnet_block ):
                    i = 0
                    continue
                ip_blocks_bin[i] = bin(int(ip_block,16))[2:].zfill(16)
                subnet_blocks_bin[i] = bin(int(subnet_block,16))[2:].zfill(16)
                print(ip_blocks_bin[i])
                print(subnet_blocks_bin[i])
                i-=1
            for k, j in zip(ip_blocks_bin, subnet_blocks_bin) :
                rbits =  int(prefixlen) - prefm
                r = self.getlgprefm(k, j, rbits, 16)
                prefm += r
                if(r != 16):
                   break;           
        return prefm
        
    def checksubnet_addr(self, family, subnet, prefixlen, hosts=[], routers=[]):
        found_addr = False
        state = "Failed"
        feedback = "Addresses are not configured, retry please"
        for h in self.net.hosts:
            if h.name not in hosts:
                continue
            cmd = "ip -j addr show"
            r = h.cmd(cmd)
            jr = json.loads(r)
            for data in jr :
                if data['ifname'] == "lo":
                    continue
                for addrinfo in data['addr_info']:
                    if family == "4":
                        if addrinfo['family'] != "inet":
                            continue
                        if int(addrinfo['prefixlen']) != int(prefixlen):
                            state = _("Failed") 
                            feedback = _("IPv4 Prefixlen does not match")
                        prefm = self.getprefixlenmatch ("inet", addrinfo['local'], subnet, prefixlen)
                        if (prefm != int(prefixlen)):
                                state = _("Failed")
                                feedback =  _("IPv4 address prefix does not match")
                        found_addr = True
                    else:
                        if family == "6":
                            if addrinfo['scope'] == 'link':
                                continue
                            if addrinfo['family'] != "inet6":
                                continue
                            if int(addrinfo['prefixlen']) != int(prefixlen):
                                state = _("Failed")
                                feedback = _("IPV6 Prefixlen does not match")
                            prefm = self.getprefixlenmatch ("inet6", addrinfo['local'], subnet, prefixlen)
                            if (prefm != int(prefixlen)):
                                state = _("Failed") 
                                feedback = _("IPV6 address prefix does not match")
                            found_addr = True
                        else:
                            state = _("Failed")
                            feedback = _("Bad input arguments")
        if found_addr:                                     
            return _("Success"), _("Congratulation")
        else:
            return state, feedback
            
    def check_ipaddr(self, family, subnet, prefixlen, hosts=[], routers=[]):
        for h in self.net.hosts:
            if h.name not in hosts:
                continue
            intfNames = h.intfNames()
            for intfName in intfNames:
                itf = self.net[h.name].intf(intfName)
                itf.ip = "192.168.5.2/24"
                print(itf.prefixLen) 
                
                
    def check_default_route(self, family, gw, nodes=[]):
        for h in self.hosts:
            if h.name not in nodes:
                continue
            if family == "4":
                cmd = "ip -j route show"
            else:
                cmd = "ip -6 -j route show"
            r = h.cmd(cmd)
            jr = json.loads(r)
            print(jr)
