import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Khởi tạo tham số
np.random.seed(42)
n_simulations = 10000
base_npv_epv = 76.13 

# 1. Gán phân phối rủi ro
exchange_rate = np.random.normal(44, 2, n_simulations)
yarn_price = np.random.triangular(1.3, 1.5, 1.8, n_simulations)
cotton_price = np.randomimport numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập UI/UX cho biểu đồ chuẩn báo cáo doanh nghiệp
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.family': 'sans-serif'})

# 1. KHỞI TẠO ENGINE MÔ PHỎNG (10.000 Trials)
np.random.seed(42)
n_simulations = 10000
base_npv = 76.13 # Trích xuất từ Phương án 5 - Excel

# Gán phân phối rủi ro (Assumptions)
exchange_rate = np.random.normal(44, 2, n_simulations)
yarn_price = np.random.triangular(1.3, 1.5, 1.8, n_simulations)
cotton_price = np.random.normal(1.0, 0.1, n_simulations)

# Ma trận độ nhạy (Linear Approximation Core)
dy = (yarn_price - 1.5) / 1.5 * 100 * 5       
dc = (cotton_price - 1.0) / 1.0 * 100 * (-3) 
de = (exchange_rate - 44) / 44 * 100 * 2         

# Dòng tiền Stochastic
simulated_npv = base_npv + dy + dc + de
mean_npv = np.mean(simulated_npv)
prob_negative = np.sum(simulated_npv < 0) / n_simulations * 100

# ==========================================
# 2. RENDER BIỂU ĐỒ 1: HISTOGRAM (PHÂN PHỐI RỦI RO)
# ==========================================
plt.figure(figsize=(10, 6))
sns.histplot(simulated_npv, bins=60, kde=True, color='#0ea5e9', edgecolor='white')
plt.axvline(x=0, color='#ef4444', linestyle='--', linewidth=2.5, label=f'Rủi ro (NPV < 0): {prob_negative:.2f}%')
plt.axvline(x=mean_npv, color='#10b981', linestyle='-', linewidth=2.5, label=f'Kỳ vọng (Mean NPV): {mean_npv:.2f}')
plt.title('PHÂN PHỐI XÁC SUẤT NPV - PHƯƠNG ÁN 5', fontsize=15, fontweight='bold', pad=15)
plt.xlabel('Giá trị NPV (Triệu Bt)', fontsize=12)
plt.ylabel('Tần suất (10,000 Vòng lặp)', fontsize=12)
plt.legend(fontsize=11)
plt.tight_layout()
plt.savefig('Slide_5_Histogram.png', dpi=300)
plt.close()

# ==========================================
# 3. RENDER BIỂU ĐỒ 2: TORNADO CHART (ĐỘ NHẠY)
# ==========================================
yarn_min, yarn_max = np.percentile(yarn_price, [5, 95]) 
cotton_min, cotton_max = np.percentile(cotton_price, [5, 95])
er_min, er_max = np.percentile(exchange_rate, [5, 95])

def calc_npv(y, c, e):
    return base_npv + ((y - 1.5)/1.5*500) + ((c - 1.0)/1.0*-300) + ((e - 44)/44*200)

sens = [
    ('Giá Sợi (Đầu ra)', calc_npv(yarn_min, 1.0, 44), calc_npv(yarn_max, 1.0, 44)),
    ('Giá Bông (Đầu vào)', calc_npv(1.5, cotton_min, 44), calc_npv(1.5, cotton_max, 44)),
    ('Tỷ Giá (Bt/USD)', calc_npv(1.5, 1.0, er_min), calc_npv(1.5, 1.0, er_max))
]
# Sắp xếp theo biên độ dao động
sens.sort(key=lambda x: abs(x[2] - x[1]))

labels = [x[0] for x in sens]
mins = [x[1] for x in sens]
maxs = [x[2] for x in sens]

fig, ax = plt.subplots(figsize=(10, 5))
y_pos = np.arange(len(labels))

for i in range(len(labels)):
    ax.barh(y_pos[i], mins[i] - base_npv, left=base_npv, color='#ef4444' if mins[i] < base_npv else '#10b981', height=0.4)
    ax.barh(y_pos[i], maxs[i] - base_npv, left=base_npv, color='#10b981' if maxs[i] >= base_npv else '#ef4444', height=0.4)

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=12, fontweight='bold')
ax.axvline(base_npv, color='#334155', linestyle='--', linewidth=2)
ax.set_xlabel('Mức độ dao động NPV (Triệu Bt)', fontsize=12)
ax.set_title('TORNADO CHART - PHÂN TÍCH ĐỘ NHẠY', fontsize=15, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('Slide_6_Tornado.png', dpi=300)
plt.close()

print("Hoàn tất! Đã lưu 2 ảnh: Slide_5_Histogram.png và Slide_6_Tornado.png").normal(1.0, 0.1, n_simulations)

# 2. Xử lý độ nhạy
delta_yarn = (yarn_price - 1.5) / 1.5 * 100 * 5       
delta_cotton = (cotton_price - 1.0) / 1.0 * 100 * (-3) 
delta_er = (exchange_rate - 44) / 44 * 100 * 2         

# 3. Tổng hợp dòng tiền mô phỏng
simulated_npv = base_npv_epv + delta_yarn + delta_cotton + delta_er
prob_negative = np.sum(simulated_npv < 0) / n_simulations * 100
mean_npv = np.mean(simulated_npv)

print(f"Mean NPV: {mean_npv:.2f}")
print(f"Xác suất rủi ro (NPV < 0): {prob_negative:.2f}%")