FROM python:3.11
RUN pip install -r requirements.txt
COPY . /app
CMD ["python", "tomato_bot/main.py"]