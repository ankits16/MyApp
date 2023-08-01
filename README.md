# MyApp
Super App

**Docker**

To run this app in docker:
  1) docker-compose build
  2) docker-compose run -p 4000:4000 -p 8000:8000 --rm web sh -c 'RUN_IN_DOCKER=True python manage.py runserver --noreload --nothreading 0.0.0.0:8000'

  If RUN_IN_DOCKER=False ptvsd will not be attached , so if you want to debug it while running in docker you can use RUN_IN_DOCKER=False
