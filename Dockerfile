FROM python:3.11
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "tomato_bot/main.py"]
