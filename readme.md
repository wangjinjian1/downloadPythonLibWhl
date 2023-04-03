# 使用说明
## 参数
```Python
def downloadLib(nes,flag = False,useproxy = False,installed = False,installpiptree = True,packagePath = 'packages',unnes = ('pipdeptree',),proxy_='--trusted-host https://repo.huaweicloud.com -i https://repo.huaweicloud.com/repository/pypi/simple'):
    '''
    自动解析依赖库并且下载，需要自带python环境
    :param nes: 需要下载的库,为set类型，必须参数
    :param flag: 如果目录packagePath存在，是否删除重建,default False
    :param useproxy: 是否使用代理下载 download , default False
    :param installed: 是否已安装，未安装会自动安装对应的python库 ,default False
    :param installpiptree: 是否安装pipdeptree,已安装的话可以需要设置为False ,default True
    :param packagePath: 下载库存放目录,default packages
    :param proxy_: 代理地址，默认华为
    :return:None
    '''
    pass
```
## 用法举例
### 所需安装的库自己环境中还未安装
```python
nes = {'matplotlib'}
downloadLib(nes)
```
### 所需安装的库已安装
```python
nes = {'matplotlib'}
downloadLib(nes,installed=True)
```

