FROM python:3.9
COPY . .
RUN pip3 install -r requirements.txt
CMD [ "python", "app.py" ]
EXPOSE 9999