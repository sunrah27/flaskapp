# BACKEND

Python Backend built initially to serve as an intermediary between the eCommerece website and the MySQL Database using API's. With the implementation of JWT and HTTPOnly Cookie I decided to combine the frontend and backend together. The data from the DB is still access using API while still benefitting from having a secure session cookie being set on the user's browser.

Link to repo: [https://github.com/sunrah27/flaskapp](https://github.com/sunrah27/flaskapp).

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

### Challanges

### Building Api

### Horrors of using a framework