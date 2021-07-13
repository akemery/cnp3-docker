from ipmininet.iptopo import IPTopo
from ipmininet.router.config import RouterConfig
from ipmininet.ipnet import IPNet
from ipmininet.cli import IPCLI
import ipaddress
import os
import sys
import gettext

from mininet.log import lg

src_dir = os.path.dirname(__file__)

inginious_dir = os.path.join( src_dir, '..', 'inginious')

sys.path.append(inginious_dir)

from inginious.grader import Grader

_ = gettext.gettext
""" 
In the following topology, ping does not perform well.
                        P2
             P0 h1---R1 --R2
                     +   /
                  P3 +  / P4
                     + /     
              P1 h2---R3
Can you fix that?
"""

class LongestPrefixMatch(IPTopo):

    def __init__(self, ipv6addr=[], ipv4addr=[], statelog="", feedbacklog="", *args, **kwargs):
        self.ipv6addr = ipv6addr
        self.ipv4addr = ipv4addr
        self.statelog = statelog
        self.feedbacklog = feedbacklog
        super().__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        
        r1 = self.addRouter("r1", config=RouterConfig)
        r2 = self.addRouter("r2", config=RouterConfig)
        r3 = self.addRouter("r3", config=RouterConfig)


        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")

        
        
        lr1h1 = self.addLink(r1, h1)
        lr1h1[r1].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[0])+1)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[0])+1)+"/24"))
        lr1h1[h1].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[0])+0xa)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[0])+11)+"/24"))

        lr2h2 = self.addLink(r2, h2)
        lr2h2[r2].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[1])+3)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[1])+2)+"/24"))
        lr2h2[h2].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[1])+0xb)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[1])+22)+"/24"))
                            
        lr3h3 = self.addLink(r3, h3)
        lr3h3[r3].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[2])+1)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[2])+3)+"/24"))
        lr3h3[h3].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[2])+0xc)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[2])+33)+"/24"))


        lr1r2 = self.addLink(r1, r2)
        lr1r2[r1].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[3])+1)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[3])+1)+"/24"))
        lr1r2[r2].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[3])+2)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[3])+2)+"/24"))
                            
        lr1r3 = self.addLink(r1, r3)
        lr1r3[r1].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[4])+1)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[4])+1)+"/24"))
        lr1r3[r3].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[4])+3)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[4])+3)+"/24"))
                            
        lr2r3 = self.addLink(r2, r3)
        lr2r3[r2].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[5])+2)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[5])+2)+"/24"))
        lr2r3[r3].addParams(ip=(str(ipaddress.ip_address(self.ipv6addr[4])+3)+"/64", \
                            str(ipaddress.ip_address(self.ipv4addr[5])+3)+"/24"))


        
        super(LongestPrefixMatch, self).build(*args, **kwargs)
        
    def pre_stop(self, net):
        test = Grader(net)
        
        answer = ['10.1.4.1', '10.13.0.3', '10.1.6.33']
        state, feedback = test.traceroute("h1", "10.1.6.33", 50, answer)
        print(state, file=open(self.statelog, "a"))
        print(feedback, file=open(self.feedbacklog, "a"))
        answer = ['10.1.6.3', '10.13.0.1', '10.1.4.11']
        state, feedback = test.traceroute("h3", "10.1.4.11", 50, answer)
        print(state, file=open(self.statelog, "a"))
        print(feedback, file=open(self.feedbacklog, "a"))
   
        super(LongestPrefixMatch, self).pre_stop(net)
        
"""
    ping ok traceroute not ok   
    net["r1"].cmd("ip -4 route add  10.1.4.0/22 via 10.12.0.2")
    net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
    net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
    net["r3"].cmd("ip -4 route add  10.1.4.0/22 via 10.23.0.2")
"""


"""
    ping ok traceroute not ok
    net["r1"].cmd("ip -4 route add  10.1.4.0/22 via 10.12.0.2")
    net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
    net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
    net["r3"].cmd("ip -4 route add  10.1.4.0/24 via 10.13.0.1")
    net["r3"].cmd("ip -4 route add  10.1.5.0/24 via 10.23.0.2")
"""

"""       
ipv6addr = [ "2042:1a::", "2042:2b::", "2042:3c::", "2042:12::", "2042:13::", "2042:23::"]
ipv4addr = [ "10.1.4.0", "10.1.5.0", "10.1.6.0", "10.12.0.0", "10.13.0.0", "10.23.0.0"]
net = IPNet(topo=LongestPrefixMatch(ipv6addr, ipv4addr), allocate_IPs=False)  # Disable IP auto-allocation
try:
    net.start()
    
    net["r1"].cmd("ip -4 route add  10.1.5.0/24 via 10.12.0.2")
    net["r1"].cmd("ip -4 route add  10.1.6.0/24 via 10.13.0.3")
    net["r2"].cmd("ip -4 route add  10.1.4.0/24 via 10.12.0.1")
    net["r2"].cmd("ip -4 route add  10.1.6.0/24 via 10.23.0.3")
    net["r3"].cmd("ip -4 route add  10.1.4.0/24 via 10.13.0.1")
    net["r3"].cmd("ip -4 route add  10.1.5.0/24 via 10.23.0.2")
    
    IPCLI(net)
finally:
    net.stop()    
"""
