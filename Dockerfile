FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


ENV FLASK_ENV=production

EXPOSE 8080

ENTRYPOINT [ "/app/entrypoint.sh" ]
