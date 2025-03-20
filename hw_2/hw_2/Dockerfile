FROM python:3.10-slim

# зависимости для LaTeX
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# запуск скрипта
CMD ["python", "generate_pdf.py"]