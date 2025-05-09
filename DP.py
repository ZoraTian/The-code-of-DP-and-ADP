import numpy as np
import matplotlib.pyplot as plt

# 参数定义
T = 7
SOC_list = [0.3, 0.4, 0.5, 0.6, 0.7]
P_list = np.linspace(-1, 1, 21)  # 动作粒度为 0.1
demand = 0.3
buy_price = [0, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]  # t=1~5 有电价
sell_price = 0.5

# 映射
SOC_to_idx = {v: i for i, v in enumerate(SOC_list)}
idx_to_SOC = {i: v for i, v in enumerate(SOC_list)}

# 初始化值函数表（T x |SOC|），T-1个决策点，T=6是终态
V_table = np.zeros((T, len(SOC_list)))
P_table = np.zeros((T, len(SOC_list)))
# DP主过程：从T-2到0反向遍历
for t in reversed(range(T - 1)):
    best_cost = float('inf')
    best_p = 0
    for i, soc in enumerate(SOC_list):
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
        V_table[t, i] = np.round(best_cost,2)  # 只记录值函数，不记录动作
        P_table[t, i] = np.round(best_p,2)
        if t == 0 and i !=2:
            V_table[t, i] = 0.0

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
print(V_table)
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
