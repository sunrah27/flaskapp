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
- [x] Build Homepage `index.html`
- [x] Build Products page `products.html`
- [x] Build Products Details page `product-details.html?sku=xxxxx`
- [x] Build Cart page `cart.html`
- [x] Build Login page `login.html`
- [x] Build Contact page `contact.html`
- [x] Refactor Products page to populate from productDB
- [x] Refactor Product Details page to populate using sku passed va URI
- [x] Refactor Homepage to pull product data from producDB
- [x] Refactor Related Products on Product Details page based on Type
- [x] Code Cart functionality
- [x] Code User login functionality
- [x] Code filter feature in the Products Page
- [x] Code sort feature
- [x] Replace browser alerts with pop-up notifications
- [x] Added pop-up notification after login
- [x] Added pop-up notification after adding item to shopping basket

## New Features in V2.0
- [x] Updated login and registration to offer full login and registration functionality replacing `userDB.json`
- [x] Login and Registration is done using a `Flask API` and stored in `MySQL Database`
- [x] Add logic to check for session cookie if user has logged in
- [x] Implement Accounts page
- [x] Allow registered users to change personal information
- [ ] Implement Purchase history
- [x] Login API
- [x] Registration API
- [x] Stores JWT as a session cookie for each successful login
- [x] Can Create, Read, Update remote MySQL DB
- [x] Has Custom Errors and loging functionality
- [x] Encrypts password with a randomly generated salt
- [x] MySQL DB stores User, Product, Purchase and Purchase details

## Features for V3.0
- [ ] Build UI to manually update Product Data
- [ ] build reporting functionality
- [ ] Implemente environment variables
- [ ] Discover how to implement CSRF tokens to all forms


## Detailed breakdown of website development

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

### Challanges

- Cookies and why I absolutely hate them
- Forced to migrate website into my FlaskApp
- Protecting API endpoints with JWT
- So many ideas, not a great designer
- Why researching tech teaches how to be a bad writer
- Should I be a developer or write coding tutorials
- AARRGGGHHH Bugs and I don't know how to fix them
- Experiencing Dunning-Kruger effect
- Rise of the Project Manager, must do it properly if the timeline allows

### Building Api

### Horrors of using a framework
