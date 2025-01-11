# 产出报告

这周尝试在配置 openqa-worker 服务器以适配 ruyisdk IDE 的 GUI 测试。

产出为 <https://openqa.inuyasha.love/tests/87> TEST PASSED.

## links

- <https://gitee.com/lvxiaoqian/memo/blob/master/deploy-openQA-for-riscv.md>
- <https://gitee.com/lvxiaoqian/memo/blob/master/openQA%2Bunmatched.md>

## alternative

- [fMBT](https://github.com/intel/fMBT/wiki/GUI-testing)

由于只找到 Python 2 的示例，并且测试时发现无法 import，所以放弃了。

- SWTBOT

SWT 是 Eclipse 的 UI 框架，但是只能以单元测试的形式和 IDE 一起运行。

## 配置 Ubuntu 的 x86 openqa-worker LXC 容器

这里使用 PVE 进行 LXC 容器的创建。

### 创建容器

使用 Ubuntu 22.04 镜像，在 PVE 创建好 CT 后（不确定是否需要 privileged），执行下面的命令。

```shell
# 开启 sshd
systemctl enable sshd
systemctl start sshd

# 修改镜像源 https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/
nano /etc/apt/sources.list
apt update

# 安装基础桌面环境（可选）
apt install --no-install-recommends -y ubuntu-desktop gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal tigervnc-standalone-server

```

配置 vnc

```shell
vncserver # 设置密码

nano ~/.vnc/xstartup
```

```shell
#复制以下内容

#!/bin/sh
unset SESSION_MANAGER
exec /etc/X11/xinit/xinitrc
exec /etc/vnc/xstartup
xrdb $HOME/.Xresources
vncconfig -iconic &
dbus-launch --exit-with-session gnome-session &

# 如果需要连接则使用 vncserver -geometry 1920x1080 -localhost no :1
```

```shell
# 安装 zsh
apt install -y zsh git
wget https://install.ohmyz.sh/
chmod +x index.html
sed -i 's/github\.com/gitclone.com\/github.com/g' index.html
./index.html
```

### 基础配置

```shell
apt install openqa-worker -y
```

打开 `/etc/openqa/client.conf`

```ini
[global]
HOST = openqa.inuyasha.love

[1]
WORKER_CLASS = qemu_riscv64
QEMU_NO_KVM=1
QEMUCPU=rv64
QEMUMACHINE=virt,usb=off
```

打开 `/etc/openqa/client.conf`

```ini
[openqa.inuyasha.love]
key= REDACTED
secret= REDACTED
```

启动 worker：`systemctl start openqa-worker@1`

使用 `systemctl status` 来查看 worker 的状态。如果出现问题可以通过官网文档所提供的方法手动执行，在手动执行时需要处于目录 `/var/lib/openqa`

### openqa-webui 与 openqa-worker 之间的联网

> 尝试了 wireguard，在 lxc 下很难工作。这里采用 zerotier 进行配置。

需要在 [zerotier](https://my.zerotier.com/) 官网注册并创建一个 network

```shell
apt install curl -y
curl -s https://install.zerotier.com | sudo bash
zerotier-cli join NETWORK_ID
```

注意在 PVE 下使用 zerotier 需要给 LXC 容器添加配置，我这里的文件为 `/etc/pve/nodes/home/lxc/106.conf`：

```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net dev/net none bind,create=dir
```

修改两端机器的 `/etc/hosts` 以方便访问。例如 `10.55.55.100 openqa.inuyasha.love`

`ping 10.55.55.100`，检查是否能 ping 通。

> 如果在启动 worker 时发现 WebSocket 无法连接，或者出现 Unauthorized 的情况，一般是反代的问题，使用隧道直连机器则不会出现这样的问题。

zerotier 一般会采用 UDP 打洞的方式直连两台机器，如果不能直连则会采用官方的中继服务器，速度会很慢。可以自己创建一个 moon 来进行中继，唯一的问题是 moon 的 IPv4 地址不能变动。

### 配置 SMB 文件共享

> 同样的，NFS 由于 LXC 容器的原因不好使用。

安装好 Samba 服务端与客户端。

在 worker 机打开 `/etc/systemd/system/var-lib-openqa-share.mount`，重启命令为 `systemctl restart var-lib-openqa-share.mount`

```shell
apt install cifs-utils
```

```ini
[Unit]
Description=Mount CIFS Share
After=network-online.target
Wants=network-online.target

[Mount]
What=//10.55.55.100/openqa_share
Where=/var/lib/openqa/share
Type=cifs
Options=username=root,password=REDACTED,nofail

[Install]
WantedBy=multi-user.target
```

在 webui 机 `/etc/samba/smb.conf`（可能会有冗余内容）

```ini
[global]
        workgroup = WORKGROUP
        passdb backend = tdbsam
        printing = cups
        printcap name = cups
        printcap cache time = 750
        cups options = raw
        map to guest = Bad User
        logon path = \\%L\profiles\.msprofile
        logon home = \\%L\%U\.9xprofile
        logon drive = P:
        usershare allow guests = Yes

getwd cache = true
#   invalid users = root
#   hosts allow = 10.55.55.0/24
#   guest account = root
#server min protocol = 4
[homes]
        comment = Home Directories
        valid users = %S, %D%w%S
        browseable = No
        read only = No
        inherit acls = Yes
[profiles]
        comment = Network Profiles Service
        path = %H
        read only = No
        store dos attributes = Yes
        create mask = 0600
        directory mask = 0700
[users]
        comment = All users
        path = /home
        read only = No
        inherit acls = Yes
        veto files = /aquota.user/groups/shares/
[groups]
        comment = All groups
        path = /home/groups
        read only = No
        inherit acls = Yes
[openqa_share]
path = /var/lib/openqa/share
available = yes
valid users = root
read only = no
browsable = yes
public = yes
writable = yes

```

一些命令：

```shell
sudo smbpasswd -a root
sudo systemctl restart smb
sudo smbstatus
```

### WebUI 管理员权限问题

我不知道如何在 OAuth 之后拿到如何管理员权限，所以直接修改数据库。

Copilot 告诉我这样，首先 `sudo -u postgres psql`，然后连接到数据库，之后：

```SQL
SELECT * FROM users; /*列出所有用户*/

UPDATE users
SET is_operator = 1, is_admin = 1
WHERE username = 'YOUR_ID';
```

### 编译 qemu

Ubuntu 软件源自带的 qemu 为 6，而最新为 9（我不知道会不会导致问题，但是在排查问题的时候选择了自己编译）

安装依赖：

```shell
apt install -y git build-essential pkg-config nlibglib2.0-dev libpixman-1-dev nlibaio-dev libcap-dev nzlib1g-dev libfdt-dev nlibgtk-3-dev nlibspice-server-dev nlibusb-1.0-0-dev nlibbrlapi-dev nlibbluetooth-dev nlibcurl4-openssl-dev nlibgtk-3-dev nlibnfs-dev nlibiscsi-dev nlibseccomp-dev nlibsnappy-dev nlibxen-dev libaio-dev
apt install python3-venv python3-tomli ninja-build pkg-config libglib2.0-dev flex bison
```

编译：

```shell
./configure --target-list=riscv64-softmmu --enable-user --enable-slirp
make -j5
cp build/qemu-system-riscv64 /bin # 替换系统的 qemu
```

### 一些中间配置

worker 机上：

```shell
apt install libtime-moment-perl
apt install libcpanel-json-xs-perl
apt install libio-scalar-perl
cpan
```

cpan 使用镜像：<https://mirrors.tuna.tsinghua.edu.cn/help/CPAN/>  
在配置时某些时候会报错，根据所报错误安装对应包。

有的命令可能需要 WebUI 的用户 `geekotest` 来执行（通过 `ls -l /var/lib/openqa` 来查看是什么用户）

有时候会出现找不到文件的问题，使用 `sudo find / -name ""`，来找到并复制到 worker 机 (使用如 `scp` 的工具)

### 最终的配置

触发测试在 webui 机上使用以下命令：

```shell
openqa-cli api -X POST --apikey REDACTED --apisecret REDACTED isos async=0 DISTRI=openeuler FLAVOR=v1 ARCH=riscv64 VERSION=23.09
```

在测试时发现需要修改 openqa 源码，`nano /usr/lib/os-autoinst/backend/qemu.pm`，搜索 `once=d`，注释掉此行。

> 这里参考了上个实习生的 <https://gitee.com/lvxiaoqian/memo/blob/master/deploy-openQA-for-riscv.md> 以及 <https://gitee.com/lvxiaoqian/memo/blob/master/openQA%2Bunmatched.md>

修改 WebUI 中 Machines 中的 `openEuler_2309_riscv64`，通过查询 <https://repo.tarsier-infra.isrc.ac.cn/openEuler-RISC-V/preview/openEuler-23.09-V1-riscv64/QEMU/> 下的 `start_vm_xfce.sh`，修改为以下内容。  
~~哇哦其实我根本不知道为什么可以运行欸 有的参数可能可以删除 自己试试吧~~

```ini
BIOS=fw_payload_oe_uboot_2304.bin
CDMODEL=virtio-blk-device
HDDMODEL=virtio-blk-device
HDD_1=openEuler-23.09-V1-xfce-qemu-preview.qcow2
NOAUTOLOGIN=1
NUMDISKS=1
PARALLEL=none
PASSWORD=openEuler12#$
QEMU=riscv64
QEMUCPU=rv64
QEMUCPUS=4
QEMUMACHINE=virt,accel=kvm,usb=off,dump-guest-core=off,gic-version=3
QEMURAM=4096
QEMU_APPEND=device virtio-vga -device usb-kbd -device usb-tablet
ROOTONLY=1
SERIALDEV=ttyS0
TIMEOUT_SCALE=200
VIRTIO_CONSOLE=0
WORKER_CLASS=qemu_riscv64
```

`fw_payload_oe_uboot_2304.bin` 文件需要存在于 worker 机的 `/usr/share/qemu/` 以及 webui 机的 `/var/lib/openqa/share/factory/other/`

### 更新测试用例

上位实习生的 <https://github.com/delete-cloud/openqa-test/blob/main/needles-design.md> 由于 openEulur 版本不同，无法通过测试。通过在 openqa WebUI 右键保存图片的方式，更新了 `/var/lib/openqa/share/tests/openeuler/products/openeuler/needles/***.png` 的内容后通过测试。

另外有 <https://github.com/delete-cloud/openqa-test/blob/main/needles-design.md>。

- 主文件在 `/var/lib/openqa/share/tests/openeuler/tests/openEuler_login_test.pm`
- needle 在 `/var/lib/openqa/share/tests/openeuler/products/openeuler/needles/openEuler_login_testsuite.yaml`

### 以后可能需要用到的

- <https://github.com/drpaneas/ubuntu_qa/tree/master>
