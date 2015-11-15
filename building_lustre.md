**Действия, которые выполняются в данном отчете следует выполнять только после сборки модифицированного ядра. 
Отчет о том, как это делать, находится [здесь](./patching_kernel.md). Собирать не из-под рута, устанавливать из-под рута**
####Сборка люстры для сервера
Конфигурируем сборщик люстры 
```
# cd ~/lustre-release/
# ./configure --with-linux=/home/build/kernel/rpmbuild/BUILD/kernel-2.6.32.573.8.1.el6_orion_lustre/
```
Запускаем сборку:
```
# make rpms
```
В итоге, если все пройдет успешно, в папке `lustre-release` появятся следующие rpm-ы:
```
lustre-2.7.62-1_g70e90c3.src.rpm
lustre-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-2.7.62.tar.gz
lustre-debuginfo-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-iokit-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-modules-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-osd-ldiskfs-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-osd-ldiskfs-mount-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-source-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-tests-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
```
Полученные rpm-ы будут работать только под нашим модифицированным ядром. 
####Установка lustre для сервера
При установке понадобится 
[e2fsprogs](http://downloads.hpdd.intel.com/public/e2fsprogs/latest/). Устанавливать начинаем с самого начала:
```
# rpm -ivh lustre-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
```
и последовательно восстанавливаем необходимые зависимости. 
В процессе установки можем получать сообщения о конфликте файлов двух версий
(особенно часто это происходит при установке e2fsprogs). 
Чтобы провести установку нужно использовать ключ `--replacefiles`:
```
# rpm -ivh --replacefiles <имя пакета с конфликтом>.rpm
```
####Сборка люстры для клиента
Нам потребуется `src.rpm` файл используемой версии lustre. Он будет лежать в папке `lustre-release`
после успешной сборки. Заходим в папку и запускаем сборку rpm-ов с ключами `--rebuild --without servers`: 
```
# cd ~/lustre-release
# rpmbuild --rebuild --without servers <lustre version>.src.rpm
```
Сборку нужно производить из-под ядра, модифицированного кодом люстры, которое мы собрали ранее. 
После успешной сборки rpm-ы для клиента будут лежать в папке `~/kernel/rpmbuild/RPMS/x86_64/':
```
lustre-client-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-client-debuginfo-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-client-modules-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-client-source-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-client-tests-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
lustre-iokit-2.7.62-2.6.32.573.8.1.el6_orion_lustre_g70e90c3.x86_64.rpm
```
####Установка lustre для клиента
Установка полностью аналогична установке пакетов сервера, однако пакеты клиента не требуют модифицированного ядра.
