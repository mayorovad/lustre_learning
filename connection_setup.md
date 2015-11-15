###Настройка соединения между компьютерами

####Настройка соединения через Hamachi

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

####Монтирование LustreFS со стороны клиента
Первым делом нужно загрузить модуль lustre в ядро (*предполагается, что клиент lustre уже установлен на системе клиента, о том как это делать можно прочитать [здесь](./building_lustre.md)
```
# modprobe lustre
```
Для того, чтобы смонтировать раздел \lustre с LustreFS достаточно выполнить:
```
# mount -t lustre <IP сервера>@tcp:/lustre /mnt
```
Для тестирования монтирования можно выполнить:
```
# mount
```
В выводе должна содержаться строка:
```
<IP сервера>@tcp:/lustre on /mnt type lustre (rw)
```
####Создание LustreFS
```
# mkfs.lustre --mdt --mgs --fsname=orionfs /dev/sdb
# mount -t lustre /dev/sdb /mnt/mdt
# mkfs.lustre --reformat --ost --index=1 --mgsnode=localhost@tcp --fsname=orionfs /dev/sdb2
# mount -t lustre /dev/sdb2 /mnt/ost1
```
