FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY connection.py .
COPY dashboard.py .
RUN mkdir ~/.streamlit
COPY .streamlit/config.toml ~/.streamlit/config.toml

EXPOSE 8501


CMD ["streamlit", "run", "dashboard.py", "--server.port=8501"]