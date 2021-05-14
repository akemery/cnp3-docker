import unittest
import docker

image = sys.argv[1]

class TestDocker(unittest.TestCase):
    def setUp(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image=image, detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        self.assertNotEqual(container, None) 
        
    def test_pingall(self):
        r = container.exec_run('sudo mn --test pingall --custom ipmininet_scripts/withip.py')
        print(r)
        self.assertNotEqual(r, None)
        container.stop()
        container.remove()
    def test_pingpair(self):
        """
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image="akemery/cnp3", detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        self.assertNotEqual(container, None) 
        """
        r = container.exec_run('sudo mn --test pingpair --custom ipmininet_scripts/withip.py')
        print(r)
        self.assertNotEqual(r, None)
        container.stop()
        container.remove()
     def test_iperf(self):
        """
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image="akemery/cnp3", detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        self.assertNotEqual(container, None) 
        """
        r = container.exec_run('sudo mn --test iperf --custom ipmininet_scripts/withip.py')
        print(r)
        self.assertNotEqual(r, None)
        container.stop()
        container.remove()
     def test_iperfudp(self):
        """
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image="akemery/cnp3", detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        self.assertNotEqual(container, None)
        """ 
        r = container.exec_run('sudo mn --test iperfudp --custom ipmininet_scripts/withip.py')
        print(r)
        self.assertNotEqual(r, None)
        container.stop()
        container.remove()

if __name__ == '__main__':
    unittest.main()

