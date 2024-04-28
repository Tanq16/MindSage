FROM python:3.12-alpine3.19

WORKDIR /app

COPY . .

RUN pip install requests flask openai youtube_transcript_api

RUN mkdir patterns && \
    for i in $(cat patternlist); do wget "$i" -O "patterns/$(echo $i | cut -d "/" -f8).md"; done

ENV FLASK_APP=server.py

CMD ["flask", "run", "--host=0.0.0.0"]

