##Настройка соединения между компьютерами

###Настройка соединения через Hamachi

>При использовании **hamachi** не получилось примонтировать фс со стороны клиента. Возможно, это связано с тем, что lnet не распознает виртуальную локальную сеть hamachi автоматически и требуется дополнительная конфигурация в /etc/modprobe.d/lnet.conf

Устанавливаем пакет для обеспечения зависимости
```
# yum install redhat-lsb
```

После установки последней версии Hamachi, которую можно скачать [здесь](https://secure.logmein.com/labs/logmein-hamachi-2.1.0.139-1.x86_64.rpm), выполняем следующие команды:
```
# /etc/init.d/logmein-hamachi start
# hamachi login
# hamachi join <XXX>
```
где `<XXX>` - номер сети Hamachi, созданной на [сайте](https://secure.logmein.com/central/Central.aspx)

####Открытие портов, настройка SSH и RSH
Устанавливаем пакеты ssh, sshd и xinetd
```
# yum install openssh-server openssh-clients rsh xinetd
```
Запускаем сервер ssh
```
# chkconfig sshd on
# service sshd start
```
Открываем порт 22 для `ssh` и порт 513 для `rlogin+rsh` и 988 для LustreFS
```
# iptables -I INPUT -p tcp --dport 22 -m state --state NEW -j ACCEPT
# iptables -I INPUT -p tcp --dport 513 -m state --state NEW -j ACCEPT
# iptables -I INPUT -p tcp --dport 988 -m state --state NEW -j ACCEPT
```
Сохраняем конфигурацию, перезапускаем `iptables` и на всякий случай `xinetd`
```
# service iptables save
# /etc/init.d/iptables restart
# service xinetd restart
```
Редактируем содержимое `/etc/xinetd.d/rsh`, чтобы там было следующее:
```
service shell {
                disable        = no
                socket_type    = stream 
                wait           = no 
                user           = root
                log_on_success += USERID
                log_on_failure += USERID
                server         = /usr/sbin/in.rshd 
                server_args    = -h
              }
```
В файле `/etc/securetty` проверяем на наличие строки `rsh` и `rlogin`, при отсутствии добавляем.

Затем запускаем сервер RSH (заодно запустим rlogin)
```
# chkconfig rsh on
# chkconfig rlogin on
```
Если все сделано правильно, можно выполнить:
```
# rlogin localhost
```
И получить запрос на ввод пароля:
```
Password:
```
Если получили ошибку, пробуем еще раз запустить rsh и rlogin, проверяем работает ли Hamachi и не забыли ли изменить какой-нибудь конфиг

###Формирование простой системы LustreFS
>Будем использовать две машины. На первой будут расположены MDS/MDT и OSS/OST. На второй - клиент. Использование второй машины обусловлено тем, что в документации к LustreFS упоминается о нежелательности расположения OSS/OST и клиента на одной машине, так как это может привести к взаимным блокировкам фс и полному отказу.

#####Настройка LNET
>Пока что настройка LNET идентична для обеих машин
В файле `/etc/hosts` прописываем для `localhost` свой ip от сетевого интерфейса, так как lustre отказывается работать с loopback интерфейсами
```
<IP адрес eth или wlan>           localhost.localdomain localhost
```

LNET (Lustre networking) обеспечивает сетевое взаимодействие LustreFS. Для простых случаев (один интерфейс, одно соединение) настройка опциональна, так как в таких случаях LNET автоматически конфигурирется на единственный интерфейс. Но для наглядности все-таки добавим свой конфиг в файл `/etc/modprobe.d/lnet.conf`(первоначально файла не существует).
Содержимое `lnet.conf` должно выглядеть так:
```
options lnet networks=tcp0(eth0) 
options lnet accept=all
```
Первая строка конфига указывает на то, что бы будем использовать tcp0 через ethernet, вторая - на то, что может использоваться любой порт(по умолчанию используется только 988)
После создания конфига, загружаем модуль lnet и запускаем сеть:
```
# modprobe lnet
# lctl network up
```
В выводе должны получить `LNET configured`
#####Настройка MDS и OSS
На первой машине требуется 2 дополнительных блочных дисковых устройства, для MDT и для OST соответственно.
>MDT и OST не могут находится на разных разделах одного дискового устройства.

Загружаем lustre в ядро и проверяем, что сеть включена
```
# modprobe lustre
```
Форматируем устройства `sdb` и `sdc` и монтируем их.
```
# mkfs.lustre --mdt --mgs --index=0 --fsname=orionfs /dev/sdb
# mount -t lustre /dev/sdb /mnt/mdt
# mkfs.lustre --ost --index=1 --mgsnode=localhost@tcp --fsname=orionfs /dev/sdc
# mount -t lustre /dev/sdc /mnt/ost1
```


#####Настройка клиента, монтирование
Загружаем модуль lustre в ядро
>предполагается, что клиент lustre уже установлен на системе клиента, о том как это делать можно прочитать [здесь](./building_lustre.md)

```
# modprobe lustre
```
Для того, чтобы смонтировать раздел \lustre с LustreFS достаточно выполнить:
```
# mount -t lustre <IP mds_node>@tcp0:/lustre /mnt
```
Для тестирования монтирования можно выполнить:
```
# mount
```
В выводе должна содержаться строка:
```
<IP сервера>@tcp0:/lustre on /mnt type lustre (rw)
```

