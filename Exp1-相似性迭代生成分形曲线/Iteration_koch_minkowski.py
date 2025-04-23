import numpy as np
import matplotlib.pyplot as plt

def koch_generator(u, level):
    """
    递归/迭代生成科赫曲线的点序列。

    参数:
        u: 初始线段的端点数组（复数表示）
        level: 迭代层数

    返回:
        numpy.ndarray: 生成的所有点（复数数组）
    """
    if level == 0:
        return u
    
    points = np.array([], dtype=np.complex128)
    for i in range(len(u)-1):
        start = u[i]
        end = u[i+1]
        vec = end - start
        
        # 科赫曲线的生成规则：将线段分为4段，添加3个新点
        p0 = start
        p1 = start + vec / 3
        p2 = p1 + vec / 3 * np.exp(1j * np.pi/3)
        p3 = start + 2 * vec / 3
        p4 = end
        
        segment = np.array([p0, p1, p2, p3, p4])
        points = np.concatenate((points, segment)) if points.size else segment
    
    # 移除重复的端点（除了最后一个）
    points = np.unique(points)
    points = np.append(points, end)
    
    return koch_generator(points, level-1)

def minkowski_generator(u, level):
    """
    递归/迭代生成闵可夫斯基香肠曲线的点序列。

    参数:
        u: 初始线段的端点数组（复数表示）
        level: 迭代层数

    返回:
        numpy.ndarray: 生成的所有点（复数数组）
    """
    if level == 0:
        return u
    
    points = np.array([], dtype=np.complex128)
    for i in range(len(u)-1):
        start = u[i]
        end = u[i+1]
        vec = end - start
        
        # 闵可夫斯基香肠的生成规则：将线段分为8段，添加7个新点
        p0 = start
        p1 = start + vec / 8
        p2 = p1 + vec / 8 * 1j
        p3 = p2 + vec / 8
        p4 = p3 + vec / 8 * (-1j)
        p5 = p4 + vec / 8 * (-1j)
        p6 = p5 + vec / 8
        p7 = p6 + vec / 8 * 1j
        p8 = end
        
        segment = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8])
        points = np.concatenate((points, segment)) if points.size else segment
    
    # 移除重复的端点（除了最后一个）
    points = np.unique(points)
    points = np.append(points, end)
    
    return minkowski_generator(points, level-1)

if __name__ == "__main__":
    # 初始线段（复数表示）
    init_u = np.array([0 + 0j, 1 + 0j], dtype=np.complex128)

    # 绘制不同层级的科赫曲线
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for i in range(4):
        koch_points = koch_generator(init_u, i+1)
        axs[i//2, i%2].plot(
            np.real(koch_points), np.imag(koch_points), 'k-', lw=1
        )
        axs[i//2, i%2].set_title(f"Koch Curve Level {i+1}")
        axs[i//2, i%2].axis('equal')
        axs[i//2, i%2].axis('off')
    plt.tight_layout()
    plt.savefig('koch_curves.png')
    plt.show()

    # 绘制不同层级的闵可夫斯基香肠曲线
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))
    for i in range(4):
        minkowski_points = minkowski_generator(init_u, i+1)
        axs[i//2, i%2].plot(
            np.real(minkowski_points), np.imag(minkowski_points), 'k-', lw=1
        )
        axs[i//2, i%2].set_title(f"Minkowski Sausage Level {i+1}")
        axs[i//2, i%2].axis('equal')
        axs[i//2, i%2].axis('off')
    plt.tight_layout()
    plt.savefig('minkowski_sausages.png')
    plt.show()
