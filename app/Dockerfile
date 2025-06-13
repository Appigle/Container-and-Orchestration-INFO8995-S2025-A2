FROM python:3.11-slim

# Create a non-root user
RUN useradd -m flaskuser

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set permissions for logs directory
RUN mkdir -p logs && chown -R flaskuser:flaskuser logs

USER flaskuser

EXPOSE 5000

CMD ["python", "main.py"] 