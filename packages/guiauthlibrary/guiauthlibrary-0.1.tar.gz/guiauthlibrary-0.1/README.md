
# eNlight WAF

Welcome on the [eNlight WAF](https://esds.co.in/waf) documentation !

[![pipeline status](http://gitlab360.enlightcloud.com/enlightwaf/enlight-waf-gui/badges/master/pipeline.svg)](http://gitlab360.enlightcloud.com/enlightwaf/enlight-waf-gui/commits/master) [![coverage report](http://gitlab360.enlightcloud.com/enlightwaf/enlight-waf-gui/badges/master/coverage.svg)](http://gitlab360.enlightcloud.com/enlightwaf/enlight-waf-gui/commits/master)

## Overview

eNlight WAF is a web application firewall that protects your web application from common web threats by making your application secure and always available. eNlight WAF ensures the security of web applications facing the internet. <br/>
eNlight WAF is ready for HTTP/2 and IPv6.

Basic eNlight WAF's features are:
 - Network firewall based on FreeBSD `pf`
 - Network TCP balancing based on `ha-proxy`
 - HTTP Proxy balancer based on `Apache`
 - User Authentication against LDAP/AD, Kerberos, SQL, Radius, ...
 - Web application firewall based on `ModSecurity` and `custom algorithms`
 - TLS endpoint, Content rewriting, and many other cool things...

eNlight WAF is build on top of FreeBSD, Apache, Redis HAproxy and MongoDB. <br/>
It is horizontaly scalable by-design (eNlight WAF Cluster) and is manageable though a unique Web GUI.

## Dependencies required to run eNlight WAF

* OS: [FreeBSD 12.1](https://download.freebsd.org/ftp/releases/amd64/amd64/ISO-IMAGES/12.1/FreeBSD-12.1-RELEASE-amd64-dvd1.iso)
* Programming Language: Python 3.7

## eNlight WAF Packages

1. eNlight_WAF_installer_v2.sh
2. eNlight-WAF.tar.gz
3. eNlight-WAF-Engine-2.4.41-68.tar.gz
4. eNlight-WAF-GUI-1.75.tar.gz
5. eNlight-WAF-Bootstrap-2.0.0.tar.gz
6. install.sh

# Installation Steps

Make sure you have the dependencies and eNlight WAF Packages mentioned above installed before proceeding further.

* **Step 0** - Clone the eNlight WAF repository (from the master branch) and ```cd ``` into the directory.
```sh
git clone -b master http://gitlab360.enlightcloud.com/akashtalole/waf_gui_1_75.git
cd waf_gui_1_75/packages
```

* **Step 1** - Copy sh and gz files into root directory. Run install.sh.

```sh
cp *.gz /root/
cp *.sh /root/
/bin/sh install.sh
```

* **Step 2** - Remove unnecesary packages and copy eNlight WAF logo into /etc/motd

```sh
/bin/rm -f  /root/eNlight_WAF_installer_v2.sh /root/eNlight-WAF-Bootstrap-2.0.0.tar.gz
vi /etc/motd
                                                            _   _ _ _       _     _    __        ___    _____
                                                        ___| \ | | (_) __ _| |__ | |_  \ \      / / \  |  ___|
                                                       / _ \  \| | | |/ _` | '_ \| __|  \ \ /\ / / _ \ | |_
                                                      |  __/ |\  | | | (_| | | | | |_    \ V  V / ___ \|  _|
                                                       \___|_| \_|_|_|\__, |_| |_|\__|    \_/\_/_/   \_\_|
                                                                      |___/

```

* **Step 3** - Clear history.

```sh
history -c
```

* **Step 4** - Create template(ESXI and Xen) by removing NICs.

* **Step 5** - Edit waf_conf_master.json on WAF Master node and waf_conf_slave.json on WAF Slave Node.

```sh
vi /var/bootstrap/waf_conf_master.json
vi /var/bootstrap/waf_conf_slave.json
```

* **Step 6** - To install WAF master node run following command

```sh
/var/bootstrap/bootstrap.py --config /var/bootstrap/waf_conf_master.json
```

* **Step 7** - To install WAF slave node run following command

```sh
/var/bootstrap/bootstrap.py --config /var/bootstrap/waf_conf_slave.json
```

* **Step 8** - Clear history.

```sh
history -c
```
