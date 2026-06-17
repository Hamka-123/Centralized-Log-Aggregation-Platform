FROM python:3.11-slim
WORKDIR /app

# Copy requirements
COPY api_collector/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy common library and the specific service source
COPY common/ ./common/
COPY api_collector/src/ ./src/

# Set Python path to /app so it can resolve 'common' and 'src' modules
ENV PYTHONPATH=/app
EXPOSE 8000

# Use the correct path for the entry point
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]