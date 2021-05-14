import unittest
import docker

class TestDocker(unittest.TestCase):
    """
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
    """
    def test_docker(self):
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
        self.assertNotEqual(client, None) 
        container = client.containers.run(image="akemery/cnp3", detach=True, runtime='kata-runtime', privileged=True, mem_limit='50g')
        #container.restart()
        print(container.logs())
        self.assertNotEqual(container, None) 
        r = container.exec_run('uname -a')
        print(r)
        r = container.exec_run('sudo mn --test pingall --custom ipmininet_scripts/withip.py')
        print(r)
        container.wait()
        container.stop()
        container.remove()

if __name__ == '__main__':
    unittest.main()

