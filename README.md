# Leaving Well: Improving Support For Young People Leaving Care
![testing](https://github.com/SocialFinanceDigitalLabs/lw-ng/actions/workflows/tests.yml/badge.svg)
![linting](https://github.com/SocialFinanceDigitalLabs/lw-ng/actions/workflows/linting.yml/badge.svg)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Leaving Well is a framework to improve support for young people leaving the care system.

Care leavers face a lot of challenges when they move from care to independence. 
Young people leaving care often move to live by themselves earlier than most people. 
Some have a lot to deal with due to difficult life experiences and a lack of support from their local authority. 
This contributes to the poor outcomes that many care leavers experience in adulthood. 

## Why we are doing this:

* Young people leaving care experience worse outcomes than their peers.

* The data collected on these young people is currently very limited. 
This means that it is difficult to understand the causes of these outcomes and how to improve them.

* Our research showed the potential for a digital tool to improve the experiences of young people leaving care.

## What we are doing:

We have developed a digital tool which aims to improve the support that young people receive. We worked with personal advisers (case workers for young people leaving care) and young people to develop every feature in the tool. The tool:

1. Gives young people a platform to express their voice and ambitions

2. Enables personal advisers to spend more time with young people. The tool makes admin tasks quicker and easier to complete.

3. Provides managers with information on their services. This can be used to identify areas which should be improved.

The tool will continue to be developed based on user feedback.

For more information email contact.leavingwell@socialfinance.org.uk.

## Partners

Bradford City Council

Coventry City Council

Doncaster City Council

Esmee Fairbairn

Garfield Weston Foundation

Leeds City Council

Southampton City Council

Southampton City Council

The London Borough of Havering

## Local Setup

This is a tool built with python and Django. You need to have [python](https://www.python.org/), [poetry](https://python-poetry.org/) and [npm](https://www.npmjs.com/) installed in your machine. 

1. create an `.env` file, with environment variables, like it's in `.env.example`;
2. Install dependencies with `poetry install`;
3. Launch a poetry shell so the dependencies are active: `poetry shell`;
4. Run `python manage.py migrate` to create the databases tables;
5. This version uses  [python-webpack-boilerplate](https://github.com/AccordBox/python-webpack-boilerplate) 
so we can use webpack for styling and packing javascript. Make sure you install the necessary dependencies:
   * `cd frontend` - change to frontend directory;
   * `npm install` - install the dependecies; 
   *  `npm run build` - creates a build directory with a production build of the files;
   *  To work more on the frontend, see instructions in the [frontend](./frontend/README.md) directory.
5. Go back to the main directory (`cd ..`) and run `python manage.py runserver 8000` to access the portal site.


## Docker Setup
If you have docker setup on your computer, you can run the following steps to get a local copy running:
   * `docker-compose build` - Build the images using the Dockerfile provided in this repo.
   * `docker-compose up` - Will spin up a copy of LW-NG along with a postgres database (at http://127.0.0.1:8000) as long as that address isn't taken by another service.