###Сборка ядра последней доступной версии с поддержкой LustreFS v2.7

13.11.2015 последним доступным ядром CentOS 6.7 было ядро версии **2.6.32-573.8.1.el6** (от	10-Nov-2015 20:35)

####Подготовка к установке

Был добавлен репозиторий EPEL 6.8 (Extra Packages for Enterprise Linux). RPM можно загрузить [отсюда](http://mirror.logol.ru/epel//6/x86_64/epel-release-6-8.noarch.rpm) 
```
# rpm -ivh epel-release-6-8.noarch.rpm
# yum update
```
Далее были установлены необходимые для сборки ядра пакеты:
```
# yum -y groupinstall "Development Tools"
# yum -y install rpm-build redhat-rpm-config unifdef gnupg quilt git
````
В `/root` была создана папка `build`, в которую был склонирован официальный гит Lustre
```
# git clone git://git.whamcloud.com/fs/lustre-release.git
```
Переходим в папку `lustre-release` и запускаем скрипт `autogen.sh`
```
# cd lustre-release
# sh ./autogen.sh
```
После запуска `autogen.sh` получили следующий вывод, по которому делаем вывод, что все зависимости удовлетворены.
```
configure.ac:12: installing `config/config.guess'
configure.ac:12: installing `config/config.sub'
configure.ac:14: installing `config/install-sh'
configure.ac:14: installing `config/missing'
libcfs/libcfs/autoMakefile.am: installing `config/depcomp'
```
####Подготовка исходников ядра
Внутри папки `/root` создаем папку `kernel` с необходимой структурой:
```
# mkdir -p kernel/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```
Переходим в `kernel` и создаем файл `.rpmmacros`
```
# cd kernel
# echo '%_topdir %(echo $HOME)/kernel/rpmbuild' > ~/.rpmmacros
```
Проводим загрузку исходников ядра [отсюда](http://vault.centos.org/6.7/updates/Source/SPackages/kernel-2.6.32-573.8.1.el6.src.rpm)
Устанавливаем исходники:
```
# rpm -ivh kernel-2.6.32-573.8.1.el6.src.rpm
```
Разворачиваем исходники
```
# rpmbuild -bp --target=`uname -m` ~/kernel/rpmbuild/SPECS/kernel.spec
```
При первой попытке был получен список неудовлетворенных зависимостей, пришлось установить пакеты:
```
# yum install -y xmlto asciidoc elfutils-libelf-devel elfutils-devel binutils-devel newt-devel python-devel audit-libs-devel perl-ExtUtils-Embed hmaccalc
```
После повторного запуска команды ```rpmbuild``` и успешного завершения исходники ядра будут лежать в папке:
```
kernel/rpmbuild/BUILD/kernel-2.6.32-573.8.1.el6/linux-2.6.32-573.8.1.el6.x86_64
```
####Добавление в ядро кода LustreFS

...
