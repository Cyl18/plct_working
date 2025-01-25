# 产出报告

- 配置好了 openQA 的 Ubuntu 22.04 环境
- 更新仓库 Cyl18/plct-openqa-ruyisdk-ide, commit [67214f1 Add ubuntu support, ruyi ide launch checks and some support scripts](https://github.com/Cyl18/plct-openqa-ruyisdk-ide/commit/67214f1e27bfcfaddbb520df86cc8726e6e172bf)
- 通过 ruyi ide 启动测试 [tests/238](https://openqa.inuyasha.love/tests/238)

可能可以使用 <https://askubuntu.com/questions/972215/a-start-job-is-running-for-wait-for-network-to-be-configured-ubuntu-server-17-1> 解决网络问题

使用 `openqa-cli api -X POST --apikey $OPENQA_API_KEY --apisecret $OPENQA_API_SECRET isos async=0 DISTRI=plct-openqa-ruyisdk-ide FLAVOR=ubuntu-22.04 ARCH=x86_64 VERSION=1 RUYI_SDK_IDE_VERSION=0.0.3` 来触发测试