---
name: astropy
description: "Astropy 是天文学核心 Python 包，为天文研究和数据分析提供基础功能。触发词：Astropy、天文坐标转换、FITS 文件、天体物理计算、天文单位、天球坐标、宇宙学计算、天文数据处理、SkyCoord、天文学 Python。"
license: BSD-3-Clause license
metadata:
    skill-author: K-Dense Inc.
risk: unknown
source: "https://github.com/astropy/astropy"
---

# Astropy

## 概述

Astropy 是天文学核心 Python 包，为天文研究和数据分析提供基础功能。使用 astropy 进行坐标变换、单位和物理量计算、FITS 文件操作、宇宙学计算、精确时间处理、表格数据操作和天文图像处理。

## 何时使用此技能

当任务涉及以下内容时使用 astropy：
- 天球坐标系之间的转换（ICRS、银道坐标、FK5、AltAz 等）
- 处理物理单位和物理量（将 Jy 转换为 mJy、秒差距转换为 km 等）
- 读取、写入或操作 FITS 文件（图像或表格）
- 宇宙学计算（光度距离、回溯时间、哈勃参数）
- 不同时间尺度和格式的精确时间处理（UTC、TAI、TT、TDB 和 JD、MJD、ISO）
- 表格操作（读取星表、交叉匹配、过滤、连接）
- 像素坐标与世界坐标之间的 WCS 变换
- 天文常数和计算

## 快速入门

```python
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.io import fits
from astropy.table import Table
from astropy.cosmology import Planck18

# 单位和物理量
distance = 100 * u.pc
distance_km = distance.to(u.km)

# 坐标
coord = SkyCoord(ra=10.5*u.degree, dec=41.2*u.degree, frame='icrs')
coord_galactic = coord.galactic

# 时间
t = Time('2023-01-15 12:30:00')
jd = t.jd  # Julian Date

# FITS 文件
data = fits.getdata('image.fits')
header = fits.getheader('image.fits')

# 表格
table = Table.read('catalog.fits')

# 宇宙学
d_L = Planck18.luminosity_distance(z=1.0)
```

## 核心功能

### 1. 单位和物理量（`astropy.units`）

处理带单位的物理量，执行单位转换，确保计算中的量纲一致性。

**关键操作：**
- 通过数值与单位相乘创建物理量
- 使用 `.to()` 方法在单位之间转换
- 执行带自动单位处理的算术运算
- 使用等效性进行领域特定转换（光谱、多普勒、视差）
- 处理对数单位（星等、分贝）

**参见：** `references/units.md` 获取完整文档、单位系统、等效性、性能优化和单位算术。

### 2. 坐标系统（`astropy.coordinates`）

表示天体位置并在不同坐标框架之间转换。

**关键操作：**
- 使用 `SkyCoord` 在任意框架中创建坐标（ICRS、银道坐标、FK5、AltAz 等）
- 在坐标系统之间转换
- 计算角距离和位置角
- 将坐标与星表匹配
- 包含距离以进行 3D 坐标操作
- 处理自行和视向速度
- 从在线数据库查询命名天体

**参见：** `references/coordinates.md` 获取详细坐标框架描述、转换、观测者相关框架（AltAz）、星表匹配和性能技巧。

### 3. 宇宙学计算（`astropy.cosmology`）

使用标准宇宙学模型执行宇宙学计算。

**关键操作：**
- 使用内置宇宙学模型（Planck18、WMAP9 等）
- 创建自定义宇宙学模型
- 计算距离（光度距离、共动距离、角直径距离）
- 计算年龄和回溯时间
- 确定任意红移处的哈勃参数
- 计算密度参数和体积
- 执行逆计算（根据给定距离查找 z）

**参见：** `references/cosmology.md` 获取可用模型、距离计算、时间计算、密度参数和中微子效应。

### 4. FITS 文件处理（`astropy.io.fits`）

读取、写入和操作 FITS（灵活图像传输系统）文件。

**关键操作：**
- 使用上下文管理器打开 FITS 文件
- 通过索引或名称访问 HDU（头数据单元）
- 读取和修改头信息（关键字、注释、历史）
- 处理图像数据（NumPy 数组）
- 处理表格数据（二进制和 ASCII 表）
- 创建新的 FITS 文件（单扩展或多扩展）
- 对大文件使用内存映射
- 访问远程 FITS 文件（S3、HTTP）

**参见：** `references/fits.md` 获取完整文件操作、头信息操作、图像和表格处理、多扩展文件和性能注意事项。

### 5. 表格操作（`astropy.table`）

处理表格数据，支持单位、元数据和多种文件格式。

**关键操作：**
- 从数组、列表或字典创建表格
- 以多种格式读取/写入表格（FITS、CSV、HDF5、VOTable）
- 访问和修改列与行
- 排序、过滤和索引表格
- 执行数据库风格操作（连接、分组、聚合）
- 堆叠和拼接表格
- 处理带单位的列（QTable）
- 使用掩码处理缺失数据

**参见：** `references/tables.md` 获取表格创建、I/O 操作、数据操作、排序、过滤、连接、分组和性能技巧。

### 6. 时间处理（`astropy.time`）

精确的时间表示和时间尺度、格式之间的转换。

**关键操作：**
- 以多种格式创建 Time 对象（ISO、JD、MJD、Unix 等）
- 在时间尺度之间转换（UTC、TAI、TT、TDB 等）
- 使用 TimeDelta 执行时间算术
- 为观测者计算恒星时
- 计算光行时改正（质心、日心）
- 高效处理时间数组
- 处理掩码（缺失）时间

**参见：** `references/time.md` 获取时间格式、时间尺度、转换、算术、观测功能和精度处理。

### 7. 世界坐标系统（`astropy.wcs`）

