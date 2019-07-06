FROM pypy:2
WORKDIR /usr/src/app
COPY pydes.py .
CMD [ "pypy", "./pydes.py" ]