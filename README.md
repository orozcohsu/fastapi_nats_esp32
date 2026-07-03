細節: https://kjpehdpd4vul.jp.larksuite.com/wiki/Dm2PwzcBBi5LG2kGjIgjhK0opsd
docker: 
CONTAINER ID   IMAGE                    COMMAND                  CREATED        STATUS        PORTS                                                                                      NAMES
639f5cad1ecb   api-server               "uvicorn app.main:ap…"   5 hours ago    Up 5 hours    0.0.0.0:8000->8000/tcp, [::]:8000->8000/tcp                                                api-service
8d8856678d55   natsio/nats-box:latest   "/bin/sh"                28 hours ago   Up 28 hours                                                                                              nats-tool
592cce958ac6   nats:latest              "/nats-server -m 8222"   28 hours ago   Up 28 hours   0.0.0.0:4222->4222/tcp, [::]:4222->4222/tcp, 0.0.0.0:8222->8222/tcp, [::]:8222->8222/tcp   nats
