# Project 3: Pizza

CS50 Web programming with javascript and python

## Info

[![Coverage Status](https://coveralls.io/repos/github/ggibelli/pinocchio-pizza/badge.svg?branch=master)](https://coveralls.io/github/ggibelli/pinocchio-pizza?branch=master)

In this project, you’ll build a web application for handling a pizza restaurant’s online orders. 
Users will be able to browse the restaurant’s menu, add items to their cart, and submit their orders. 
Meanwhile, the restaurant owners will be able to add and update menu items, and view orders that have been placed.

For this project I used python 3.8 and django 3.0, for the front-end I used vanilla JS and bootstrap.
The app runs in a docker container and has 96% test coverage, I use travis to continuous test and deploy on Heroku.


## Files info

This django project has three apps, pages that handles the static pages, users that handles the signup and login part and orders that manages the menu and ordering part.

There is also a folder for the static assets, images, js and css and one for all the templates.

Since I used docker and pipenv there is no requirements.txt but the Pipfile and Pipfile.lock instead. 
There are also a Dockerfile and a docker-compose.yml for the docker container, a heroku.yml for the deployment and the .travis.yml for the CI/CD.

## Personal touch
I choosed to add the following personal thouches:
- The users can see their order status
- The users can pay through Stripe
- The restaurant managers can set the orders state as 'Complete'
- After the successfull payment and after the order becomes complete an e-mail is sent to the customer.

## License
[MIT](https://choosealicense.com/licenses/mit/)