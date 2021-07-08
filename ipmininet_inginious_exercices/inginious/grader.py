import pytest
import json
import gettext
import ipaddress
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
            ip_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                             "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                             "0".zfill(16), "0".zfill(16)]
            subnet_blocks_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                 "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                 "0".zfill(16), "0".zfill(16)]
            i = 0
            for ip_block, subnet_block in zip(ip_blocks, subnet_blocks):
                if (ip_block == '') or ( "/" in ip_block )  \
                    or (subnet_block == '') or ( "/" in subnet_block ):
                    continue
                ip_blocks_bin[i] = bin(int(ip_block,16))[2:].zfill(16)
                subnet_blocks_bin[i] = bin(int(subnet_block,16))[2:].zfill(16)
                i+=1
            for k, j in zip(ip_blocks_bin, subnet_blocks_bin) :
                rbits =  int(prefixlen) - prefm
                r = self.getlgprefm(k, j, rbits, 16)
                prefm += r
                if(r != 16):
                   break;          
        return prefm
        
    def checksubnet_addr(self, family, subnet, prefixlen, nodes=[]):
        found_addr = False
        state = _("Failed")
        feedback = _("Addresses are not configured, retry please")
        for n in nodes:
            h = None
            """ search in hosts """
            for host in self.net.hosts:
                if host.name == n:
                    h = host
                    break
            """ if notfound search in router """
            if h == None:
                for router in self.net.routers:
                    if router.name == n:
                        h = router
                        break
            """ if notfound go to the next """
            if h == None:
                continue
            print(h.name)
            cmd = "ip -j addr show"
            r = h.cmd(cmd)
            jr = json.loads(r)
            found_addr = False
            for data in jr :
                if data['ifname'] == "lo":
                    continue
                for addrinfo in data['addr_info']:
                    if family == "4":
                        if found_addr == True:
                            break;
                        if addrinfo['family'] != "inet":
                            continue
                        if int(addrinfo['prefixlen']) != int(prefixlen):
                            state = _("Failed") 
                            feedback = _("IPv4 Prefixlen does not match")
                            continue
                        prefm = self.getprefixlenmatch ("inet", addrinfo['local'], subnet, prefixlen)
                      
                        if (prefm != int(prefixlen)):
                                state = _("Failed") 
                                feedback = _("IPv4 address prefix does not match")
                                continue
                        found_addr = True
                    else:
                        if family == "6":
                            if found_addr == True:
                                break;
                            if addrinfo['scope'] == 'link':
                                continue
                            if addrinfo['family'] != "inet6":
                                continue
                            if int(addrinfo['prefixlen']) != int(prefixlen):
                                state = _("Failed")
                                feedback = _("IPV6 Prefixlen does not match")
                                continue
                            prefm = self.getprefixlenmatch ("inet6", addrinfo['local'], subnet, prefixlen)
                            if (prefm != int(prefixlen)):
                                state = _("Failed")
                                feedback = _("IPV6 address prefix does not match")
                                continue
                            found_addr = True
                        else:
                            return _("Failed"), _("Bad input arguments")
        if found_addr == True:                                     
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
        found_gw = False
        state = _("Failed")
        feedback = _("Gateway is not correctly configured")
        for h in self.net.hosts:
            if h.name not in nodes:
                continue
            if family == "4":
                cmd = "ip -j route show"
            else:
                cmd = "ip -6 -j route show"
            r = h.cmd(cmd)
            jr = json.loads(r)
            for data in jr:
                if found_gw :
                    break
                try:
                    gateway = ipaddress.ip_address(data['gateway'])
                    if gateway == ipaddress.ip_address(gw):
                        found_gw = True
                finally:
                    continue
        if found_gw :                                     
            return _("Success"), _("Congratulation")
        else:
            return state, feedback 