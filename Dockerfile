# ============================================================
# Readmission Risk API - Dockerfile (FIXED)
# ============================================================

# 1. 使用一个轻量级的 Python 基础镜像
FROM python:3.11-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. (关键修复) 更新软件源并安装 libgomp1
#    这行命令会安装你的模型所依赖的系统库
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 4. 先复制 requirements.txt (为了更好的缓存)
COPY requirements.txt .

# 5. 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 6. 复制应用程序的其余部分
COPY main.py .
COPY readmission_stack_ensemble_final.pkl .

# 7. 暴露 API 运行的端口
EXPOSE 8000

# 8. 启动 API 服务的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]