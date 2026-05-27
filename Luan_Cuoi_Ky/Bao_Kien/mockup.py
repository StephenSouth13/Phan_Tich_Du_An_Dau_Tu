import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Thiết lập tham số môi trường
np.random.seed(42)
n_simulations = 10000
base_npv = 76.13 

# 1. Gán phân phối rủi ro
exchange_rate = np.random.normal(44, 2, n_simulations)
yarn_price = np.random.triangular(1.3, 1.5, 1.8, n_simulations)
cotton_price = np.random.normal(1.0, 0.1, n_simulations)

# 2. Tổng hợp dòng tiền mô phỏng
dy = (yarn_price - 1.5) / 1.5 * 100 * 5       
dc = (cotton_price - 1.0) / 1.0 * 100 * (-3) 
de = (exchange_rate - 44) / 44 * 100 * 2         
simulated_npv = base_npv + dy + dc + de

# 3. RENDER 2 ẢNH CẦN THIẾT
# Ảnh 1: Histogram (Phân phối xác suất)
plt.figure(figsize=(10, 6))
sns.histplot(simulated_npv, bins=60, kde=True, color='#0ea5e9')
plt.axvline(x=0, color='#ef4444', linestyle='--')
plt.title('PHÂN PHỐI XÁC SUẤT NPV - PHƯƠNG ÁN 5', fontsize=14, fontweight='bold')
plt.savefig('Slide_5_Histogram.png', dpi=300)
plt.close()

# Ảnh 2: Tornado Chart
def calc_npv(y, c, e):
    return base_npv + ((y - 1.5)/1.5*500) + ((c - 1.0)/1.0*-300) + ((e - 44)/44*200)

sens = [('Giá Sợi', calc_npv(1.3,1,44), calc_npv(1.8,1,44)), ('Giá Bông', calc_npv(1.5,0.9,44), calc_npv(1.5,1.1,44)), ('Tỷ Giá', calc_npv(1.5,1,42), calc_npv(1.5,1,46))]
fig, ax = plt.subplots(figsize=(8, 4))
for i, (name, min_v, max_v) in enumerate(sens):
    ax.barh(i, min_v - base_npv, left=base_npv, color='#ef4444')
    ax.barh(i, max_v - base_npv, left=base_npv, color='#10b981')
ax.set_yticks(range(3), [s[0] for s in sens])
plt.axvline(base_npv, color='black')
plt.savefig('Slide_6_Tornado.png', dpi=300)

print("Đã tạo xong 2 ảnh: Slide_5_Histogram.png và Slide_6_Tornado.png")