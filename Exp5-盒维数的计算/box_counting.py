"""
项目5: 盒计数法估算分形维数
实现盒计数算法计算分形图像的盒维数

任务说明：
1. 实现盒计数算法计算分形图像的盒维数
2. 完成以下函数实现
3. 在main函数中测试你的实现
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def load_and_binarize_image(image_path, threshold=128):
    """
    加载图像并转换为二值数组
    
    参数：
    image_path -- 图像文件路径（字符串）
    threshold -- 二值化阈值（0-255之间的整数，默认128）
    
    返回：
    二值化的NumPy数组（0和1组成）
    
    实现步骤：
    1. 使用PIL.Image打开图像并转换为灰度
    2. 转换为NumPy数组
    3. 根据阈值进行二值化处理
    """
    # TODO: 实现图像加载和二值化
    # ... your code here ...
    # 打开图像并转换为灰度
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)
    
    # 二值化处理
    binary_array = np.where(img_array > threshold, 1, 0)
    
    return binary_array
    
def box_count(binary_image, box_sizes):
    """
    盒计数算法实现
    
    参数：
    binary_image -- 二值图像数组（0和1组成的NumPy数组）
    box_sizes -- 盒子尺寸列表（整数列表）
    
    返回：
    字典 {box_size: count}，记录每个盒子尺寸对应的非空盒子数量
    
    实现步骤：
    1. 获取图像高度和宽度
    2. 遍历每个盒子尺寸：
       a. 计算网格行列数
       b. 遍历所有盒子区域
       c. 统计包含前景像素的盒子数量
    """
    # TODO: 实现盒计数算法
    # ... your code here ...
    height, width = binary_image.shape
    counts = {}
    
    for box_size in box_sizes:
        # 计算网格行列数
        rows = height // box_size
        cols = width // box_size
        
        # 如果图像尺寸不是盒子尺寸的整数倍，增加一行/列
        if height % box_size != 0:
            rows += 1
        if width % box_size != 0:
            cols += 1
            
        count = 0
        
        # 遍历所有盒子
        for i in range(rows):
            for j in range(cols):
                # 计算当前盒子区域
                y_start = i * box_size
                y_end = min((i + 1) * box_size, height)
                x_start = j * box_size
                x_end = min((j + 1) * box_size, width)

                # 检查盒子是否包含前景像素
                box = binary_image[y_start:y_end, x_start:x_end]
                if np.any(box == 1):
                    count += 1
                    
        counts[box_size] = count
        
    return counts
    
def calculate_fractal_dimension(binary_image, min_box_size=1, max_box_size=None, num_sizes=10):
    """
    计算分形维数
    
    参数：
    binary_image -- 二值图像数组
    min_box_size -- 最小盒子尺寸（默认1）
    max_box_size -- 最大盒子尺寸（默认图像最小尺寸的一半）
    num_sizes -- 盒子尺寸数量（默认10）
    
    返回：
    盒维数D, 元组(epsilons, N_epsilons, slope, intercept)
    
    实现步骤：
    1. 生成等比数列的盒子尺寸
    2. 调用box_count获取计数结果
    3. 对结果进行对数变换
    4. 使用线性回归计算斜率
    """
    # TODO: 实现分形维数计算
    # ... your code here ...
    height, width = binary_image.shape
    
    # 设置最大盒子尺寸
    if max_box_size is None:
        max_box_size = min(height, width) // 2
        
    # 生成等比数列的盒子尺寸
    box_sizes = np.logspace(np.log2(min_box_size), np.log2(max_box_size), 
                           num=num_sizes, base=2, dtype=int)
    box_sizes = np.unique(box_sizes)  # 去除重复值
    box_sizes = box_sizes[box_sizes > 0]  # 确保没有0尺寸
    
    # 获取盒计数结果
    counts = box_count(binary_image, box_sizes)
    epsilons = np.array(list(counts.keys()))
    N_epsilons = np.array(list(counts.values()))
    
    # 对数变换
    log_eps = np.log(epsilons)
    log_N = np.log(N_epsilons)
    
    # 线性回归
    slope, intercept = np.polyfit(log_eps, log_N, 1)
    D = -slope
    
    return D, (epsilons, N_epsilons, slope, intercept)

def plot_log_log(epsilons, N_epsilons, slope, intercept, save_path=None):
    """
    绘制log-log图
    
    参数：
    epsilons -- 盒子尺寸列表
    N_epsilons -- 对应的盒子计数列表
    slope -- 拟合直线斜率
    intercept -- 拟合直线截距
    save_path -- 图片保存路径（可选）
    
    实现步骤：
    1. 对数变换
    2. 绘制散点图
    3. 绘制拟合直线
    4. 添加标签和图例
    """
    # TODO: 实现log-log图绘制
    # ... your code here ...
    log_eps = np.log(epsilons)
    log_N = np.log(N_epsilons)
    
    plt.figure(figsize=(8, 6))
    plt.scatter(log_eps, log_N, color='b', label='Data points')
    
    # 绘制拟合直线
    fit_line = slope * log_eps + intercept
    plt.plot(log_eps, fit_line, 'r-', 
             label=f'Fit line (slope={-slope:.3f})')
    
    plt.xlabel('log(ε)')
    plt.ylabel('log(N(ε))')
    plt.title('Log-log plot for box counting')
    plt.legend()
    plt.grid(True)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

if __name__ == "__main__":
    """
    主函数 - 测试你的实现
    
    实现步骤：
    1. 加载并二值化图像
    2. 计算分形维数
    3. 输出结果
    4. 绘制log-log图
    
    测试说明：
    1. 使用项目提供的测试图像或自己准备的图像
    2. 比较计算结果与理论值
    """
    # TODO: 实现主函数测试
    # 示例路径，请根据实际情况修改
    IMAGE_PATH = "../../images/barnsley_fern.png"  
    
    # 1. 加载并二值化图像
    # binary_img = load_and_binarize_image(IMAGE_PATH)
    
    # 2. 计算分形维数
    D, results = calculate_fractal_dimension(binary_img)
    epsilons, N_epsilons, slope, intercept = results
    
    # 3. 输出结果
    print("盒计数结果:")
        for eps, count in zip(epsilons, N_epsilons):
            print(f"ε = {eps:4d}, N(ε) = {count:6d}, log(ε) = {np.log(eps):.3f}, log(N(ε)) = {np.log(count):.3f}")
        
        print(f"\n线性回归斜率: {slope:.5f}")
        print(f"估算的盒维数 D = {D:.5f}")
    
    # 4. 绘制log-log图
    plot_log_log(*results[1:], "log_log_plot.png")
        
    except FileNotFoundError:
        print(f"错误：找不到图像文件 {IMAGE_PATH}")
        print("请确保路径正确，或者使用其他图像文件")
    except Exception as e:
        print(f"发生错误: {str(e)}")
