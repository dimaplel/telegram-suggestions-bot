FROM python:3.10-alpine
WORKDIR /usr/app/
COPY requirements.txt ./requirements.txt
RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache && \
    apk --purge del .build-deps

COPY . .
ENV PYTHONPATH ./
CMD ["python", "bot.py"]