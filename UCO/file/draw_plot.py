import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def format_value(y):
    """智能数值格式化"""
    if y == 0:
        return "0"
    if abs(y) < 0.001:
        return f"{y:.1e}"
    elif abs(y) >= 1000:
        return f"{y:.2e}"
    else:
        return f"{y:.2f}" if y != int(y) else f"{int(y)}"


with open("workdata.csv") as f:
    df = pd.read_csv(f, skipinitialspace=True)

    output_dir = "dataset_plots"
    os.makedirs(output_dir, exist_ok=True)
    df = df.dropna(axis=1, how='all')

    datasets = df['DATASET'].unique()
    all_values = np.concatenate([df.iloc[:, 2:].values.flatten(), 
                            df[df['LABEL'] == 'MAINTENANCE'].iloc[:, 2:].values.flatten()])
    global_min = np.min(all_values)
    global_max = np.max(all_values)

    for dataset in datasets:
        # 筛选数据
        subset = df[df['DATASET'] == dataset]
        uco = subset[subset['LABEL'] == 'UCO'].iloc[0, 2:].astype(float)
        maint = subset[subset['LABEL'] == 'MAINTENANCE'].iloc[0, 2:].astype(float)
        
        # 创建画布
        fig, ax = plt.subplots(figsize=(10, 6))

        uco_line = ax.semilogy(uco.index.astype(int), uco, 
                          marker='o', linestyle='-', linewidth=2, 
                          color='tab:blue', label='UCO', markersize=8)
        maint_line = ax.semilogy(maint.index.astype(int), maint, 
                            marker='s', linestyle='--', linewidth=2,
                            color='tab:red', label='MAINTENANCE', markersize=8)
        
        for i, (x, y) in enumerate(zip(uco.index.astype(int), uco)):
            # UCO标签向上偏移
            va_pos = 'bottom'  # 统一底部对齐
            y_pos = y * 1.6 if y > ax.get_ylim()[1]/10 else y * 1.4  # 增大偏移系数
            ax.text(x, y_pos, 
                    format_value(y),
                    color='tab:blue', fontsize=9, ha='center', 
                    va=va_pos, rotation=0, alpha=0.9)

        for i, (x, y) in enumerate(zip(maint.index.astype(int), maint)):
            # MAINTENANCE标签向上微调
            va_pos = 'bottom' if y > ax.get_ylim()[1]/10 else 'top'
            y_pos = y * 1.3 if y > ax.get_ylim()[1]/10 else y * 0.7  # 调整偏移方向
            ax.text(x, y_pos,
                    format_value(y),
                    color='tab:red', fontsize=9, ha='center',
                    va=va_pos, rotation=0, alpha=0.9)
        
        
        # 统一坐标轴设置
        ax.set_ylim(max(global_min, 1e-7), global_max*1.5)  # 保留安全边距
        ax.set_xlabel('Data Points (1-10)', fontsize=12)
        ax.set_ylabel('Logarithmic Values', fontsize=12)
        ax.grid(True, which='both', linestyle='--', alpha=0.5)
        ax.set_title(f"{dataset} - Log Scale Comparison", pad=15, fontsize=14)
        
        # 优化刻度标签
        ax.yaxis.set_major_formatter(plt.ScalarFormatter())
        ax.yaxis.set_minor_formatter(plt.NullFormatter())
        
        # 组合图例
        ax.legend(ncol=2, loc='upper center', 
                bbox_to_anchor=(0.5, 1.15),
                frameon=False,
                fontsize=10)
        
        # 保存图片
        filename = f"{dataset.replace(' ', '_').replace('.', '_')}_log.png"
        plt.savefig(os.path.join(output_dir, filename), 
                dpi=300, bbox_inches='tight')
        plt.close()


print(f"已生成 {len(datasets)} 张图表，保存至 {output_dir} 目录")