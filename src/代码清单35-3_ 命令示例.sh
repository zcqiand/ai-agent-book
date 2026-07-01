# 构建和启动
docker-compose build
docker-compose up -d

# 查看日志
docker-compose logs -f rag-api

# 进入容器
docker exec -it rag-api bash
