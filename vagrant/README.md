## To start the VM
```
vagrant up

```

## To update packages on the VM

```
vagrant provision

```

## Some known issues

```
Error while connecting to libvirt: Error making a connection to libvirt URI qemu:///system?no_verify=1&keyfile=/root/.ssh/id_rsa:
Call to virConnectOpen failed: Failed to connect socket to '/var/run/libvirt/libvirt-sock': No such file or directory
```

```
sudo apt install qemu qemu-kvm libvirt-clients libvirt-daemon-system virtinst bridge-utils

sudo systemctl enable libvirtd
sudo systemctl start libvirtd

```

the server inginious listens on port 7070, so open `http://localhost on your browser`
