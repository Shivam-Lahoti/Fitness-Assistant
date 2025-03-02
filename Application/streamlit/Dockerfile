FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8502

CMD ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]