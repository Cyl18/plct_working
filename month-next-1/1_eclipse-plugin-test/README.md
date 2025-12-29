# 测试报告

版本 [4019d74](https://github.com/ruyisdk/ruyisdk-eclipse-plugins/commit/4019d74407718d8c77f8dc56741ea6794e5a847e)  

## 总结

新闻测试通过，其它子系统有部分问题。  
共有 1 个 blocking 问题，3 个 major 问题，5 个 minor 问题，1 个 consistency 问题。  

## 详细说明

### 1. 安装时提示没有证书

> 严重度: minor

<img src="pics/1-install-cert.jpg" height="100" alt="1-install-cert" />

### 2. 安装 ruyi 时继续没有被 disable

> 严重度: major

<img src="pics/2-install-no-confirm.jpg" height="100" alt="2-install-no-confirm" />
<img src="pics/2-install-no-confirm-2.jpg" height="100" alt="2-install-no-confirm-2" />

### 3. 新闻

> pass

<img src="pics/3-news-pass.jpg" height="100" alt="3-news-pass" />

### 4. 选择开发板时没有 sort

> 严重度：consistency

<img src="pics/4-select-board-no-sort.jpg" height="100" alt="4-select-board-no-sort" />

### 5. 下载 package 的 UI 中 OK 没有被 disable

> 严重度: major

<img src="pics/5-download-package-ui.jpg" height="100" alt="5-download-package-ui" />

### 6. 下载 package 的 UI 刷 log

> 严重度：minor

<img src="pics/6-download-package-no-confirm.jpg" height="100" alt="6-download-package-no-confirm" />
<img src="pics/6-download-package-no-confirm-1.jpg" height="100" alt="6-download-package-no-confirm-1" />

### 7. package 的卸载按钮不好被找到

> 严重度：minor

可以像 Android SDK 那样，反选再 save 则移除，或者加一个 uninstall

<img src="pics/7-uninstall-not-easy-to-find.jpg" height="100" alt="7-uninstall-not-easy-to-find" />

### 8. ruyi venv 有两个 manual

> ~~严重度：minor~~ ruyi 问题

<img src="pics/8-ruyi-venv-2manual.jpg" height="100" alt="8-ruyi-venv-2manual" />
<img src="pics/8-ruyi-venv-2manual-2.jpg" height="100" alt="8-ruyi-venv-2manual-2" />

### 9. venv 不检测当前目录，只能写在项目根目录才会被检测到

> 严重度：major

<img src="pics/9-ruyi-venv.jpg" height="100" alt="9-ruyi-venv" />
<img src="pics/9-ruyi-venv-2.jpg" height="100" alt="9-ruyi-venv-2" />

### 10. venv 项目在删除时不刷新

> 严重度：minor

<img src="pics/10-not-refresh-venv-when-delete-proj.jpg" height="100" alt="10-not-refresh-venv-when-delete-proj" />

### 11. venv CDT 配置不易用

> 严重度：blocking

// need verify

新建一个 C/C++ 项目，可以成功覆盖：

<img src="pics/11-can-apply-to-normal-c-proj.jpg" height="100" alt="11-can-apply-to-normal-c-proj" />

但是新建 RuyiSDK 项目不行：

<img src="pics/11-no-cdt.jpg" height="100" alt="11-no-cdt" />

### 12. 开发板设置没有被 package 引用，显得 pointless

> 严重度：minor

<img src="pics/12-settings-pointless.jpg" height="100" alt="12-settings-pointless" />
