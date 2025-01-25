# 月产出报告

- [docs/#66](https://github.com/ruyisdk/docs/pull/66) 更新文档：使用 gcc 编译 coremark；新增文档：使用 meson/cmake 集成，使用 qemu 和 llvm；一些细节修改
- 配置了 openqa-worker 服务器，网络与 webui 连接
- 新建仓库 [Cyl18/plct-openqa-ruyisdk-ide](https://github.com/Cyl18/plct-openqa-ruyisdk-ide)
- 编写了 ruyisdk IDE 的启动的测试用例
- 配置了 openQA 的 riscv openEuler 24.03 LTS 并能在 openQA 上触发启动系统的测试用例
- 配置了 openQA 的 Ubuntu 22.04 并能在 openQA 上触发启动系统的测试用例
- 通过 ruyi ide 启动测试 [tests/238](https://openqa.inuyasha.love/tests/238)
- 提出 issue [ruyi/261](https://github.com/ruyisdk/ruyi/issues/261) 在 Arch Linux 下打包会因为 Poetry 版本没有 2.0 而报错
- 测试报告 <https://gitee.com/yunxiangluo/ruyisdk-test/pulls/61>

测试可以通过以下命令触发： `openqa-cli api -X POST --apikey $OPENQA_API_KEY --apisecret $OPENQA_API_SECRET isos async=0 DISTRI=plct-openqa-ruyisdk-ide FLAVOR=ubuntu-22.04 ARCH=x86_64 VERSION=1 RUYI_SDK_IDE_VERSION=0.0.3`