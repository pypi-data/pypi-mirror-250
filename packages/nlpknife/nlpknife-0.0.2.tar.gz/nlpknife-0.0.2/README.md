## 项目说明

我的瑞士军刀

## 安装与部署
### 在线安装

```shell
python setup.py install
```

### 离线安装

在项目根目录进行打包
```shell
sh ./shell/package.sh
```
注意，这里的离线构建环境应当与部署总体环境一致，包括python版本，系统等

随后将得到的 nlpknife.tar.gz 迁移到部署环境，解压并安装对应依赖项就可以。
解压：
```shell
tar -zxvf nlpknife.tar.gz
```
安装
```shell
sh ./package/install.sh
```