在图像中的像素坐标与世界坐标之间转换。

**关键操作：**
- 从 FITS 头信息读取 WCS
- 将像素坐标转换为世界坐标（反之亦然）
- 计算图像覆盖范围
- 访问 WCS 参数（参考像素、投影、比例）
- 创建自定义 WCS 对象

**参见：** `references/wcs_and_other_modules.md` 获取 WCS 操作和转换。

## 其他功能

`references/wcs_and_other_modules.md` 文件还涵盖：

### NDData 和 CCDData
带有元数据、不确定性、掩码和 WCS 信息的 n 维数据集容器。

### 建模
为天文数据创建和拟合数学模型的框架。

### 可视化
具有适当拉伸和缩放的天文图像显示工具。

### 常数
带有正确单位的物理和天文常数（光速、太阳质量、普朗克常数等）。

### 卷积
用于平滑和滤波的图像处理核。

### 统计
稳健的统计函数，包括 sigma 裁剪和异常值剔除。

## 安装

```bash
# 安装 astropy
uv pip install astropy

# 安装可选依赖以获得完整功能
uv pip install astropy[all]
```

## 常见工作流

### 在坐标系统之间转换坐标

```python
from astropy.coordinates import SkyCoord
import astropy.units as u

# 创建坐标
c = SkyCoord(ra='05h23m34.5s', dec='-69d45m22s', frame='icrs')

# 转换为银道坐标
c_gal = c.galactic
print(f"l={c_gal.l.deg}, b={c_gal.b.deg}")

# 转换为高度角-方位角（需要时间和位置）
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz

observing_time = Time('2023-06-15 23:00:00')
observing_location = EarthLocation(lat=40*u.deg, lon=-120*u.deg)
aa_frame = AltAz(obstime=observing_time, location=observing_location)
c_altaz = c.transform_to(aa_frame)
print(f"Alt={c_altaz.alt.deg}, Az={c_altaz.az.deg}")
```

### 读取和分析 FITS 文件

```python
from astropy.io import fits
import numpy as np

# 打开 FITS 文件
with fits.open('observation.fits') as hdul:
    # 显示结构
    hdul.info()

    # 获取图像数据和头信息
    data = hdul[1].data
    header = hdul[1].header

    # 访问头信息值
    exptime = header['EXPTIME']
    filter_name = header['FILTER']

    # 分析数据
    mean = np.mean(data)
    median = np.median(data)
    print(f"Mean: {mean}, Median: {median}")
```

### 宇宙学距离计算

```python
from astropy.cosmology import Planck18
import astropy.units as u
import numpy as np

# 计算 z=1.5 处的距离
z = 1.5
d_L = Planck18.luminosity_distance(z)
d_A = Planck18.angular_diameter_distance(z)

print(f"Luminosity distance: {d_L}")
print(f"Angular diameter distance: {d_A}")

# 该红移处的宇宙年龄
age = Planck18.age(z)
print(f"Age at z={z}: {age.to(u.Gyr)}")

# 回溯时间
t_lookback = Planck18.lookback_time(z)
print(f"Lookback time: {t_lookback.to(u.Gyr)}")
```

### 星表交叉匹配

```python
from astropy.table import Table
from astropy.coordinates import SkyCoord, match_coordinates_sky
import astropy.units as u

# 读取星表
cat1 = Table.read('catalog1.fits')
cat2 = Table.read('catalog2.fits')

# 创建坐标对象
coords1 = SkyCoord(ra=cat1['RA']*u.degree, dec=cat1['DEC']*u.degree)
coords2 = SkyCoord(ra=cat2['RA']*u.degree, dec=cat2['DEC']*u.degree)

# 查找匹配
idx, sep, _ = coords1.match_to_catalog_sky(coords2)

# 按分离阈值过滤
max_sep = 1 * u.arcsec
matches = sep < max_sep

# 创建匹配星表
cat1_matched = cat1[matches]
cat2_matched = cat2[idx[matches]]
print(f"Found {len(cat1_matched)} matches")
```

## 最佳实践

1. **始终使用单位**：为物理量附加单位以避免错误并确保量纲一致性
2. **对 FITS 文件使用上下文管理器**：确保正确关闭文件
3. **优先使用数组而非循环**：以数组形式处理多个坐标/时间以获得更好性能
4. **检查坐标框架**：转换前验证框架
5. **使用适当的宇宙学模型**：为分析选择正确的宇宙学模型
6. **处理缺失数据**：对有缺失值的表格使用掩码列
7. **指定时间尺度**：对于精确计时，明确时间尺度（UTC、TT、TDB）
8. **对带单位的表格使用 QTable**：当表格列有单位时
9. **检查 WCS 有效性**：使用转换前验证 WCS
10. **缓存常用值**：昂贵计算（如宇宙学距离）可以缓存

## 文档和资源

- Astropy 官方文档：https://docs.astropy.org/en/stable/
- 教程：https://learn.astropy.org/
- GitHub：https://github.com/astropy/astropy

## 参考文件

特定模块的详细信息：
- `references/units.md` - 单位、物理量、转换和等效性
- `references/coordinates.md` - 坐标系统、转换和星表匹配
- `references/cosmology.md` - 宇宙学模型和计算
- `references/fits.md` - FITS 文件操作和处理
- `references/tables.md` - 表格创建、I/O 和操作
- `references/time.md` - 时间格式、尺度和计算
- `references/wcs_and_other_modules.md` - WCS、NDData、建模、可视化、常数和工具

## 局限性
- 仅当任务明确符合上述描述的范围时使用此技能。
- 不要将输出视为环境特定验证、测试或专家评审的替代品。
- 如果缺少所需输入、权限、安全边界或成功标准，请停止并请求澄清。
