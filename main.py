import datetime
import matplotlib.pyplot as plt

def generate_chart():
    # 1. 模擬/擷取數據
    time_slots = ["09:00", "11:00", "13:00", "15:00", "17:00"]
    data_values = [105, 120, 115, 140, 138]

    # 取得當前更新時間
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. 開始繪製圖表
    plt.figure(figsize=(10, 5))
    plt.plot(time_slots, data_values, marker="o", color="#007acc", linewidth=2.5, label="即時數據")
    
    plt.title(f"Live Data Chart (Updated: {current_time} UTC)", fontsize=13)
    plt.xlabel("Time", fontsize=11)
    plt.ylabel("Value", fontsize=11)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    # 3. 儲存圖表為 chart.png
    output_filename = "chart.png"
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close()
    
    print(f"✅ 成功產出圖表：{output_filename}，更新時間：{current_time}")

if __name__ == "__main__":
    generate_chart()
