FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y libgl1

COPY . .

RUN echo '#!/bin/sh' > /app/start.sh && \
    echo 'python jsoneditor.py --no-show' >> /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
