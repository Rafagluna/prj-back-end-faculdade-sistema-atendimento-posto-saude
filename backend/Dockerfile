FROM python:3.10-slim

WORKDIR /app

# Copia primeiro apenas o requirements.txt para aproveitar o cache de
# camadas do Docker: as dependências só são reinstaladas se este arquivo mudar.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
