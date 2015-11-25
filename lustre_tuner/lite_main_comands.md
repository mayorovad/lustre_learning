Соединение
```
echo -e "options lnet networks=tcp0(eth0)\noptions lnet accept=all" > /etc/modprobe.d/lnet.conf

echo "<IP адрес eth или wlan>           localhost.localdomain localhost" >> /etc/hosts

modprobe lustre

modprobe lnet

lctl network up
```

Форматирование
```
mkfs.lustre --mdt --mgs --index=0 --fsname=orionfs /dev/sdb

mkfs.lustre --ost --index=0 --mgsnode=localhost@tcp0 --fsname=orionfs /dev/sdc
```
Монтирование
```
mount -t lustre /dev/sdb /mnt/mdt

mount -t lustre 10.42.43.10@tcp:/mds1/client /mnt
```

Изменение параметров
```
tunefs.lustre --erase-param --mgsnode=IPADDR --writeconf /dev/sda

tunefs.lustre --param="failover.node=IPADDR@tcp0" /dev/sda
```

Настройка RAID
```
mdadm --create <array_device> -c <chunksize> -l \ <raid_level> -n <active_disks> -x <spare_disks> <block_devices>

mdadm --create <array_device> -l <raid_level> -n \<active_devices> -x <spare_devices> <block_devices>
```

Проверка свободного места
```
lfs df

df -t lustre
```
