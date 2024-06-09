# BetWhiz
### NLP based application for bet prediction.


BetWhis is an application whose purpose is to predict match results based
on related tweets. Automated scraper collects data related to
games and stores them into database using created REST API.
The data is used to train the NLP model. Model predictions can
be utilized by querying the appropriate API endpoint.

## Feautures

- Creating and managing teams, games, and tweet records stored in a PostgreSQL database through a REST API.
- A simple GUI allowing users to test model predictions.
- A CNN-LSTM architecture NLP model responsible for predictions.
- A scraper ready to collect game-related tweets.
- A Jupyter Notebook that allows for adjusting model parameters.



## Technologies used


| Python | Django | Django REST Framework | NumPy | PyTorch | Pandas | Scikit-Learn | NLTK |
|--------|--------|-----------------|-------|---------|--------|--------------|------|
| ![Python](https://www.python.org/static/community_logos/python-logo.png) | ![Django](https://static.djangoproject.com/img/logos/django-logo-positive.png) | ![Django REST Framework](https://www.django-rest-framework.org/img/logo.png) | ![NumPy](https://numpy.org/images/logo.svg) | ![PyTorch](https://pytorch.org/assets/images/pytorch-logo.png) | ![Pandas](https://pandas.pydata.org/static/img/pandas_secondary.svg) | ![Scikit-Learn](https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png) | ![NLTK](https://miro.medium.com/v2/resize:fit:592/1*YM2HXc7f4v02pZBEO8h-qw.png) |

## Installation

Configure .env file first.
```sh
pip install -r requirements.txt
cd api && python manage.py runserver
```


