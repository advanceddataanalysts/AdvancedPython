## Linux中生成的图片中文编码问题

```shell
# 全局安装中文字体
yum -y groupinstall chinese-support
yum -y groupinstall mkfontscale

# 手动刷新缓存
mkfontscale
mkfontdir
fc-cache
```





## Matplotlib中文编码问题

#### 在Linux上运行matplotlib时会因中文编码问题造成乱码 ,解决方案为下载一个字体包并将其导入到Linux上的matplotlib中

1. 下载*arial unicode ms.ttf* 的字体

2. 拷贝一份到matplotlib中 ,路径为

   ```shell
   cp arial\ unicode\ ms.ttf  /root/.virtualenvs/datatimer/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf
   ```

3. 重命名

   ```shell
   cd /root/.virtualenvs/datatimer/lib/python3.6/site-packages/matplotlib/mpl-data/fonts/ttf
   cp arial\ unicode\ ms.ttf  Vera.ttf
   ```

4. 删除字体缓存

   ```shell
   cd ~/.cache/matplotlib/
   rm -rf fontlist-v300.json
   ```

5. python脚本中添加

   ```shell
   import matplotlib.pyplot as plt
   plt.rcParams['font.family'] = ['Arial Unicode MS', 'sans-serif'] #  全局设置支持中文字体，默认 sans-serif
   ```

   

