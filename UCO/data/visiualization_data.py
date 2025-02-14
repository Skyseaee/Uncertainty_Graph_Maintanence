import os
import fire
import pandas as pd
import matplotlib.pyplot as plt

def analyze_graph(file_path, degree_plot_path='degree_plot', probability_plot_path='probability_plot'):
    """
    统计图的度分布和概率分布，并保存对应的图表。

    参数：
        file_path (str): 输入文件路径，文件每行格式为 a,b,probability。
        degree_plot_path (str): 度分布柱状图的保存路径。
        probability_plot_path (str): 概率分布直方图的保存路径。
    """
    # 加载数据
    data = pd.read_csv(file_path, header=None, names=['a', 'b', 'probability'], delim_whitespace=True)
    data['probability'] = data['probability'] / data['probability'].max()
    tmp_name = file_path.split('.')[0]
    # 统计每个点的度
    degree_count = {}
    maxs = 0
    for a, b in zip(data['a'], data['b']):
        degree_count[a] = degree_count.get(a, 0) + 1
        degree_count[b] = degree_count.get(b, 0) + 1
        maxs = max(maxs, degree_count[a], degree_count[b])

    mins = len(degree_count)
    for _, b in degree_count.items():
        mins = min(mins, b)
    
    bars = [0 for _ in range(maxs-mins+2)]
    for _, b in degree_count.items():
        bars[b-mins+1] += 1
    
    # 转换为 DataFrame 方便统计
    x_ticks = list(range(mins, maxs + 2))
    
    # 绘制度分布柱状图
    plt.figure(figsize=(10, 6))
    plt.bar(x_ticks, bars, color='skyblue')
    plt.xticks(range(mins, maxs + 2))
    plt.xlabel('Degree')
    plt.ylabel('Count')
    plt.title(f'{tmp_name} Degree')
    plt.tight_layout()
    plt.savefig(os.path.join(degree_plot_path, tmp_name))  # 保存度分布图
    plt.close()

    # 绘制概率分布直方图
    plt.figure(figsize=(10, 6))
    plt.hist(data['probability'], bins=20, color='orange', alpha=0.7, edgecolor='black')
    plt.xlabel('Probability')
    plt.ylabel('Frequency')
    plt.title(f'{tmp_name} Edge Probability')
    plt.tight_layout()
    plt.savefig(os.path.join(probability_plot_path, tmp_name))  # 保存概率分布图
    plt.close()

    print(f"度分布图已保存至: {degree_plot_path}")
    print(f"概率分布图已保存至: {probability_plot_path}")

# 示例用法
# analyze_graph('graph_data.txt', 'degree_distribution.png', 'probability_distribution.png')
if __name__ == '__main__':
    fire.Fire(analyze_graph)