# vlppy 库

## 介绍

1. start date:  2022-08-26
2. auther:  yangwuju
3. url：https://gitee.com/yangwuju/vlppy.git
4. description:  Quickly build visible light localization models.

## 安装教程

```powershell
python -m pip install vlppy
```

## 软件架构

* model/room：房间、墙壁参数
* model/led：led位置、发射的信号(None、DC、AC、AIM)
* model/pd：pd 各种参数、LOS链路和NLOS链路接收LED信号、噪声
* model/pd2: 在原有的基础上增加了pd的角度特征
* signal/filter：滤波器设计（包括fir,iir）
* signal/plot：绘制波形图
* demo/vlp_model：可见光定位模型
* demo/demo_main：可见光定位测试例程
* demo/demo_filter：滤波器测试例程
* io/io：数据保存与加载
* setting/json_setting：加载json配置文件
* error/error：VLP常见异常
* vis/vis：可视化绘图
* tools/decorator：VLP可能用到的装饰器

## 例程

### 1.滤波器例程

```python
from vlppy import demo

demo.demo_filter.main()
```

### 2.可见光定位例程

```python
from vlppy import demo

demo.demo_main.main()
demo.demo_main.test_func()
```

## 使用教程

### 1. 模型参数定义

* 新建一个 **settings.json** 文件
* 在 **settings.json** 文件添加模型参数

```json
{
    "Room": {
        "size":{  
	    ...
        }, // 房间尺寸
        "wall":{
            ...
        } // 反射墙壁
    }, // 房间
    "PD":{  
        "PD1":{
            ...
        },
        "PD2":{
            ...
        }
    }, // 光电探测器
    "LED": {
        "LED1": {
	    ...
        }
    }  // 发光二极管 
}
```

* 加载模型参数

```python
from vlppy.setting import Settings
Args = Settings('settings.json') # 模型参数包含在字典 Args.items 中
```

### 2. 搭建模型

新建一个模型类 **VLP_Model**

```python
import numpy as np
import matplotlib.pyplot as plt
from vlppy.model import LED,PD,Room
from vlppy.signal import filter,plot

class VLP_Model:
    def __init__(self, *args, **kwargs):
	"""初始化模型
	"""
	self.room = Room(...)
	self.pd = PD(...)
	self.led = LED(...)

    def get_data(self):
	"""计算PD接收LED功率
	"""
	P_PD = self.pd.recv_led_signal(led=self.led, room=self.room) 
	X, Y, Z = self.room.get_tp_pos(fmt='c')
	return (P_PD, X, Y, Z)

    def show(self,z,savepath=...,showfig=True):
        """绘图
        z: 功率数据
	savepath: 保存路径
	showfig: 是否显示
        """
        xr, yr, _ = self.room.get_tp_grid()
        z = np.reshape(z, xr.shape)  
        ax = plt.axes(projection='3d')
        ax.plot_surface(xr, yr, z, cmap='viridis', edgecolor='none')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        if savepath != ...:
            plt.savefig(savepath)
        if showfig:
            plt.show()
```

### 3. 加载模型

```python
def main():
    cm = VLP_Model(**Args.items)
    (P,X,Y,Z) = cm.get_data()
  
    # 绘图
    cm.show(P)
```

### 4. 保存数据

```python
from vlppy.io import IO

# 保存文件路径
filepath = ...

data = {
    "P": P,
    "X": X,
    "Y": Y,
    "Z": Z
}

# 保存数据
io = IO() 
io.save_excel(filepath, data)
```

### 5. 查看数据

```python
from vlppy.io import IO

# 文件路径
filepath = ...

# 加载数据
io = IO() 
data = io.load_excel(filepath)

# 查看数据形状
print(data.shape)
```
