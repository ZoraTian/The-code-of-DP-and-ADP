import numpy as np
import matplotlib.pyplot as plt

# --- 基本设置 ---
T = 7
SOC_list = [0.3, 0.4, 0.5, 0.6, 0.7]
P_list = np.linspace(-1,1,21)
demand = 0.3
buy_price = [0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # t=1~5 有价，其余设为0
sell_price = 0.5
alpha = 0.2
episodes = 500

# 映射
SOC_to_idx = {v: i for i, v in enumerate(SOC_list)}
idx_to_SOC = {i: v for i, v in enumerate(SOC_list)}

# 初始化值函数表 V(t, soc)
V_table = np.zeros((T, len(SOC_list)))

# --- 训练阶段：近似动态规划 ---
for ep in range(episodes):
    soc = 0.5  # 固定初始SOC
    for t in range(T - 1):  # 最后一时段不需更新
        best_cost = float('inf')
        best_p = 0
        for p in P_list:
            soc_next = np.round(soc - p,1)
            if soc_next not in SOC_list:
                continue
            # 即时成本计算（用户购/卖电）
            net = p - demand
            if net > 0:
                stage_cost = -net * sell_price
            else:
                stage_cost = -net * buy_price[t + 1]

            idx_next = SOC_to_idx[soc_next]
            total_cost = stage_cost + V_table[t + 1, idx_next]

            if total_cost < best_cost:
                best_cost = total_cost
                best_p = p

        idx_now = SOC_to_idx[soc]
        V_table[t, idx_now] = (1 - alpha) * V_table[t, idx_now] + alpha * best_cost
        soc = np.round(soc - best_p,1)  # 状态前向推进（沿路径）
print(np.round(V_table,4))
# --- 策略执行阶段（按公式 34） ---
soc = 0.5
trajectory_SOC = [soc]
trajectory_Pbat = []
trajectory_Cost = []

for t in range(T - 1):
    best_cost = float('inf')
    best_p = 0
    for p in P_list:
        soc_next = np.round(soc - p,1)
        if soc_next not in SOC_list:
            continue
        net = p - demand
        if net > 0:
            cost_now = -net * sell_price
        else:
            cost_now = -net * buy_price[t + 1]
        idx_next = SOC_to_idx[soc_next]
        total_cost = cost_now + V_table[t + 1, idx_next]

        if total_cost < best_cost:
            best_cost = total_cost
            best_p = p

    trajectory_Pbat.append(best_p)
    trajectory_Cost.append(best_cost)
    soc = np.round(soc - best_p,1)
    trajectory_SOC.append(soc)

# --- 输出结果 ---
print("时段 | SOC  | Pbat | 成本")
for t in range(T - 1):
    print(f"{t:>3}  | {trajectory_SOC[t]:.2f} | {trajectory_Pbat[t]:.2f} | {trajectory_Cost[t]:.2f}")
print(f"最终SOC: {trajectory_SOC[-1]:.2f}，总成本: {sum(trajectory_Cost):.2f}")

# --- 可视化 ---
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(range(T), trajectory_SOC, marker='o', label="SOC")
plt.xlabel("Time")
plt.ylabel("SOC")
plt.title("SOC Trajectory")
plt.grid(True)
plt.legend()

plt.subplot(1, 2, 2)
plt.step(range(T - 1), trajectory_Pbat, where='post', marker='x', label="Pbat")
plt.xlabel("Time")
plt.ylabel("Power (kW)")
plt.title("Battery Power Trajectory")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
