## pull akemery/cnp3 image from dockerhub

```
sudo docker pull akemery/cnp3
```

## build akemey/cnp3 image

```
 $ sudo docker build -t akemery/cnp3 .
```

## run akemery/cnp3 image
```
$ sudo docker run -it --privileged akemery/cnp3 bash
```

## or run with kata-runtime

```
$ sudo docker run -ti --runtime kata-runtime  --privileged  akemery/cnp3 bash
```
## run on the docker ipmininet script
```
$ python3 ipmininet_scripts/ospf6.py
```
