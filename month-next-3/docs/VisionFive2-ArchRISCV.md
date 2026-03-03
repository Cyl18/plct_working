# 折腾 VisionFive 2：在 Arch Linux RISC-V 上跑起 Weston + 硬件加速 GPU

> 文章部分由 Claude 整理编写

最近拿到了一块 VisionFive 2（以下简称 VF2），想着在上面装个 Arch Linux 玩玩，顺手把桌面环境也搞起来。结果折腾了挺久，踩了不少坑，记录一下。

## 刷镜像

首先从 [rvspace 论坛](https://forum.rvspace.org/t/arch-linux-image-for-visionfive-2/1459) 找到了社区维护的 Arch Linux RISC-V 镜像。镜像是 zst 压缩的，直接解压然后 dd 进 SD 卡：

```bash
zstd -d ArchLinux-VF2_6.12_v6.0.0-cwt25.img.zst --stdout | sudo dd \
  of=/dev/sdb bs=4M status=progress oflag=sync
```

顺便一提，板子刚到手的时候有一股明显的洗板水味道……工厂气息扑面而来。后面 `pacman -Syyu` 的过程中突然整个系统 I/O 报错（垃圾 sd 卡），重来了一次才成功。

## 初始配置

板子插电开机，先通过串口或 HDMI 进系统。第一步把 SSH 配好，方便后续远程操作：

```bash
vi /etc/ssh/sshd_config   # 确认 PasswordAuthentication、PubkeyAuthentication、PermitRootLogin 都开着
systemctl restart sshd

# 把公钥复制进去
nano .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
chmod -R 600 .ssh
```

然后配代理，更新系统：

```bash
export https_proxy=http://<your-proxy>:port
pacman -Syyu
```

语言环境也顺手配一下（后面装 XFCE4 的时候发现没配 locale 会影响显示）：

```bash
nano /etc/locale.gen   # 取消注释需要的 locale，比如 zh_CN.UTF-8 和 en_US.UTF-8
locale-gen
```

## 解决 2K 60Hz 闪屏

接了显示器之后发现 2K 60Hz 下屏幕一直在闪，难受得很。查了一下，改启动参数把分辨率降到 720p 就好了：

```bash
nano /boot/extlinux/extlinux.conf
```

在启动参数里加上对应的分辨率限制，改完重启生效。

## 扩容磁盘

镜像刷进去之后根分区默认只占了一小部分空间，需要手动扩一下。先用 cfdisk 把分区扩到最大，再让 btrfs 把文件系统也撑满：

```bash
cfdisk /dev/mmcblk1      # 找到根分区，Resize 到最大，Write 保存
sudo btrfs filesystem resize max /
```

用 `df -h` 确认空间到位了再继续。

## 尝试 KDE Plasma：依赖报错

空间够了，接下来装桌面。先冲了 KDE Plasma：

```bash
pacman -Sy plasma-meta
```

结果依赖解析直接报错：

```
warning: cannot resolve "libicuuc.so=76-64", a dependency of "freerdp"
warning: cannot resolve "freerdp", a dependency of "krdp"
warning: cannot resolve "krdp", a dependency of "plasma-meta"
:: The following package cannot be upgraded due to unresolvable dependencies:
      plasma-meta

:: Do you want to skip the above package for this upgrade? [y/N]
```

`plasma-meta` 因为 `krdp → freerdp → libicuuc` 这条链子断了装不上。换成直接装 `plasma` 包组倒是能装，但启动 sddm 之后 Plasma 直接崩了，没细看 log，直接放弃。

## 尝试 XFCE4：驱动不支持 X11

换了个轻量方向，试试 XFCE4：

```bash
pacman -S xfce4 xorg-server
startxfce4
```

启动之后发现渲染有问题，`glxinfo` 报错，OpenGL 跑不起来。开始排查：

```bash
lsmod | grep pvr
dmesg | grep -i pvr
ls /dev/dri
ls /usr/lib/dri | grep pvr
LIBGL_DEBUG=verbose glxinfo -B
cat /var/log/Xorg.0.log | grep -E "DRI|glamor|modeset"
```

查了一圈，情况比较复杂。VF2 的 GPU 是 **PowerVR 系列**，内核侧用的是 Linux 6.8 合并进主线的新上游 DRM pvr 驱动（能在 dmesg 里看到 `Initialized pvr 1.19.6345021`）。

用户态这边有一个社区包 `mesa-pvr-ddk119`，里面包含了 `libEGL_pvr.so` 和对应的 GLVND ICD 文件，PowerVR 的 EGL 驱动是可用的。

但问题是：`mesa-pvr-ddk119` **完全不支持 GLX/X11**，只支持 Wayland EGL。XFCE4 走的是 X11，所以不管怎么折腾都没用。

**结论：PowerVR 驱动只支持 Wayland EGL，X11 没有支持。**

XFCE4 放弃，换思路。

## 改用 Weston（Wayland）：成功

既然只能走 Wayland，那就装 Weston：

```bash
pacman -Rs xfce4
pacman -S weston
```

装完直接跑 `weston`，结果报缺少 `libdisplay-info.so.2`，但系统里装的是 `.so.3`。这是 weston 二进制链接的版本比仓库包版本低，打个软链接临时解决：

```bash
ln -s /usr/lib/libdisplay-info.so.3 /usr/lib/libdisplay-info.so.2
weston
```

这次成功启动了！

但在 Weston 里打开终端跑 `eglinfo`，默认看到的还是 llvmpipe。这是因为 GLVND 优先选了 Mesa EGL，Mesa 初始化失败后 fallback 了。在 `/etc/environment` 里加一行强制指定 pvr 的 ICD，重启后就好了：

```bash
echo '__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/40_pvr.json' >> /etc/environment
```

重启后 Weston 内的终端跑 `eglinfo` 就能看到 `OpenGL ES profile renderer: PowerVR B-Series BXE-4-32`，硬件加速正常。

## 尝试跑 Minecraft

折腾完桌面，顺手试了一下能不能跑 Minecraft。启动器用的是 HMCL，参考了 [rvspace 论坛上的相关帖子](https://forum.rvspace.org/t/how-to-play-minecraft-on-the-visionfive-2/3306)。

注意 HMCL 需要图形环境，**必须在 `weston --xwayland` 启动后，从 Weston 内的终端运行**，直接从 SSH 跑会因为没有 display 直接崩。

RISC-V 上跑 Minecraft 最麻烦的是 LWJGL——官方没有 riscv64 的预编译包，需要自己从 [Glavo 的 fork](https://github.com/Glavo/lwjgl3) 源码编译。先装好依赖：

```bash
pacman -S base-devel gtk3 libxtst
pacman -S ttf-dejavu ttf-liberation noto-fonts xorg-fonts-misc
```

然后拉代码编译：

```bash
git clone --depth=1 https://github.com/Glavo/lwjgl3.git
cd lwjgl3
export ANT_OPTS="-Dhttps.proxyHost=<your-proxy> -Dhttps.proxyPort=port"
LWJGL_BUILD_ARCH=riscv64 ant
```

结果编译卡在了这里：

```
Execute failed: java.io.IOException: Cannot run program "riscv64-linux-gnu-strip"
```

`riscv64-linux-gnu-strip` 是交叉编译工具链里的，Arch Linux RISC-V 上本机编译不需要这个，但构建脚本写死了。`pacman -F riscv64-linux-gnu-strip` 也找不到对应的包。

这个问题暂时没解决，Minecraft 就先搁着了。

> 编译的时候看到频率到 750MHz 了，不清楚什么问题
> echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
> 也许 CPU 调度可以解决，但温度也得先满足

## 总结

整体折腾下来，坑主要集中在两块：

**GPU 驱动：**
- 社区包 `mesa-pvr-ddk119` 提供了可用的 PowerVR EGL 驱动，Wayland 下硬件加速（`PowerVR B-Series BXE-4-32`）完全正常
- 但 GLVND 默认会优先选 Mesa EGL，Mesa 初始化失败后 fallback 到 llvmpipe，需要手动固定 ICD：
  ```bash
  echo '__EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/40_pvr.json' >> /etc/environment
  ```
- `mesa-pvr-ddk119` **不支持 X11/GLX**，所以所有 X11 桌面（KDE、XFCE4 等）都跑不起来，只能走 Wayland

**其他小坑：**
- `libdisplay-info` 版本不匹配，需要打软链接才能启动 Weston
- KDE `plasma-meta` 依赖链断了，装不上

如果你也想在 VF2 上玩 Arch Linux：装 Weston，配好 `__EGL_VENDOR_LIBRARY_FILENAMES`，硬件加速是有的，就是只能 Wayland。
