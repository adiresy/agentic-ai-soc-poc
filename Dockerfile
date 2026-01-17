FROM python:3.10-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY scripts/ scripts/
COPY gui/ gui/
COPY data/ data/
COPY docs/ docs/
COPY governance/ governance/

EXPOSE 8501

CMD ["streamlit", "run", "gui/dashboard.py"]

