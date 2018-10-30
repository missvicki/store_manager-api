## Store Manager 

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
    * can modify a single product

* Attendant:
    * can create a sale order of a product
    * can get all products 
    * can get a specific product
    * can create a product


## Heroku Endpoints

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| GET | [/api/v1/products](https://store-manager-api-.herokuapp.com/api/v1/products) | Fetches all products|
| GET | [/api/v1/products/product_id](https://store-manager-api-.herokuapp.com/api/v1/products/1) | Fetches a single product |
| GET | [/api/v1/sales](https://store-manager-api-.herokuapp.com/api/v1/sales) | Fetches all sales |
| DELETE | [/api/v1/products/product_id](https://store-manager-api-.herokuapp.com/api/v1/products/1) | Deletes a single
 product |
| PUT | [/api/v1/products/product_id](https://store-manager-api-.herokuapp.com/api/v1/products/1) | Modifies a single product |
| POST | [/api/v1/products](https://store-manager-api-.herokuapp.com/api/v1/products) | Creates a product |
| POST | [/api/v1/sales](https://store-manager-api-.herokuapp.com/api/v1/sales) | Creates a sales order |


Note: Posting and deleting still needs revision-

## Testing the app

`$nosetests --with-cov --cov  tests/`
  
##Language

**Python**: 3.6.5

## Run the app

`$ python run.py`

## Authors

* **Victor Nomwesigwa**

## Acknowledgments

* Thank you to Andela for the opportunity of giving me this challenge
* My fellow Andela bootcampers, thank you for the help rendered to me when I was stranded





