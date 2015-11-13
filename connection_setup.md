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
