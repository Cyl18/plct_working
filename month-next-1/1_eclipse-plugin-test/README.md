# 测试报告

## 总结

新闻测试通过，其它子系统有部分问题。  
共有 4 个 major 问题，6 个 minor 问题，1 个 consistency 问题。  

## 详细说明

### 1. 安装时提示没有证书

> 严重度: minor

### 2. 安装 ruyi 时继续没有被 disable

> 严重度: major

### 3. 新闻

> pass

### 4. 选择开发板时没有 sort

> 严重度：consistency

### 5. 下载 package 的 UI 中 OK 没有被 disable

> 严重度: major

### 6. 下载 package 的 UI 刷 log

> 严重度：minor

### 7. package 的卸载按钮不好被找到

> 严重度：minor

可以像 Android SDK 那样，反选再 save 则移除

### 8. ruyi venv 有两个 manual

> 严重度：minor

### 9. venv 不检测当前目录，只能写在项目根目录

> 严重度：major

### 10. venv 项目在删除时不刷新

> 严重度：minor

### 11. venv CDT 配置不易用

> 严重度：major

新建一个 C/C++ 项目，可以成功覆盖：

但是新建 RuyiSDK 项目不行：

### 12. 开发板设置没有被 package 引用，显得 pointless

> 严重度：minor