FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -y python3.12 python3-setuptools python3-pip python3.12-venv
COPY . /app
WORKDIR /app
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python3", "-m", "src"]