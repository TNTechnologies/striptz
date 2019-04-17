In order to use striptz you first need to set up a dummy interface. Currnetly the interface needs to be named eth1.
Future revistions will parse config file for setting. If the interface needs to be changed edit the interface paramater
of the sniff function.

`ip link add eth1 type dummy`

`ip link set eth1 promisc on`

`ip link set eth1 up`



Next you will need to configure the Mikrotik router to stream sniffed data. The example Configurations are
just basics needed to make the system work. Further configurations should be made for

`/tool sniffer set streaming-enabled=yes`

`/tool sniffer set streaming-server=<IP_OR_HOSTNAME_OF_SNORT_SERVER>`

`/tool sniffer set filter-stream=yes`

`/tool sniffer start`



Start striptz.py

`./path_to/striptz.py start`



Start snort with -i eth1 tag. (example)

`snort -d -h <CIDR_NOTATION_OF_SUBNETS_TO_MONITOR> -l /var/log/snort/ -c /etc/snort/snort.conf -i eth1 -A console`
