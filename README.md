# pyscaling — 基于向量空间搜索引擎的验证码识别小程序

![Python](https://img.shields.io/badge/python-2.7-blue.svg)
![PIL](https://img.shields.io/badge/dependency-Pillow-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

一个使用 **基本向量空间搜索引擎**（Vector Space Search）识别规整型验证码的小程序。无需深度学习框架，仅依靠 Pillow + 余弦相似度模板匹配，即可完成「预处理 → 切割 → 训练 → 识别」全流程，是理解传统图像识别思路的绝佳练手项目。

## ✨ 特性

- 🧩 **零深度学习依赖** —— 只用 Pillow / numpy / matplotlib，Python 2.7 即可运行
- 📐 **经典算法** —— 向量空间模型 + 余弦相似度，把每个字符图像展开为像素向量做匹配
- 🎨 **颜色直方图定位** —— 自动统计颜色索引，一键分离前景与干扰像素
- ✂️ **自动字符切割** —— 基于投影分析的连通区域切分，产出单字符训练样本
- 🗂️ **自带训练集** —— `iconset/` 内置 0-9 / a-z 的标准字符模板库

## 🔍 识别原理

```
原始验证码 ──► 颜色直方图统计 ──► 二值化(提取 220/227 索引) ──► 字符切割
                                                                │
识别结果 ◄── 余弦相似度排序 ◄── 向量化(OverZoom) ◄── 模板库训练 ◄─┘
```

| 步骤 | 说明 |
| --- | --- |
| 1. 颜色直方图 | `catch_histogram.HisToGram()` 统计各颜色索引出现频率，锁定验证码字符所在的颜色索引值（本项目为 220 / 227） |
| 2. 二值化 | `convert_two_pic([220, 227])` 把命中的像素置黑、其余置白，得到纯净黑白图 |
| 3. 字符切割 | `conver_one_pic_1/2` 先求整图字符包围盒，再按列投影切出每个单字符 |
| 4. 向量化 | `OverZoom()` 把单字符图展开为 `{像素下标: 像素值}` 的向量 |
| 5. 训练 | `Train()` 遍历 `iconset/<字符>/` 全部模板图，切割 + 向量化后构建训练集 |
| 6. 识别 | `VectorCompare.selfAdd()` 计算测试向量与全部模板的余弦相似度，取最大者 |

> 💡 核心思想：两张图越相似，其像素向量的夹角越小、余弦值越接近 1。

## 🚀 快速开始

```bash
git clone https://github.com/lijishuang/pyscaling.git
cd pyscaling

# 依赖（Python 2.7）
pip install Pillow numpy matplotlib

# 识别示例验证码 pic.gif
python loons.py
```

输出示例：

```text
(6, 8, 14, 20)
(15, 8, 25, 20)
...
[(0.9137931, '7'), (0.8988216, 's'), (0.8051091, '9'),
 (0.9593813, 't'), (0.9072221, '9'), (0.8757605, 'j')]
```

即验证码 `pic.gif` 被识别为 **`7s9t9j`**（括号内为各字符的匹配置信度）。

## 📁 项目结构

```text
pyscaling/
├── loons.py          # 主程序：loons 识别类 + catch_histogram 直方图类
├── pic.gif           # 待识别的示例验证码
├── iconset/          # 训练模板库：0-9、a-z 各字符的标准样本（GIF）
├── res/              # 训练过程产出的切割样本（运行时生成）
└── tempCodeRunnerFile.py
```

## 🎯 识别范围与局限

✅ 适用：数字 + 小写字母组合、字符排列规整、无旋转/粘连的验证码
❌ 不适用：扭曲变形、字符粘连、带干扰线或噪点复杂的验证码

若要识别新类型的验证码：

1. 用 `catch_histogram("新图.gif").HisToGram()` 找到新的颜色索引值
2. 将索引值代入 `convert_two_pic([...])`
3. 在 `iconset/` 中补充对应字符的新模板样本

## ⚠️ 免责声明

本项目仅供 **图像处理与机器学习入门学习** 使用。请勿将其用于任何违反法律法规或目标网站服务条款的用途（包括但不限于批量破解验证码、绕过安全机制）。使用者需自行承担一切法律责任。

## 📄 License

MIT
