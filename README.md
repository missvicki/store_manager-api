## Store Manager       [![Build Status](https://travis-ci.org/missvicki/store_manager-api.svg?branch=heroku)](https://travis-ci.org/missvicki/store_manager-api) [![Maintainability](https://api.codeclimate.com/v1/badges/a68f287f8f7b9bf13c07/maintainability)](https://codeclimate.com/github/missvicki/store_manager-api/maintainability) [![codecov](https://codecov.io/gh/missvicki/store_manager-api/branch/heroku/graph/badge.svg)](https://codecov.io/gh/missvicki/store_manager-api) [![Coverage Status](https://coveralls.io/repos/github/missvicki/store_manager-api/badge.svg?branch=heroku)](https://coveralls.io/github/missvicki/store_manager-api?branch=heroku)

Store Manager is a web application that helps store owners manage sales and product inventory records. This application is meant for use in a single store.    

## Getting Started

For installation of this project:  `$ git clone 'https://github.com/missvicki/store_manager-api.git`

## Prerequisites

* Create a Virtual Environment e.g.: `$ virtualenv storemanager`
* Activate the environment: 
    * For Windows: `$c:/ .\storemanager\Scripts\activate`
    * For Linux and Mac: `$ source storemanager/bin/activate`
* Install project dependencies e.g. flask: `$ pip install -r requirements.txt`

## Features

* Admin: 
    * can create and delete a product
    * can get all products 
    * can get a specific product
    * can get all sale orders

* Attendant:
    * can create a sale order of a product
    * can get all products 
    * can get a specific product
    * can create a product


## Heroku Endpoints

|Endpoint|Link|
|:---:|:---|
|Index|[/](https://store-manager-api-.herokuapp.com/)|
|`Products`*GET*|[/api/v1/products](https://store-manager-api-.herokuapp.com/api/v1/products)|
|`Products`*GET* Product|[/api/v1/products/product_id](https://store-manager-api-.herokuapp.com/api/v1/products/1)|
|`Products`*POST*|[/api/v1/products](https://store-manager-api-.herokuapp.com/api/v1/products)|
|`Products`*DELETE* Product|[/api/v1/products/product_id](https://store-manager-api-.herokuapp.com/api/v1/products/1)|
|`Sales` *GET*|[/api/v1/sales](https://store-manager-api-.herokuapp.com/api/v1/sales)|
|`Sales` *POST*|[/api/v1/sales](https://store-manager-api-.herokuapp.com/api/v1/sales)|


Note: Posting and deleting still needs revision-

## Testing the app

  `$nosetests --with-cov --cov  tests/`
  

## Run the app

`$ python run.py`

## Authors

* **Victor Nomwesigwa**

## Acknowledgments

* Thank you to Andela for the opportunity of giving me this challenge
* My fellow Andela bootcampers, thank you for the help rendered to me when I was stranded





