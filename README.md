# Python Backend for eCommerce website

A Python project built using Flask framework to act as the backend for my [eCommerce project](https://redstoreapi.onrender.com/) (App is hosted on Render and takes around 50sec to start up if not in use). The App connects to a MySQL DB hosted on Aiven and also acts as the server for the API endpoints the eCommerce project uses for Login, Registration, Purchase Histroy and Product data. App also offers a backend to connect to the MySQL DB and update product data.

## Inspiration

During my Introduction to Web Development Bootcamp I learned a lot about front end web development and wanted to put this knowledge to the test. While brain storming ideas for a project I ultimately settled on an eCommerce website. It had all of the features a typical website may have and to test my knowledge as well as fill any gaps I decided to give it go.

As I progressed in my Bootcamp I started off as an experimenting ways to combine my MySQL and Python knowledge together. I wanted to be able to connect to a MySQL DB. From there I began exploring how to perform CRUD operations on the DB using Python. This then grew into creating the logic for a simple Login and Registration functionality. Eventually becoming a complete platform for an eCommerce website supported using API, Python and MySQL Database.

Flask + Python + MySQL + HTML + CSS + JS = API \o/

# FRONTEND
An ecommerce site with a shopping basket. Products details are retrived from a JSON file named productdb.json.

A basic version of the site built purely using HTML, CSS and JS can be found at at [https://sunrah27.github.io/eCommerce/](https://sunrah27.github.io/eCommerce/)

Link to repo: [https://github.com/sunrah27/eCommerce/](https://github.com/sunrah27/eCommerce/).

## Features
Site has following features completed:
[x] Build Homepage `index.html`
[x] Build Products page `products.html`
[x] Build Products Details page `product-details.html?sku=xxxxx`
[x] Build Cart page `cart.html`
[x] Build Login page `login.html`
[x] Build Contact page `contact.html`
[x] Refactor Products page to populate from productDB
[x] Refactor Product Details page to populate using sku passed va URI
[x] Refactor Homepage to pull product data from producDB
[x] Refactor Related Products on Product Details page based on Type
[x] Code Cart functionality
[x] Code User login functionality
[x] Code filter feature in the Products Page
[x] Code sort feature
[x] Replace browser alerts with pop-up notifications
[x] Added pop-up notification after login
[x] Added pop-up notification after adding item to shopping basket

## Features in V2.0
[x] Updated login and registration to offer full login and registration functionality replacing `userDB.json`
[x] Login and Registration is done using a `Flask API` and stored in `MySQL Database`
[x] Add logic to check for session cookie if user has logged in
[x] Implement Accounts page
[x] Allow registered users to change personal information
[x] Login API
[x] Registration API
[x] Stores JWT as a session cookie for each successful login
[x] Can Create, Read, Update remote MySQL DB
[x] Has Custom Errors and loging functionality
[x] Encrypts password with a randomly generated salt
[x] MySQL DB stores User, Product, Purchase and Purchase details

## Features for V3.0
[ ] Refactor Python and JavaScript code (possibly a complete rewrite)
[ ] Update designa and add logout option
[ ] Add front end input validation and sanitation
[ ] Add backend data validation and sanitation
[ ] Implement Purchase history
[ ] Build UI to manually update Product Data
[ ] build reporting functionality
[ ] Implemente environment variables
[ ] Discover how to implement CSRF tokens to all forms

## Rise of the Project Manager Full Stack developer, must do it the right way, maybe....

### Challenges
------
First challenge from the very get go was design. Designing an entire website from scratch was difficult and it is important I did not include to many extra features else there was a risk I would over load myself. To this end I decided to go with a simple eCommerce website, with 5 pages.

Second challenge came about after building the static version of the website. I had a website that looked nice but didn't do much. If it was a design prototype I would have ended there but I wanted to build an eCommerce website that offered a variety of features incluing a list of products and a shopping cart. It took me couple of weeks thinking of a way to have a local Database of products. Eventually I overcame this when I realised I could just create a JSON file with all of my product information.

### Building static HTML and CSS
------
Creating the static HTML was not too difficult but setting up all of the CSS was a challenge. Once I maanaged to complete the static HYML and CSS I was forced to refactor it completely in order to make sure I can reuse sections of the code. This took multiple attempts and several moments of frustration where a simple change in CSS or the addition of an extra `div` would cause the site to display incorrectly.

Eventually it became an iterative process. After building couple of pages, I would write the CSS `@media queries` then after building a new page I'd go back to the previous pages and try to consolidate the changes by trying reuse classes.

Howevere, my site only had one product and a lot of non-fuctional links. I was staring at the daunting task of building static pages for every product which I was not very keen and pushed it aside as a last resort. Fortunately I would come across an idea how to over come this issue using JavaScript later.

### Creating JSON files for Products
------
Before I could even touch JavaScript I had to build my `peoductsDB.json` file. Based on my designs I managed to outline few informatin I required for every product.

But I would ultimately modify the productsDB and remove the two Product Name and settle on one. I also needed to include a data/time with every product as my Homepage had a latest product module. I debated weather to hard code the rating stars but ultimate decided to incluide it as part of the DB. One odd issue I came across later was tha Product Description. i was unable to include any bullet points, this forced me to spllit it into three differnt properties. Product Description, Product List and Product Materials. A surprise outcome of the DB was the easy way to manage the product images. Renaming all of the prduct images with Product SKU made it significantly easier to fetch via JS.

### Adding JavaScript
------

#### Building Products Page
Ah, the land of mangic. I decided to populate the Products Page with the products in the `productsDB.json`. This was not a complicated task as all I had to do was fetch the data form the JSON file, store it in an object and then reference the information I need. I found myself consolidating a lot of my HTML code and creating simple templates which I can repeat and generate HTML to display all of the products. 

#### Building Product Details Page
Once done I realised I could over come another issue I was having. What if I passed the product SKU via URL to the Product Details Page and then read the SKU in the URL to display the relevant product information. This will mean I only need one Product Details Page and I can also use the product SKU on the Products Page as part of the anchor link.

I needed to figure out how to pass information via URL and also how to extract this information. After some research I wrote the following fuction:

```javascript
// Function to read SKU from URL
function getSKUFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('sku');
}
```
With this I was now able to search the productDB and display the relevant information. Next step build the Related Products module.

#### Related Products Module
This module proved more difficult then I had first intended. I was able to display all products related to the product displayed on the module but I was also displaying the existing product. After a lot of time tinkering with JS and pulling my hair out I realised all I needed to do was add `!== currentSku` when declaring the relatedProducts object.

```javascript
// Filter products based on the pType of the current product
const relatedProducts = productData.filter(product => product.pType === currentProduct.pType && product.pSku !== currentSku);
```

#### Latest Products Module
Building the Latest Product Module was pretty straight forward after Related Products Module. However, I started noticing a lot of console errors appearing. I noticed I had JavaScript code which should run only on specific pages. Thus began the first of many JavaScript refactoring and breaking my site.

#### Building the Shopping Cart
Building the Shopping Cart was pretty simple. I knew from the start I am going to use the browsers local storage. The main issue I began to have was the EventListner not attaching to the button on the Product Details page. After a lot of debugging I discovered the issue was due to the Button HTML being generated using JS in the Products Details page. To resolve this issue I was finally forced to clean up my JavaScript and break my code in to smaller functions. Adding Async and Wait to functions to ensure JS codes only ran after the pages were loaded. I also took time to refactor my code and reduce duplication. One major change was storing the `productDB.json` to a single object called `productData` reducing multiple function calls. I also removed as much code outside of the `document.addEventListener('DOMContentLoaded', async function () { }` as possible. This helped me finally resolve the issue with being able to add an item to the Shopping Cart.

#### Presistent Login and Contact Us
I had originally planned to have a login page which would display the user profile but I decided to skip on the user profile and just create a login feature. The `user`information was stored in a `user.json` file and when the user logs in a key is saved to the browsers local storage. I wrote a new function to run on every page to check if the user is logged in. I also changed the Login link in the main nav to display a greeting message to the `user` after login. Also only when the user is logged in can they access the Shopping Cart page.

#### Filters and Sorts
The final feature left to code was the product filters and the product sort which were part of the design for the Products page. This required a complete rewrite of the JS function poulating the Products Page along with several additional functions had to be created:

- `function populateProductsPage(productData, filterType = 'all', sortType = 'default')`
⋅⋅⋅ Function updated to take filter and sorty arguments

- `function generateProductHTML(product)`
⋅⋅⋅ Function only used to generte HTML code for the products page

- `function populateFilterByTypeDropdown(productData)`
⋅⋅⋅ Function to populate the Filter dropdown using all of the different product types

- `function setupFilterAndSortEventListeners(productData)`
⋅⋅⋅ Function to add Event Listenrs

- `function sortProducts(products, sortType)`
⋅⋅⋅ Function to sort products based on default, price (high and low) and ratings

# BACKEND

Python Backend built initially to serve as an intermediary between the eCommerece website and the MySQL Database using API's. With the implementation of JWT and HTTPOnly Cookie I decided to combine the frontend and backend together. The data from the DB is still access using API while still benefitting from having a secure session cookie being set on the user's browser.

Link to repo: [https://github.com/sunrah27/flaskapp](https://github.com/sunrah27/flaskapp).

### Snaking through with Python

#### Databases are not all that scary
I just came off learning MySQL and was eager to try and combine both MySQL and Python knowledge. While I know how to conduct CRUD operations I realised I had to be careful what I was trying to do through Python. I started off with creating a DB that would handle user registration and login and immediatly realised even if I was to implement input validations in the front end, all data needs to be sanitised and checked before being comitted to the Database. A future task I wish to persue is look at Python and JavaScript libries that handle data validation and data sanitation.

#### Building API's
The original purpose of this project was for me to learn how to write my own API. I had the false impression that API's were very difficult and required considerable knowledge. My stance of not using any frameworks was because I wanted to understand and become familiar with python and how to construct and debug my own code. However, my Bootcamp course was just an introduction to Python and to build API's from scratch required intimiate knowledge and familiarity across multiple technologies which I do not have at the moment. I ultimately decided to settle on using Flask framework. I spent a lot of time experimenting with Flask before becoming comfortable with creating API enpoints.

To write an API endpoint simply requires:
```python
@app.route(/api/endpoint)
def myApiEndpoint
```
#### Protecting API endpoints with JWT
Once I managed to confidently connect to my database and communicate using API's I built a user registration and login functionality. I looked into different methods and eventually learned of using JWT Tokens to validate successful logins. This taught me how to start protecting endpoints by adding `@JWT_required()` decorator. Now calls to any protected endpoints prevents information from being leaked from the database. Furthermore I learned about the difference between response/request headers vs payload. Sadly this only came about after countless hours of research.

#### Cookies and why I absolutely hate them
Cookies are everywhere and it's extremely common to come across cookies. However, how to create and make use of a cookie is difficult to understand. There are far to many documentations for various uses making it extremely challanging. Every attempt to learn about cookies and login systems led to a different implementation that are pooly explained. One major issue I had was after setting the JWT token as a HttpOnly cookie I could not figure out why the cookie was not being used to validate the user being logged in. Countless hours or research and experimentation led me to discover two issues not fully explained. `@JWT_required` only accesped a JWT token if the cookie was labelled `access_token_cookie`. All documentations pointed to the cookie name being `access_token` including various code examples on StackOverflow and even ChatGPT. Secondly when calling a protected API HttpOnly cookies were not accessible to JavaScript and are only sent as a request headers if and only if I included the line `credentials: 'include'`. These issues were further compounded by lack of coherent documentations, clean examples and poor debug errors in VSCode terminal. Unfortunately my misgivings with cookies did not end there. I then had to learn the hard way how cookies do not work as intended in a development environment. I eventually had a face first crash with Cross-origin resource sharing (CORS) and CSRF. Unfortunately I never fully understood how to overcome these two issues and as a result I was forced to implement less secure workarounds.

#### Forced to migrate website into my FlaskApp
To overcome CORS requirements I was ultimately forced to combine my Frontend and Backend into one. Originally I had planned to keep both separate and use API's to handle comunication between the two. Sadly maintaining this stance prevented me from implementing a working Login/Registration system as well are being able to validate user logins when accessing protected endpoints. One weekend of constant investigation as to what was wrong, why the issue was occuring and then trying out numerous different approaches I moved the eCommerce website inside the FlaskApp. This however came with it's own challenges. This is my first Flask application and I only decided to go with this framework due to alternative of creating API endpoints from scratch. Now however, I had to learn how to render HTML files within Python. It dind't take long to realise that there was something wrong. Python constantly reported errors unable find the HTML file for the root directory. Frustration began building up and I was starting to feel like giving up. Ultimately I decided to scratch the entire project and jsut start from scratch. Create a new python project, setup a new virtual environment, only install libraries when I use them. I returned to the absolute basic and started building the app piece by piece. I finally learned one frustrating and one annoying truths about Python. Python will not render a HTML page if there is an error. Up until now this was never an issue as the HTML file would always be displayed on a browser regardless of any code issues. So I was forced to correct any errors that came about from using render_tempaltes. Secondly part of best practise in creating my own API endpoints was for me to use user blueprints. This meant the templates and static folders which should contain my html and css + js files respectively had to be inside the blueprint folder. A piece of information that was missed out on mutliple examples and even ChatGPT did not know. Fixing all of the file links, moving the folders to the relevant directory eventually led to me finally discovring how to migrate static pure HTML, CSS and JS to Python and then render each HTML file. 

#### So many ideas, not a great designer
I was finally set. My website was working again. I was able to login and register new users correctly. I am now ready to add more features to my site. I decided to include a requirement I had dropped at a very early stage of the eCommerce website project. I would finally be able to build an Accounts page. However, I never created a design for the page and now I was staring at the daunting task of coming up with a design for the accounts page. Even reusing existing layouts was fine but I was struggling to pick a direction. Having struggled with the design I decided to instead just focus on implementing the login for the Accounts page. Users will be able to see their account information and also provide additional information such as addresses. I experimented on Figma but found myself making the design overly complicated or diviating too far from the existing design Fortunately I was able to reportpose the contact_us page designs. I want to add aditional features but each new feature needs a front end design. This will also include changing the CSS. Coding is one things but creating something out of nothing is not one of my greatest strengths.

#### Why researching tech teaches how to be a bad writer
In my journey to create create a website that communicates with a databse using API I was forced to read a lot, A LOT of terribly written, encrypted and possible alien documentations. Researching one issue if lucky led to a single result, however there was little wisdom to gain as the documentations failed to detail additional requirements and use cases or worse limitations and the proper workarounds. I discovered an issue where one specific protected endpoint constantly failed even though I am still able to login, register, have a persistent login etc... Sadly the only information I had going was a 401 error on the brwoser console and VSCodes terminal. I searched and searched, made sure `--debug` was always added when running my flask app. Began implementing logs for every possible path and potential errors I could presive. None of that prepared me for the dreaded 401 error. 3 days of insanity later I made the most insignificant progress. The issue one comes up when the POST method is used for a protected endpoint. Why? No one knows. Logs? Only a 401. Debug terminal? Only that the request was refused. Why? Why did this happen? What is going on? Sadly I can't tell you. No amount of research allowed me to trace the issue back and get an insight into what could be the issue. More frustration, rewritting code, creating new endpoints and a lot of time wasted did I finally learn of an additional requirements. When making a POST request to an API protected by @JWT_required you had to supply a CSRF token. What is a CSRF token? What does it do? How does it work? how do I get one? I wish I could say I was able to read the JWT documentation and learned about CSRF token requirement and then was directed to understanding what to do next...

Well no. Not a chance. Coders are terrible writers. Their documentations generally lack much use to anyone unless the user is already a skilled developer. For some reason the documentations if lucky will have a single code example. Generally documentations will list all of the arguments that can be passed or methods available. Yet explanations for any lacks any substance. CSRF was one such issue. I kept coming across JS code examples of how to include csrf tokens to APi requests but failed to explain CARF tokens should be auto generated and included as a hidden feilds on forms. Or how CSRF tokens are accompanied with a CSRF HTTPOnly session cookie. Sadly this was a challenge for me on the most fundemental level and I am discouraged to learn the cause of all these confusion is the dev community for it's collective faliure to offer proper documentations. Ultimatley I opted to not protect my POST API endpoints as I found it impossible to understand how to implement CSRF tokens and validate said tokens.

#### Should I be a developer or write coding tutorials
Feeling disheartened with alot of the hurdles and the impossible feeling of not having an idea how to proceed I begane reviewing my own understanding of Python. Did I learn it correctly, should I have these issues, maybe I am forgetting something. Soon I found myself retracing my steps and going over the basics. Trying to explain to invisible friend how and why certain codes do stuff. Soon enough I found myself writting python codes to demonstrate manipulating strings, lists, dictionaries. I think I learned some python but there is much much more I need to learn before I can feel confident in my own ability. To claim I understnad something is to be able to teach it to another person and sadly I do not feel like I can do any of that yet.

#### AARRGGGHHH Bugs and I don't know how to fix them
I soon find myself dealing with more bugs. I have removed the productDB.json file and moved all product information into the MySQL DB. Amazing...except no. The data types have now copletely changed. What I once did in JavaScript had to now be done in Python and then the JS code had to be updated to reflect this. But now another JS function is no longer working because the information that is received from the database is not in the same format anymore. I found myself coding in both Python and JavaScript fixing logic and data type issues. My Python code file has grown considerably even after splitting up my code into different files. My script.js file is now well over 1000 line of codes. I am getting the sinking feeling there is a better way to do this... but how?

#### Experiencing Dunning-Kruger effect
I am now convinced I should learn about Python and JavaScript classes. Create new mini projects that will allow me to flush out concepts in greater details allowing me top experiment further. MySQL also offers views, stored procedures and functions. I always believe computers should make human lives easier so there surely must be an easier to do everything. This project of mine started off as creating an eCommerce website with a working checkout basket. It got expanded to retrive information from a MySQL DB using custom API's. With the knowledge I have now I would likely stop and explore other ways of creating the individual requirements and a completely different apprach to building every component up independantly.