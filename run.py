import unittest
import docker
import sys

image = "akemery/cnp3"
script = "ipmininet_scripts/withip.py"

class TestDocker(unittest.TestCase):
    def setUp(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image=image, detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        self.assertNotEqual(container, None) 
        self.container = container
        
    def test_basic(self):
        command = 'sudo mn --test pingall --custom ' + script
        r = self.container.exec_run(command)
        print(r)
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
        # m command
        r = self.container.exec_run("../mininet/util/m h1 ifconfig")
        print(r)
        self.container.stop()
        self.container.remove()
            
    def tearDown(self):
        self.container.stop()
        self.container.remove()

if __name__ == '__main__':
    unittest.main()

