import unittest
import docker
import sys

image = "akemery/cnp3"
script = "ipmininet_scripts/withip.py"

class TestDocker(unittest.TestCase):
    """
    def setUp(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image=image, detach=True, runtime='kata-runtime', privileged=True, mem_limit='13g')
        self.assertNotEqual(container, None) 
        self.container = container
    """    
    def test_basic(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image="akemery/cnp3", detach=True, runtime='kata-runtime', privileged=True, mem_limit='20g', volumes=['/tmp/:/tmp/'])
        # container = client.containers.run(image="ubuntu", detach=True, command="bash")
        self.assertNotEqual(container, None) 
        print(container.logs())
        print(container.status)
        # container.wait(condition="running")
        """
        while container.status == 'created':
            r = container.exec_run(' ls /tmp/simple.log ')
            if r.exit_code == 0:
                print(r)
                exit(1)
        """        
        # self.container = container
        
        # r = container.exec_run('service openvswitch-switch start')
        # print(r)
        # command = 'sudo mn --test pingall --custom simple.py ' 
        # r = container.exec_run(command)
        # print(r)
        """
        self.assertNotEqual(r, None)
        # test_pingpair
        command = 'sudo mn --test pingpair --custom ' + script
        r = self.container.exec_run(command)
        print(r)
        self.assertNotEqual(r, None)
        # test_iperf
        command = 'sudo mn --test iperf --custom ' + script
        r = self.container.exec_run(command)
        print(r)
        self.assertNotEqual(r, None)
        #test_iperfudp
        command = 'sudo mn --test iperfudp --custom ' + script
        r = self.container.exec_run(command)
        print(r)
        self.assertNotEqual(r, None)
        """
        print(container.status)
        # r = container.exec_run(" python3 ipmininet_scripts/ospf6.py")
        # r = container.exec_run(cmd=" python3 simple.py  ", detach=True, tty=True)
        r = container.exec_run(" python3 ipmininet_scripts/ospf6.py ")
        print(r)
        """
        while container.status == 'created':
            r = container.exec_run(' ls /tmp/u.log ')
            if r.exit_code == 0:
                # print(r)
                # self.container = container
                # print(container.status)
                # m command
                r = container.exec_run(" mininet/util/m h2 ping h1 ")
                print(r)
                self.assertNotEqual(r, None)
                break
        """        
        print(container.status)
        container.stop()
        container.remove()
    """        
    def tearDown(self):
        self.container.stop()
        self.container.remove()
    """
if __name__ == '__main__':
    unittest.main()

