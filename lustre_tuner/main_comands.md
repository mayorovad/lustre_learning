##Команды для поднятия, настройки сервера

```
cd ~/lustre-release/

rpm -ivh lustre-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm

rpm -ivh kernel-debuginfo-common-x86_64-2.6.32-431.23.3.el6_lustre.x86_64.rpm

rpm -ivh kernel-debuginfo-2.6.32-431.23.3.el6_lustre.x86_64.rpm

rpm -ivh lustre-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh lustre-modules-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh —oldpackage kernel-2.6.32-431.23.3.el6_lustre.x86_

rpm -ivh lustre-modules-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh lustre-osd-ldiskfs-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh —replacefiles libcom_err-1.42.13.wc3-7.el6.x86_64.rpm

rpm -ivh —replacefiles e2fsprogs-1.42.13.wc3-7.el6.x86_64.rpm

rpm -ivh —replacefiles lustre-osd-ldiskfs-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh lustre-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

yum install sg3_utils

rpm -ivh lustre-iokit-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

yum install openmpi

rpm -ivh lustre-tests-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh lustre-source-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

rpm -ivh —replacefiles lustre-2.5.3-2.6.32_431.23.3.el6_lustre.x86_64.x86_64.rpm

mount -t lustre 10.42.43.10@tcp:/mds1/client /mnt
109 modprobe lnet

yum install openssh-server openssh-clients rsh xinetd

iptables -I INPUT -p tcp --dport 988 -m state --state NEW -j ACCEPT

service iptables save

/etc/init.d/iptables restart

service xinetd restart

echo "<IP адрес eth или wlan>           localhost.localdomain localhost" >> /etc/hosts

echo -e "options lnet networks=tcp0(eth0)\noptions lnet accept=all" > /etc/modprobe.d/lnet.conf

modprobe lnet

lctl network up

modprobe lustre

tunefs.lustre --erase-param --mgsnode=IPADDR --writeconf /dev/sda

tunefs.lustre --param="failover.node=IPADDR@tcp0" /dev/sda

mkfs.lustre --mdt --mgs --index=0 --fsname=orionfs /dev/sdb

mount -t lustre /dev/sdb /mnt/mdt

mkfs.lustre --ost --index=0 --mgsnode=localhost@tcp0 --fsname=orionfs /dev/sdc

mount -t lustre /dev/sdc /mnt/ost1

mdadm --create <array_device> -c <chunksize> -l \ <raid_level> -n <active_disks> -x <spare_disks> <block_devices>

mdadm --create <array_device> -l <raid_level> -n \<active_devices> -x <spare_devices> <block_devices>

lfs df

df -t lustre
```

##Команды для клиента

```
cd ~/lustre-release

rpmbuild --rebuild --without servers <lustre version>.src.rpm

yum install openssh-server openssh-clients rsh xinetd

iptables -I INPUT -p tcp --dport 988 -m state --state NEW -j ACCEPT

service iptables save

/etc/init.d/iptables restart

service xinetd restart

echo "<IP адрес eth или wlan>           localhost.localdomain localhost" >> /etc/hosts

echo -e "options lnet networks=tcp0(eth0)\noptions lnet accept=all" > /etc/modprobe.d/lnet.conf

modprobe lnet

lctl network up

modprobe lustre

mount -t lustre <IP mds_node>@tcp0:/lustre /mnt
```