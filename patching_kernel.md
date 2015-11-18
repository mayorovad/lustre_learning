###Сборка ядра последней доступной версии с поддержкой LustreFS v2.7

13.11.2015 последним доступным ядром CentOS 6.7 было ядро версии **2.6.32-573.8.1.el6** (от	10-Nov-2015 20:35)

####Подготовка к установке

Установку из-под рута **не выполнять**

Добавляем репозиторий EPEL 6.8 (Extra Packages for Enterprise Linux). RPM можно загрузить [отсюда](http://mirror.logol.ru/epel//6/x86_64/epel-release-6-8.noarch.rpm) 
```
# rpm -ivh epel-release-6-8.noarch.rpm
# yum update
```
Далее были установлены необходимые для сборки ядра пакеты:
```
# yum -y groupinstall "Development Tools"
# yum -y install rpm-build redhat-rpm-config unifdef gnupg quilt git
````
Прямо в своей домашней директории выполняем
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
В домашней папке создаем папку `kernel` с необходимой структурой:
```
# mkdir -p kernel/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
```
Переходим в `kernel` и создаем файл `.rpmmacros`
```
# cd kernel
# echo '%_topdir %(echo $HOME)/kernel/rpmbuild' > ~/.rpmmacros
```
Проводим загрузку исходников ядра [отсюда](http://vault.centos.org/6.7/updates/Source/SPackages/kernel-2.6.32-573.8.1.el6.src.rpm).
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
Заходим в `~/kernel/rpmbuild` и разворачиваем исходники ядра
```
# cd ~/kernel/rpmbuild
# rpmbuild -bp --target=`uname -m` ./SPECS/kernel.spec
```
После разворачивания переходим в папку `kernel/rpmbuild/BUILD/kernel-2.6.32-573.8.1.el6/linux-2.6.32-573.8.1.el6.x86_64` и редактируем 4-ую строчку файла Makefile так, чтобы она выглядела следующим образом:
```
EXTRAVERSION = .573.8.1.el6_orion_lustre
```
Не выходя из папки, заменяем `.config` на файл подходящей конфигурации из `lustre-release`:
```
# cp ~/lustre-release/lustre/kernel_patches/kernel_configs/kernel-2.6.32-2.6-rhel6-x86_64.config ./.config
```
Связваем серии и патчи с их расположением в `lustre-release`:
```
# ln -s ~/lustre-release/lustre/kernel_patches/series/2.6-rhel6.series series
# ln -s ~/lustre-release/lustre/kernel_patches/patches patches
```
Применяем патчи с помощью `quilt`:
```
# quilt push -av
```
И запускаем сборку кернела:
```
# make oldconfig || make menuconfig
# make include/asm
# make include/linux/version.h
# make SUBDIRS=scripts
# make include/linux/utsrelease.h
# make
# make rpm
```
> Возможно, можно пропустить этап с командой `make` и сразу выполнить `make rpm`, но я этого не проверял
> Для компиляции ядра нужно около 10 Гб свободного места на жестком диске

Если все пройдет удачно, rpm ядра будет лежать в `~/kernel/rpmbuild/RPMS/x86_64/`
####Установка ядра
Из под **root** запускаем установку rpm-a:
```
# rpm -ivh ~/kernel/rpmbuild/RPMS/x86_64/kernel-2.6.32.573.8.1.el6_orion_lustre-2.x86_64.rpm
```
После установки нужно добавить наше ядро в меню загрузки и сформировать initrd:
```
# /sbin/new-kernel-pkg --package kernel --mkinitrd --dracut --depmod --install 2.6.32.573.8.1.el6_orion_lustre
```
Делаем `reboot`, выполняем `uname -r`, видим, что ядро у нас теперь `2.6.32.573.8.1.el6_orion_lustre`.

О том, как устанавливать и собирать пакеты `lustre` для сервера и клиента, можно прочитать в этом [отчете](./building_lustre.md) 
