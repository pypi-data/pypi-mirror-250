======================
LXD dynamic DNS client
======================

Program to monitor the LXD API endpoint for container and VM changes and performs DDNS updates to keep DNS records up to date.

Installation
------------

.. code:: bash

    pip install lxd-dyndns


Usage
-----

.. code:: bash

    $ lxd-dyndns -f /etc/lxd-dyndns.conf -d info


.. code:: toml

    cache_dir = "/var/lib/lxd-dyndns"

    [projects.k8s]
    dns_server = "192.168.2.1"
    dns_port = 8053
    dns_transport = "TCP"
    dns_key_name = "knot_lxd"
    dns_key_secret = "Zj7NdR9/6DJonRuTt/++QgMyvSlD4Ndv+i5SvGtGY3Q="
    dns_zone = "lxd.domain.tld."

    lxd_server = "https://lxd-leader.domain.tld:8443"
    lxd_verify = false
    lxd_client_cert = "/etc/ssl/lxd-dyndns/client.crt"
    lxd_client_key = "/etc/ssl/lxd-dyndns/client.key"

    ipv6_prefixes = [ "dead:beef::0/96" ]

