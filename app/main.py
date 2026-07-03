from contextlib import asynccontextmanager
from fastapi import FastAPI
import nats

nc = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global nc
    # 啟動時建立與 NATS 的長連線
    nc = await nats.connect("nats://host.docker.internal:4222")
    yield
    # 關機時關閉連線
    if nc:
        await nc.close()

app = FastAPI(title="IoT Control Center", lifespan=lifespan)

# IoT 命令下發 API
@app.post("/control")
async def control_device(command: str, device_id: str = "iot.device.01"):
    global nc
    if not nc or not nc.is_connected:
        return {"status": "error", "message": "NATS 伺服器未連線"}

    # 瞬間將命令透過現成的長連線，發布到特定 IoT 設備的通道
    await nc.publish(device_id, command.encode())
    await nc.flush()

    return {"status": "command_sent", "target_device": device_id, "command": command}


# 測試 API 路由 (保持不變)
@app.get("/")
def root():
    return {
        "message": "Hello World",
        "service": "api-service",
        "status": "ok"
    }

@app.get("/hello")
def hello():
    return {"message": "Hello from Docker API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

