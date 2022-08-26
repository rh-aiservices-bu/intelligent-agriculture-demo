FROM registry.access.redhat.com/ubi8/python-38

WORKDIR /opt/app-root/src

RUN pip install pipenv==2022.8.24

COPY Pipfile Pipfile.lock crops_96.31.h5 app.py ./

RUN pipenv install --system

COPY app.py ./

EXPOSE 5000

CMD ["python", "-u", "app.py"]