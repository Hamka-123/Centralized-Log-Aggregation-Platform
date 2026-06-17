FROM python:3.11-slim
WORKDIR /app

# Copy requirements
COPY alerting_worker/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy common library and the specific service source
COPY common/ ./common/
COPY alerting_worker/src/ ./src/

# Set Python path to /app so it can resolve 'common' and 'src' modules
ENV PYTHONPATH=/app

# Use the correct path for the entry point
CMD ["python", "-m", "src.main"]


