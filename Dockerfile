FROM python:3.10

WORKDIR /app
COPY . /app
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx

RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 12345

CMD [ "python", "NNPredictTcpSocket.py"]
#CMD [ "python", "NNPredictTcpSocket.py" ]