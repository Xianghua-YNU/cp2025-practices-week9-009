"""
项目2: L-System分形生成与绘图模板
请补全下方函数，实现L-System字符串生成与绘图。
"""
import matplotlib.pyplot as plt
import math

def apply_rules(axiom, rules, iterations):
    """
    生成L-System字符串
    :param axiom: 初始字符串（如"F"或"0"）
    :param rules: 规则字典，如{"F": "F+F--F+F"} 或 {"1": "11", "0": "1[0]0"}
    :param iterations: 迭代次数
    :return: 经过多轮迭代后的最终字符串
    """
    # TODO: 实现L-System字符串生成逻辑
    current = axiom
    for _ in range(iterations):
        next_seq = []
        for c in current:
            next_seq.append(rules.get(c, c))
        current = ''.join(next_seq)
    return current

def draw_l_system(instructions, angle, step, start_pos=(0,0), start_angle=0, savefile=None):
    """
    根据L-System指令绘图
    :param instructions: 指令字符串（如"F+F--F+F"）
    :param angle: 每次转向的角度（度）
    :param step: 每步前进的长度
    :param start_pos: 起始坐标 (x, y)
    :param start_angle: 起始角度（0表示向右，90表示向上）
    :param savefile: 若指定则保存为图片文件，否则直接显示
    """
    # TODO: 实现L-System绘图逻辑
    x, y = initial_pos
    current_angle = initial_angle
    stack = []
    fig, ax = plt.subplots()
    for cmd in commands:
        # 向前绘制
        if cmd in ('F', '0', '1'):
            nx = x + step * math.cos(math.radians(current_angle))
            ny = y + step * math.sin(math.radians(current_angle))
            ax.plot([x, nx], [y, ny], color='green' if tree_mode else 'blue', linewidth=1.2 if tree_mode else 1)
            x, y = nx, ny
        # 向前移动但不绘制    
        elif cmd == 'f':
            x += step * math.cos(math.radians(current_angle))
            y += step * math.sin(math.radians(current_angle))
        # 左转
        elif cmd == '+':
            current_angle += angle_deg
        # 右转    
        elif cmd == '-':
            current_angle -= angle_deg
        # 压栈(保存状态)    
        elif cmd == '[':
            stack.append((x, y, current_angle))
            if tree_mode:
                current_angle += angle_deg
        # 出栈(恢复状态)        
        elif cmd == ']':
            x, y, current_angle = stack.pop()
            if tree_mode:
                current_angle -= angle_deg 
    ax.set_aspect('equal')
    ax.axis('off')
    if savefile:
        plt.savefig(savefile, bbox_inches='tight', pad_inches=0.1, dpi=150)
        plt.close()
    else:
        plt.show()
        
if __name__ == "__main__":
    """
    主程序示例：分别生成并绘制科赫曲线和分形二叉树
    学生可根据下方示例，调整参数体验不同分形效果
    """
    # Koch curve parameters 科赫曲线
    koch_axiom = "F"
    koch_rules = {'F': 'F+F--F+F'}
    koch_angle = 60
    koch_iter = 4
    koch_step = 5
    koch_cmds = apply_rules(koch_axiom, koch_rules, koch_iter)
    plt.figure(figsize=(10, 3))
    draw_l_system(koch_cmds, koch_angle, koch_step, initial_pos=(0, 0), initial_angle=0)
    plt.title("L-System Koch Curve")
    plt.axis('equal')
    plt.axis('off')
    plt.show()

    # Fractal tree parameters 分形树
    tree_axiom = "0"
    tree_rules = {'1': '11', '0': '1[0]0'}
    tree_angle = 45
    tree_iter = 7
    tree_step = 7
    tree_cmds = apply_rules(tree_axiom, tree_rules, tree_iter)
    plt.figure(figsize=(7, 7))
    draw_l_system(tree_cmds, tree_angle, tree_step, initial_pos=(0, 0), initial_angle=90, tree_mode=True)
    plt.title("L-System Fractal Tree")
    plt.axis('equal')
    plt.axis('off')
    plt.show()
