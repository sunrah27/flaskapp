# FlaskApp

A Python project built using Flask framework to act as the backend for my [eCommerce project](https://github.com/sunrah27/eCommerce). The App connects to a MySQL DB hosted on Aiven and also acts as the server for the API endpoints the eCommerce project uses for Login, Registration, Purchase Histroy and Product data. App also offers a backend to connect to the MySQL DB and update product data.

## Features
The app has the following features
- [x] Login API
- [x] Registration API
- [x] Stores JWT as a session cookie for each successful login
- [x] Can Create, Read, Update remote MySQL DB
- [x] Has Custom Errors and loging functionality
- [x] Encrypts password with a randomly generated salt
- [x] MySQL DB stores User, Product, Purchase and Purchase details
- [ ] Build UI to manually update Product Data
- [ ] build reporting functionality
- [ ] Implemente environment variables

## Inspiration

The project started off as an experiment to try and combine my MySQL and Python knowledge together. I wanted to be able to connect to a MySQL DB I created myself. From there I began exploring how to perform CRUD operations on the DB using Python. This then grew into creating the logic for a simple Login and Registration functionality. However, I wanted to keep frontend and backend separate and began exploring creation of API's. This led me to use Flask Framework

Flask + Python + MySQL + HTML + CSS + JS = API \o/