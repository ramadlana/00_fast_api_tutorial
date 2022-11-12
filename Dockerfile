# docker build -t my_app:1.0.0 . 
# 
FROM python:3.11

# 
WORKDIR /app

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt

# 
COPY . .

EXPOSE 80

# 
CMD ["python3","server.py"]
