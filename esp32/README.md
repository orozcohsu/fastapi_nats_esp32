執行 fastapi 建立 pub 訊息
 curl -X POST "http://localhost:8000/control?command=TURN_ON_ALARM&device_id=iot.device.01" 

執行 nats-tool 訂閱 sub 訊息
 docker exec -it nats-tool nats sub "iot.device.01"
