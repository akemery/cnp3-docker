import pytest
import json
import gettext
import ipaddress
from ipmininet.ipnet import IPNet
from mininet.log import lg as log

from ipmininet.topologydb import TopologyDB
from ipmininet.tests.utils import traceroute


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
    
    def getlgprefm(self, k:str, j:str, rbits=16, rsize=16):
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
        
    def getConnectedRouter(self, srcRouter:str, intF:str):
        db = TopologyDB(net=self.net)
        _Network = db.getNetwork()
        dict1 = _Network[srcRouter]
        for data in dict1:
            if self.isRouterName(data) :
                if dict1[data]['name'] == intF:
                    return data
        for data in dict1:
            if self.isHostName(data) :
                if dict1[data]['name'] == intF:
                    return data  
        return None 
        
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
               
               
               
    def check_default_route(self, family, gw,  nodes=[], isRouters=False):
        found_gw = False
        state = _("Failed")
        feedback = _("Gateway is not correctly configured")
        if isRouters :
            m = self.net.routers
        else:
            m = self.net.hosts
        for h in m:
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
                if "gateway" in data :
                    if data['dst'] == "default":
                        gateway = ipaddress.ip_address(data['gateway'])
                        if gateway == ipaddress.ip_address(gw):
                            found_gw = True
                """
                finally:
                    continue
                """
        if found_gw :                                     
            return _("Success"), _("Congratulation")
        else:
            return state, feedback 
            
    def check_static_route(self, family, dst=[], outIntf=[], nexthopIP=[], nodes=[]):
        state = _("Success")
        feedback = _("Route is correctly configured")
        for router in self.net.routers:
            if router.name not in nodes:
                continue
            if family == "4":
                cmd = "ip -j route show"
            else:
                cmd = "ip -6 -j route show"
            r = router.cmd(cmd)
            jr = json.loads(r)
            for data in jr:
                if dst[0] == data['dst'] :
                    if (data['dev'] != outIntf[0]) or (data['gateway'] != nexthopIP[0]):
                        state == _("Failed")
                        feedback == _("Route is not correctly configured")
                if dst[1] == data['dst'] :
                    if (data['dev'] != outIntf[1]) or (data['gateway'] != nexthopIP[1]):
                        state == _("Failed")
                        feedback == _("Route is not correctly configured")
        return state, feedback
        
    def check_ecmp_route(self, family, dst, outIntf=[], nexthopIP=[], nodes=[]):
        state = _("Success")
        feedback = _("Route is correctly configured")
        for router in self.net.routers:
            if router.name not in nodes:
                continue
            if family == "4":
                cmd = "ip -j route show"
            else:
                cmd = "ip -6 -j route show"
            r = router.cmd(cmd)
            jr = json.loads(r)
            for data in jr:
                if dst == data['dst']:
                    if "nexthops" in data :
                        for nexthop in data['nexthops']:
                            if (nexthop['dev'] != outIntf[0]) or (nexthop['gateway'] != nexthopIP[0]):
                                state == _("Failed")
                                feedback == _("Route is not correctly configured")
                            if (nexthop['dev'] != outIntf[1]) or (nexthop['gateway'] != nexthopIP[1]):
                                state == _("Failed")
                                feedback == _("Route is not correctly configured")
                    """            
                    finally:
                        continue
                    """   
        return state, feedback
    
    def isRouterName(self, name:str):
        for r in self.net.routers:
            if r.name == name:
                return True
        return False
    
    def isHostName(self, name:str):
        for r in self.net.hosts:
            if r.name == name:
                return True
        return False
 
    def isRouter(self, name:str):
        for r in self.net.routers:
            if r.name == name:
                return True
        return False
              
    def isNodeIP(self, name:str, dstip:str, isRouter=False):
        IPs = ""
        cmd = "ifconfig"
        if isRouter:
            for r in self.net.routers:
                if r.name == name:
                    IPs = r.cmd(cmd)
                    return dstip in IPs
        else:
            for host in self.net.hosts:
                if host.name == name:
                    IPs = host.cmd(cmd) 
                    return dstip in IPs
    
    def getOutputIntf(self, src:str, block_bin_dst=[], isRouter=False ):
        res = []
        name = src
        d = None
        lg_prefm = 0
        if isRouter == True:
            for r in self.net.routers:
                if r.name == src:
                    name = r.name
                    cmd = "ip -j -6 route show"
                    r = r.cmd(cmd)
                    jr = json.loads(r)
                    for data in jr :
                        rip_blocks = data['dst'].split(":")
                        i = 7
                        block_bin = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                                     "0".zfill(16), "0".zfill(16)]
                        prefm = 0
                        for rblock in rip_blocks :
                            if (rblock == '') or ( "/" in rblock ):
                                i = 0
                                continue
                            block_bin[i] = bin(int(rblock,16))[2:].zfill(16)
                            i-=1
                        for k, j in zip(block_bin, block_bin_dst) :
                            prefm+= self.getlgprefm(k, j)
                        if prefm > lg_prefm:
                            lg_prefm = prefm
                            d = data
        else :
            for h in self.net.hosts:
                if h.name == src:
                    name = h.name
                    cmd = "ip -j -6 route show"
                    r = h.cmd(cmd)
                    jr = json.loads(r)
                    for data in jr :
                        if data['dst'] == "default":
                            d = data
                            break
        assert(d!=None)
        try:
            if d['nexthops'] != None:
                nexthops = d['nexthops']
                for intF in nexthops:
                    res.append(intF['dev'])
            else:
                print("Not nexthop")
        except Exception as e:
            res.append(d['dev'])
        return res, name
            
    def pariTraceroute(self, src:str, dst:str, ipv6=True):
        path = []
        subintF = []
        dpath = dict()
        if ipv6:
            dstips_blocks = dst.split(":")
            block_bin_dst = ["0".zfill(16), "0".zfill(16), "0".zfill(16), \
                         "0".zfill(16), "0".zfill(16), "0".zfill(16), \
                         "0".zfill(16), "0".zfill(16)]
            i = 7 
            for block in dstips_blocks:
                if block == '':
                    continue
                block_bin_dst[i] = bin(int(block,16))[2:].zfill(16)     
                i-=1
        else:
            dstips_blocks = dst.split(".")
            block_bin_dst = \
                         ["0".zfill(8), "0".zfill(8), "0".zfill(8), "0".zfill(8)]
            i = 3
            for block in dstips_blocks:
                if block == '':
                    continue
                block_bin_dst[i] =  \
                                 bin(int(block,10))[2:].zfill(8)     
                i-=1
        router = ""
        res, router = self.getOutputIntf(src, block_bin_dst, self.isRouter(src))
        path.append(src)
        subintF.append(res) 
        isNodeIP = False
        i = 0
        for res in subintF:
            if len(res) == 0 or isNodeIP == True:
                break  
            for intF in res :
                nextres = []
                r = self.getConnectedRouter(router, intF)
                nextres, nextr = self.getOutputIntf(r, block_bin_dst, self.isRouter(r))
                path.append(nextr)
                subintF.append(nextres)
                if router in dpath.keys():
                    dpath[router] = dpath[router]+" "+r
                else :
                    dpath[router] = r
            i+=1
            # res = nextres
            router = path[i]
            isNodeIP = self.isNodeIP(router, dst, self.isRouter(router))
        return dpath    


    def traceroute(self, src: str, dst_ip: str, timeout=300, answer=[]):
        state = _("Success")
        feedback = _("Route is correctly configured")
        r = traceroute(self.net, src, dst_ip, timeout)
        print(r)
        print(answer)
        if r != answer:
           state = _("Failed")
           feedback = _("Bad answer, try again")
        return state, feedback
