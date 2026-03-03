
```shell
# 安装 MATE 桌面
dnf install mate-desktop
dnf install mate-session-manager mate-panel caja marco

# 安装 Xorg
dnf install xorg-x11-server-Xorg xorg-x11-xinit xorg-x11-drivers

# 安装显卡驱动
dnf install mesa-dri-drivers mesa-libEGL mesa-libGL libdrm xorg-x11-drv-modesetting xorg-x11-drv-evdev

# xinit (可能需要)

echo "exec mate-session" > ~/.xinitrc
chmod +x ~/.xinitrc

# 安装并启用 LightDM
dnf install lightdm lightdm-gtk
systemctl enable lightdm
systemctl set-default graphical.target
reboot
```
