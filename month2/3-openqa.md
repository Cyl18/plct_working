# 产出报告

- 新建仓库 [Cyl18/plct-openqa-ruyisdk-ide](https://github.com/Cyl18/plct-openqa-ruyisdk-ide) 尝试编写了 ruyisdk IDE 的测试用例，但是目前在 openEuler riscv64 上无法运行
- 进行了 openQA 的相关配置，编写并学习相关配置文件，新增 testsuite launch-ruyi-ide-testsuite，解耦测试，在以后可以进行多种发行版的测试，具体在 <https://openqa.inuyasha.love/tests/166>，但是目前由于 openEuler 无法运行，计划之后配置 x86 Ubuntu
- 测试报告 <https://gitee.com/yunxiangluo/ruyisdk-test/pulls/61>
- [配置了 openEuler 24.03 LTS](https://github.com/Cyl18/plct-openqa-ruyisdk-ide/blob/main/scripts/launch-openEulur24.sh) 
- 提出 issue [在 Arch Linux 下打包会因为 Poetry 版本没有 2.0 而报错](https://github.com/ruyisdk/ruyi/issues/261)

---

## openEuler 的设置

- 修改 openEuler 分辨率 (`-display sdl` 足够)
- 创建 [qemu snapshot](https://wiki.qemu.org/Documentation/CreateSnapshot)

```
# snapshot 需要使用绝对路径 可以使用下面的命令修改
qemu-img rebase
```

- 让 openEuler 用户 NOPASSWD

```shell
sudo visudo
sudo usermod -aG wheel openeuler
```

- 配置[自动登录](https://wiki.archlinux.org/title/LightDM)。

---

## Ruyi_IDE_openEulur_24.03_riscv64_测试报告

本次测试基于 Ruyi IDE 0.0.3 版本预编译的 riscv64 版本包 [ruyisdk-0.0.3-linux.gtk.riscv64.tar.gz](https://mirror.iscas.ac.cn/ruyisdk/ide/0.0.3/ruyisdk-0.0.3-linux.gtk.riscv64.tar.gz)

在 openEuler 24.03 LTS riscv64 进行了手动测试。

### 测试环境说明

- openEuler 2403 riscv64 镜像使用 openEuler 提供的 QEMU 镜像 [openEuler-24.03-V1-xfce-qemu-testing.qcow2.zst](https://mirror.iscas.ac.cn/openeuler-sig-riscv/openEuler-RISC-V/testing/2403LTS-test/v1/QEMU/)

### 测试日志

```bash
bash-5.2$ /ruyisdk
CompileCommand:exclude org/eclipse/idt/internal/core/dom/rewrite/ASTRewriteAnayzer.getExtendedRange bool exclude = true
Jan 15,2025 10:54:08 AM org.apache.aries.spifly.BaseActivator log
INF0: Registered provider org.slf4j.simple.SimpleServiceProvider of service orgslf4j.spi.SLF4JServiceProvider in bundle slf4j.simple
/home/openeuler/ruyisdk//plugins/org.eclipse.justi.openidk.hotspot.jre.full.linux,riscy64 21.0,5,20241023-1957/jre/bin/java: symbol lookup error: /home/openeuler/ruyisdk/configuration/org,eclipse.osgi/548/0/.cp/libswt-pi3-gtk-4967r8.so: undefined symbol:g_once_init_enter_pointer
```

### 测试结果

无法启动 Ruyi IDE。

### 测试结论

当前版本的 Ruyi IDE 无法支持在官方提供的 openEulur 24.03 riscv xfce 环境下运行。
