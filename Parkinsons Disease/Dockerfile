FROM python:3.9
WORKDIR /user/src/app
COPY . /user/src/app
RUN apt-get update && \
    apt-get install -y python3 python3-pip

COPY requiremnts.txt ./
RUN pip install flask
RUN pip install -r requiremnts.txt
# Add Python3 to the PATH
ENV PATH="${PATH}:/usr/local/bin/python3"
EXPOSE 3000
ENV FLASK_APP=app.py
CMD ["python", "app.py"]