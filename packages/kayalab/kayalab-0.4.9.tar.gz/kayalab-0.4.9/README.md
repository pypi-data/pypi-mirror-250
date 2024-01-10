# Kayalab python module

CLI utility to create virtual machines and install HPE Ezmeral products.

## Usage

It supports install/delete operations for Virtual Machines on Proxmox VE and Vmware vSphere.

### Prepare

Download base cloud images for template creation.

Tested images can be found at:
Rocky8:
`https://download.rockylinux.org/pub/rocky/8/images/x86_64/Rocky-8-GenericCloud.latest.x86_64.qcow2`

RHEL8 (login required):
`https://access.cdn.redhat.com/content/origin/files/sha256/5f/5f9cd94d9a9a44ac448b434f3e28d24465deef089bbd452392b3f10e96cb8eaa/rhel-8.8-x86_64-kvm.qcow2`

#### Vmware

Convert qcow2 image to vmdk

`qemu-img convert -f qcow2 -O vmdk -o subformat=streamOptimized Rocky-8-GenericCloud.latest.x86_64.qcow2 Rocky-8-GenericCloud.latest.x86_64.vmdk`

(Enable and) SSH into the esx host (change your host name)
`ssh root@<esx.host>`

Copy vmdk to a datastore (change your host name and datastore path)
`scp Rocky-8-GenericCloud.latest.x86_64.vmdk root@<esx.host>:/vmfs/volumes/<datastore>`

Convert image to disk
`vmkfstools -i Rocky-8-GenericCloud.latest.x86_64.vmdk rocky-template.vmdk -W file -d thin -N`

#### Proxmox

Copy qcow2 base image file(s) into /var/lib/vz/template/qemu folder (create the qemu folder first)

### Configure Utility

`kayalab config set`

To enable proxy (no_proxy will be generated and added to environment automatically):

```ini
proxy = http://proxy.company.com:80
```

To use local yum/dnf repository:

Using Nexus OSS, you can add a yum-proxy repository with this:
Remote Storage: `https://download.rockylinux.org/pub/rocky/`

```ini
yum_proxy = http://10.1.1.10:8081/repository/yum-proxy
```

To use local mapr repository:

Using Nexus OSS, you can add a yum-proxy repository with this:
Remote Storage: `https://package.ezmeral.hpe.com/releases/`
Authentication: Checked
Authentication Type: Username
Username: `<HPE passport email>`
Password: `<Repository Token>`

```ini
mapr_proxy = http://10.1.1.10:8081/repository/mapr-proxy
```

### Copy UA airgap files (optional)

More details on how to use AirGap utility is available in the [documentation](https://docs.ezmeral.hpe.com/unified-analytics/12/Installation/airgap-utility.html)

`ezua-airgap-util --release v1.2.0 --copy --dest_url http://<local-registry>:5000/ --dest_creds user:pass`

### Create template VM

`kayalab create template -t pve|vmw --host <host>`

### Create VMs

`kayalab create vm -t pve|vmw --host <host>`

### Ezmeral Data Fabric

#### Install Ezmeral Data Fabric

Version 7.5 with EEP 9.2.0 will be installed on as many hosts provided. Installer will be installed on the first node and system will automatically distribute services across other nodes. Single node installation is also possible. Core components (fileserver, DB, Kafka/Streams, s3server, Drill, HBase, Hive) and monitoring tools (Grafana, OpenTSDB...) will be installed.

`kayalab install ezdf -h 10.1.1.21 -h 10.1.1.22 -h 10.1.1.23 -h 10.1.1.24 -h 10.1.1.25`

#### Configure Ezmeral Data Fabric Client

Will download secure files from the server and install/configure the client for the cluster.

`kayalab install dfclient --server 10.1.1.21 --client 10.1.1.30`

### Ezmeral Unified Analytics

You need to get UA installer docker image and then extract ezfabricctl and ezfab-release.tgz files from it.

```bash
docker cp hpe-ezua-installer-ui:/root/ezua-installer-ui/ezfab-release.tgz .
docker cp hpe-ezua-installer-ui:/root/ezua-installer-ui/ezfabricctl_darwin_amd64 .
docker cp hpe-ezua-installer-ui:/root/ezua-installer-ui/ezfabricctl_linux_amd64 .
```

TODO: can provide direct links if/when they are publicly available.

Install container in first node:

Assuming vm1 and vm2 created for control-plane (4 cores & 32GB memory), and vm3, vm4, vm5 as worker nodes (32 cores & 128GB memory). Requirements might change with future releases (available at `https://docs.ezmeral.hpe.com/`)

`kayalab install ezua orch -h <vm1-ip-or-fqdn>`

Add other hosts to the pool:

`kayalab install ezua pool -w <vm2-ip-or-fqdn> -w <vm3-ip-or-fqdn> -w <vm4-ip-or-fqdn> -w <vm5-ip-or-fqdn>`

Create workload cluster:

`kayalab install ezua workload -o <vm1-ip-or-fqdn> -c ezfab-orchestrator-kubeconfig`

## NOTES

If API servers (ProxmoxVE and/or vSphere) are using self-signed certificates, insecure connection warnings will mess up your screen. You can avoid this using environment variable (this is not recommended due to security concerns):

`export PYTHONWARNINGS="ignore:Unverified HTTPS request"`

## TODO

[ ] Proper documentation and code clean up

[ ] Test on standalone ESX host

[ ] Test airgap for UA
