# Redis Spec File




## Commands 

```shell script

yum install -y centos-release-scl && yum install -y devtoolset-7

# Enable environment
$ scl enable devtoolset-7 bash

$ diff -up redis.conf.orig redis.conf

```


## Issues
 - [Blog :: Fix centos7 build redis 6 return error](https://www.limstash.com/en/articles/202005/1638)