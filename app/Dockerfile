FROM python:3.12.5

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

EXPOSE 8000

WORKDIR /django

RUN pip3 install numpy cloudpickle scikit-learn imblearn seaborn pandas cripsy-bootstrap5 django-cors-headers gunicorn xgboost lightgbm

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ECEC.wsgi:application"]
