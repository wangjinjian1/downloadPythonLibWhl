import json, os, shutil


def downloadLib(nes, flag=False, useproxy=False, installed=False, installpiptree=True, packagePath='packages',
                proxy_='--trusted-host pypi.tuna.tsinghua.edu.cn -i https://pypi.tuna.tsinghua.edu.cn/simple'):
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
    installtemplate = 'pip install {} \n'
    uninstalltemplate = 'pip uninstall {} -y \n'

    ########## 检查是否使用代理下载
    print('检查是否使用代理下载'.center(50, '='))
    if useproxy:
        print('使用代理下载')
        proxy = proxy_
    else:
        print('不使用代理下载')
        proxy = ''

    ########## 检查是否安装pipdeptree
    print('检查是否安装pipdeptree'.center(50, '='))
    if installpiptree:
        print('安装pipdeptree')
        os.system('pip install pipdeptree {}'.format(proxy))
    else:
        print('不安装pipdeptree')

    ########## 检查是否已安装库
    print('检查是否已安装库'.center(50, '='))
    if not installed:
        print('已安装')
        for i in nes:
            os.system('pip install {} {} \n'.format(i, proxy))
    else:
        print('不安装')

    ########## 开始检查是目录是否存在或者是否删除目录重下载
    print('开始检查是目录是否存在或者是否删除目录重下载'.center(50, '='))
    if not os.path.isdir(packagePath):
        print(f'{packagePath}目录不存在，新建目录下载')
        os.mkdir(packagePath)
        for n in nes:
            os.system('pip download {} {} -d {}'.format(proxy, n, packagePath))
    elif flag:
        print(f'删除{packagePath}目录后，重新下载')
        shutil.rmtree(packagePath)
        os.mkdir(packagePath)
        for n in nes:
            os.system('pip download {} {} -d {}'.format(proxy, n, packagePath))
    else:
        print(f'已存在{packagePath}目录，不重新下载')

    nes = set([k.lower().split("==")[0] for k in nes])

    ############ 生成requirements.json
    print('生成requirements.json'.center(50, '='))
    os.system('pipdeptree  --packages {}  --json > requirements.json'.format(','.join(nes)))

    ############ 解析库对应的文件名
    print('解析库对应的文件名'.center(50, '='))
    packageDic = {}
    for file in os.listdir(packagePath):
        key = file.split('-')[0].replace('_', '-')
        packageDic[key.lower()] = file
        print(key.lower(), '---', file)

    ############ 解析requirements.json
    print('解析requirements.json'.center(50, '='))
    dependencys = {}
    with open('requirements.json', 'r') as f:
        js = json.load(f)
        for k in js:
            dependencys[k["package"]["key"].lower()] = {}
            if k['dependencies']:
                dependencys[k["package"]["key"].lower()]['depend'] = [i['key'].lower() for i in k['dependencies']]
    finaldic = {}

    # 递归
    def f(keys, index):
        if keys is None:
            return
        for k in keys:
            if k in finaldic:
                if finaldic[k] < index:
                    finaldic[k] = index
                    if 'depend' in dependencys[k]:
                        f(dependencys[k]['depend'], index + 1)
            else:
                finaldic[k] = index
                if 'depend' in dependencys[k]:
                    f(dependencys[k]['depend'], index + 1)
                    f(dependencys[k]['depend'], index + 1)

    print('解析依赖关系'.center(50, '='))
    f(nes, 0)
    finakkeys = sorted(finaldic, key=lambda k: finaldic[k], reverse=True)
    extraKeys = packageDic.keys() - finakkeys
    ############ 生成安装文件
    print('生成安装文件'.center(50, '='))
    with open('install.txt', 'w+', encoding='utf8') as f:
        for k in finakkeys:
            f.write(installtemplate.format(packageDic[k]))
        if len(extraKeys)>0:
            f.write('\n\n')
            for k in extraKeys:
                f.write(installtemplate.format(packageDic[k]))

    ############ 生成卸载文件
    print('生成卸载文件'.center(50, '='))
    with open('uninstall.txt', 'w+', encoding='utf8') as f:
        for k in finakkeys:
            f.write(uninstalltemplate.format(packageDic[k]))
        if len(extraKeys)>0:
            f.write('\n\n')
            for k in extraKeys:
                f.write(uninstalltemplate.format(packageDic[k]))

    ############ 生成说明
    print('生成说明'.center(50, '='))
    with open('readme.txt', 'w+', encoding='utf8') as f:
        f.write('''
        打开install.txt，复制对应的内容，进入packagePath，默认packages目录，打开cmd，进入该目录后，粘贴运行。\n
        删除打开uninstall.txt，同理
        ''')
    print('结束！！'.center(50, '='))


if __name__ == '__main__':
    ''''''
    nes = {'rsa', 'js2py'}
    # nes = {'matplotlib', 'requests', 'pandas', 'xlrd', 'xlwt', 'openpyxl', 'numpy',
    #        'scikit-learn', 'Pillow', 'lxml', 'snowland-smx', 'selenium==2.48', 'aiohttp',
    #        'httpx', 'SQLAlchemy', 'setuptools','pyautogui','pyqt5','opencv-python',
    #        'pyyaml','pycryptodome','pyinstaller','pynput'}
    downloadLib(nes, flag=True, installed=False, useproxy=True)
