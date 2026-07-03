import network
import socket
import time
from machine import Pin

# 1. 硬件配置：設定 ESP32-S3 的 LED 腳位
# 提示：如果您的 S3 開發板沒亮，請試著將 47 改為 21 或 2
led = Pin(47, Pin.OUT)
led.value(0) # 預設關燈

# 2. 網路配置
SSID = "您的WiFi名稱"
PASSWORD = "您的WiFi密碼"

# 🌟 關鍵：填寫您 Ubuntu 主機的區網實體 IP
NATS_SERVER = "192.168.1.100" 
NATS_PORT = 4222

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("正在連線至 Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
            print(".", end="")
    print("\n✅ Wi-Fi 連線成功！ESP32-S3 IP:", wlan.ifconfig()[0])

def listen_nats():
    connect_wifi()
    
    print(f"正在與 NATS 建立長連線 -> {NATS_SERVER}:{NATS_PORT}")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((NATS_SERVER, NATS_PORT))
    except Exception as e:
        print("❌ 連線失敗，請檢查 Ubuntu IP、Docker 或防火牆！", e)
        return

    # 讀取 NATS 的初始 INFO 握手訊息
    s.readline()

    # 發送 NATS 訂閱協定指令
    s.send(b"CONNECT {}\r\n")
    s.send(b"SUB iot.device.01 sub_id_01\r\n")
    print("📡 成功訂閱 'iot.device.01' 通道，等待開關燈命令...")

    # 進入無窮循環長連線
    while True:
        try:
            line = s.readline()
            if not line:
                print("❌ 連線中斷！")
                break
                
            cmd = line.decode().strip()
            
            # 回應 NATS 伺服器的心跳包，防止被踢下線
            if cmd == "PING":
                s.send(b"PONG\r\n")
                continue
                
            # 解析收到的 PUB 訊息
            if cmd.startswith("MSG"):
                # NATS 協定的下一行才是真正的 Message 內容
                payload = s.readline().decode().strip()
                print(f"📥 [收到指令]: {payload}")
                
                # 🔮 核心硬體控制：解析內容並控制 LED
                if payload == "LED_ON":
                    print("💡 執行指令 -> 開燈")
                    led.value(1) # 給高電位，點亮 LED
                elif payload == "LED_OFF":
                    print("🌑 執行指令 -> 關燈")
                    led.value(0) # 給低電位，熄滅 LED
                else:
                    print("⚠️ 未知的控制指令:", payload)
                    
        except Exception as e:
            print("運作時發生錯誤:", e)
            break

    s.close()
    print("🔄 5 秒後嘗試重新連線...")
    time.sleep(5)
    listen_nats()

# 執行監聽
listen_nats()

