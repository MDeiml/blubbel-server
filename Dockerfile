FROM python:3

COPY src/*.py /src/

EXPOSE 8000

CMD ["python", "/src/app.py"]
