FROM centos:7


COPY ./wandisco.repo     /etc/yum.repos.d/wandisco.repo

RUN yum install -y epel-release && yum update -y && yum groupinstall -y "Development Tools" \
    && yum install -y net-tools gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools createrepo \
    && yum clean all --enablerepo=* && rm -rf /var/cache/yum && rm -rf /var/cache/rpm && rm -rf /var/lib/yum/*


COPY ./tmp/rpm-build.sh  /usr/local/bin/rpm-build.sh
COPY ./local.repo        /etc/yum.repos.d/local.repo

