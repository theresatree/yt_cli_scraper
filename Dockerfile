FROM python:3.11-slim

# install required packages
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# default run command
CMD ["python", "main.py"]
