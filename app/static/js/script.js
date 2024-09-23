document.addEventListener('DOMContentLoaded', async function () {
    const productData = await getAllProducts('/api/v1/allproducts');

    // Display mobile menu
    const menuItems = document.getElementById('menuItems');
    const menuIcon = document.getElementById('menuIcon');
    menuItems.style.maxHeight = '0px';
    menuIcon.addEventListener('click', () => {
        menuItems.style.maxHeight = menuItems.style.maxHeight === '0px' ? '200px' : '0px';
    });

    // Check if the current page is index.html
    const isHomePage = window.location.pathname.endsWith('/index.html') || window.location.pathname === '/eCommerce/';
    if (isHomePage) {
        populateLatestProducts(productData);
    }

    // Check if the current page is products.html
    const isProductsPage = window.location.pathname.includes('products.html');
    if (isProductsPage) {
        populateFilterByTypeDropdown(productData);
        setupFilterAndSortEventListeners(productData);
        populateProductsPage(productData);
    }

    // Check if the current page is product-details.html
    const isProductDetailsPage = window.location.pathname.includes('product-details.html');
    if (isProductDetailsPage) {
        const sku = getURLParameter('sku');
        fetchProductDetails(sku);
        fetchRelatedProducts(sku, productData);
    }

    // Check if the current page is cart.html
    const isCartPage = window.location.pathname.includes('cart.html');
    if (isCartPage) {
        displayCartItems(productData);
        addCartEventListners();
    }

    // Check if the current page is login.html
    const isLoginPage = window.location.pathname.includes('login.html');
    if (isLoginPage) {
        setupLoginEventListeners();
    }

    const isContactPage = window.location.pathname.includes('contact.html');
    if (isContactPage) {
        setupContactEventListeners();
    }

    const isAccountsPage = window.location.pathname.includes('accounts.html');
    if (isAccountsPage) {
        displayAccountsPage();
    }


    // Check if the user is logged in or not and redirect to Cart or Login page
    handleCartContainerClick();
    // Check if the user is logged in
    checkLoggedInUser();
    // Check and update the cart counter across every page.
    updateCartCounter();
});

//
// Functions run on multiple pages
//

// function to generate star icons based on rating
function generateStarIcons(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating % 1 !== 0;
    const emptyStars = 5 - Math.ceil(rating);

    let starsHTML = '';
    for (let i = 0; i < fullStars; i++) {
        starsHTML += '<i class="fa fa-star"></i>';
    }
    if (halfStar) {
        starsHTML += '<i class="fa fa-star-half-o"></i>';
    }
    for (let j = 0; j < emptyStars; j++) {
        starsHTML += '<i class="fa fa-star-o"></i>';
    }
    return starsHTML;
}

// Function check if user is logged in when Cart is clicked and redirect to Cart page or Login page
function handleCartContainerClick() {
    const cartContainer = document.querySelector('.cartContainer img');
    if (cartContainer) {
        cartContainer.addEventListener('click', function () {
            // Make AJAX request to check authentication status
            fetch('/api/v1/protected', {
                method: 'GET',
                credentials: 'include' // Include cookies in the request
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Check if user is logged in
                if (data.message == "Success") {
                    // User is logged in, redirect to cart page
                    window.location.href = './cart.html';
                } else {
                    // User is not logged in, redirect to login page
                    window.location.href = './login.html';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    }
}

// function to display a notification product is added cart
function showNotification(message) {
    const notificationContainer = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.classList.add('notification');
    notification.innerText = message;

    notificationContainer.appendChild(notification);

    notification.addEventListener('click', () => {
        hideNotification(notification, notificationContainer);
    });

    setTimeout(() => {
        notification.classList.add('hidden');
        setTimeout(() => {
            notificationContainer.removeChild(notification);
        }, 500); // fadeout animation time. needs to match CSS timing in .notification. js time is in ms css time is in s 
    }, 3000); // time the notification is displayed in ms
}

function showNotification2(message) {
    const notificationContainer = document.getElementById('notification-container2');
    const notification = document.createElement('div');
    notification.classList.add('notification2');
    notification.innerText = message;

    notificationContainer.appendChild(notification);

    notification.addEventListener('click', () => {
        hideNotification(notification, notificationContainer);
    });

    setTimeout(() => {
        notification.classList.add('hidden');
        setTimeout(() => {
            if (notificationContainer.contains(notification)){
                notificationContainer.removeChild(notification);
            }
        }, 500); // fadeout animation time. needs to match CSS timing in .notification. js time is in ms css time is in s 
    }, 3000); // time the notification is displayed in ms
}

function hideNotification(notification, container) {
    notification.classList.add('hidden');
    setTimeout(() => {
        container.removeChild(notification);
    }, 500); // fadeout animation time (needs to match CSS timing in .notification; JavaScript time is in ms, CSS time is in s)
}

// Function to check if a user is already logged in
function checkLoggedInUser() {
    fetch('/api/v1/protected', {
        method: 'GET',
        credentials: 'include' // This ensures that the browser includes the HTTPOnly cookie in the request
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 401) {
            return null;
        } else {
            throw new Error('Network response was not ok');
        }
    })
    .then(data => {
        // Update menu and hide login message with user's full name
        if (data.message == "Success") {
            updateMenuAndHideLoginMessage(data.user.fullname);
        }
    })
    .catch(error => {
        // Log any errors
        console.error('There was a problem with the fetch operation:', error);
    });
}


function updateMenuAndHideLoginMessage(data) {
    document.getElementById('menuItems').querySelector('li:last-child').innerHTML = `<a href="./accounts.html">Hello ${data}</a>`;
}

function hideLoginMessage() {
    const loginMessage = document.querySelector('.loginMessage');
    loginMessage.classList.add('hide');
}

//
// Function run on index.html
//

// Function to populate the Latest Product module
async function populateLatestProducts(productData) {
    try {
        // Wait for the product data to be fetched and sorted
        const sortedProductData = await fetchAndSortProductData(productData);
        const row = document.getElementById('latestProductsRow');
        // Clear existing content in the row
        row.innerHTML = '';

        // Populate the Latest Product module with the 8 most recently added products
        for (let i = 0; i < 8 && i < sortedProductData.length; i++) {
            const product = sortedProductData[i];
            const firstImage = product.first_image;
            const fullName = product.fullName;
            const price = parseFloat(product.price);
            const sku = product.sku;
            const star = parseFloat(product.star);
            // Create the product HTML dynamically
            const productHTML = `
                <div class="col-4">
                    <a href="./product-details.html?sku=${sku}">
                        <img src="/static/img/${firstImage}" alt="${fullName}">
                        <h4>${fullName}</h4>
                        <div class="rating">
                            ${generateStarIcons(star)}
                        </div>
                        <p>£${price.toFixed(2)}</p>
                    </a>
                </div>
            `;

            // Append the product HTML to the row
            row.innerHTML += productHTML;
        }
    } catch (error) {
        console.error('Error fetching and populating latest products:', error);
    }
}

// Function to fetch and sort product data
function fetchAndSortProductData(productData) {
    return productData.sort((a, b) => new Date(b.date) - new Date(a.date));
}

//
// Function run on Products page
//

function getAllProducts() {
    return fetch('/api/v1/allproducts', {
        method: 'GET',
        credentials: 'include' // Include cookies in the request
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to add event listeners for filter and sort
function setupFilterAndSortEventListeners(productData) {
        const filterByTypeDropdown = document.getElementById('filterByType');
        const sortByDropdown = document.getElementById('sortBy');
    
        filterByTypeDropdown.addEventListener('change', onDropdownChange);
        sortByDropdown.addEventListener('change', onDropdownChange);
    
        // Event listener function
        function onDropdownChange() {
            const selectedType = filterByTypeDropdown.value;
            const selectedSort = sortByDropdown.value;
            
            // Update the URL with the selected filter or sort
            window.history.replaceState({}, '', `?filter=${selectedType}&sort=${selectedSort}`);
            
            // Call the function to populate products based on filter and sort
            populateProductsPage(productData, selectedType, selectedSort);
        }
}

// Function to populate Products page with filters and sort
function populateProductsPage(productData, filterType = 'all', sortType = 'default') {
   
    // Use the filter from the URL if available, otherwise use the default
    filterType = getURLParameter('filter') || filterType;

    const productRow = document.getElementById('productRow');
    productRow.innerHTML = '';

    // Apply filter by type
    const filteredProducts = (filterType !== 'all') ? productData.filter(product => product.type.toLowerCase() === filterType.toLowerCase()) : productData;

    // Apply sorting
    const sortedProducts = sortProducts(filteredProducts, sortType);

    // Populate the Products page with filtered and sorted products
    sortedProducts.forEach((product) => {
        const productHTML = generateProductHTML(product);
        productRow.insertAdjacentHTML('beforeend', productHTML);
    });
}

// Get URL parameters function
function getURLParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Function to generate product HTML
function generateProductHTML(product) {
    return `
        <div class="col-4">
            <div class="product">
                <a href="./product-details.html?sku=${product.sku}">
                    <img src="/static/img/${product.first_image}" alt="${product.fullName}">
                    <h4>${product.fullName}</h4>
                    <div class="rating">
                        ${generateStarIcons(parseFloat(product.star))}
                    </div>
                    <p>£${parseFloat(product.price).toFixed(2)}</p>
                </a>
            </div>
        </div>
    `;
}

// Function to populate the "Filter by Type" dropdown
function populateFilterByTypeDropdown(productData) {
    const filterByTypeDropdown = document.getElementById('filterByType');
    const uniquePTypes = [...new Set(productData.map(product => product.type))];

    uniquePTypes.forEach(type => {
        const option = document.createElement('option');
        const capitalizedType = type.charAt(0).toUpperCase() + type.slice(1).toLowerCase();
        option.value = capitalizedType; // Ensure option value is also capitalized
        option.textContent = capitalizedType;
        filterByTypeDropdown.appendChild(option);
    });
}

// Function to sort products based on selected option
function sortProducts(products, sortType) {
    switch (sortType) {
        case 'default':
            return products.sort((a, b) => a.sku - b.sku);
        case 'priceH':
            return products.sort((a, b) => b.price - a.price);
        case 'priceL':
            return products.sort((a, b) => a.price - b.price);
        case 'rating':
            return products.sort((a, b) => b.star - a.star);
        default:
            return products.sort((a, b) => a.sku - b.sku);
    }
}

//
// Function run on product-details page
//

function getProductDetails(sku) {
    return fetch(`/api/v1/productdetails?sku=${sku}`, { // Include SKU parameter in the URL
        method: 'GET',
        credentials: 'include' // Include cookies in the request
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

// Function to populate the product-details page based on the SKU passed via URL
async function fetchProductDetails(sku) {
    const product = await getProductDetails(sku);
    document.title = `Red Store | ${product.fullName}`;

    const imagesArray = product.images.split(',');
    const detailsListArray = JSON.parse(product.detailsList);
    const detailsListHTML = detailsListArray.map(detail => `<li>${detail}</li>`).join('');

    // Generate HTML elements for each image
    const smallImagesHTML = imagesArray.map(image => `
        <div class="small-img-col">
            <img src="/static/img/${image.trim()}">
        </div>
    `).join('');

    if (product) {
        const productDetailsHTML = `
            <div class="col-2">
                <img id="mainProduct" src="/static/img/${imagesArray[0].trim()}">
                <div class="small-img-row" id="smallImages">
                    ${smallImagesHTML}
                </div>
            </div>
            <div class="col-2">
                <p>${product.type} \\ SKU-${product.sku}</p>
                <h1>${product.fullName}</h1>
                <div class="rating">
                    ${generateStarIcons(parseFloat(product.star))}
                </div>
                <h4>£${parseFloat(product.price).toFixed(2)}</h4>
                <select name="selectSize" id="selectSize">
                    ${product.sizes.split(',').map(size => `<option value="${size.trim()}">${size.trim()}</option>`).join('')}
                </select>
                <input id="quantity" type="number" value="1">
                <a id="addToCartBtn" href="" class="btn">Add to cart</a>
                <h3>Product details <i class="fa fa-indent"></i></h3>
                <p>${product.detail}</p></br>
                <ul class="pDetailList">${detailsListHTML}</ul></br>
                <p>${product.materials}</p>
            </div>
        `;

        productDetailsRow.innerHTML = productDetailsHTML;

        // Change the main product image on product-details.html
        if (smallImages) {
            smallImages.addEventListener('click', function (event) {
                var target = event.target.closest('.small-img-col');
                if (target) {
                    var newSrc = target.querySelector('img').src;
                    mainProduct.src = newSrc;
                }
            });
        } else {
        console.error('Element with ID "smallImagesContainer" and "mainProductImage" not found.');
        }

        // addToCartBtn is generated using JS in the above block of code.
        if (addToCartBtn) {
            addToCartBtn.addEventListener('click', function (event) {
                event.preventDefault();

                // Get the selected size and quantity
                const sizeSelect = document.getElementById('selectSize');
                const quantity = parseInt(document.getElementById('quantity').value, 10) || 0;
                let selectedSize;

                switch(sizeSelect.options[sizeSelect.selectedIndex].value) {
                    case "S":
                        selectedSize = "Small";
                        break;
                    case "M":
                        selectedSize = "Medium";
                        break;
                    case "L":
                        selectedSize = "Large";
                        break;
                    case "XL":
                        selectedSize = "X-Large";
                        break;
                    case "XXL":
                        selectedSize = "XX_large";
                        break;
                };

                addToCart(product, selectedSize, quantity);
                showNotification(`${quantity} ${product.fullName}(s) size ${selectedSize} added to the cart!`);
            });
        } else {
            console.error('Element with ID "addToCartBtn" not found.');
        }
    }  
}
        
// Function to add selected product to cart and store data to local storage
function addToCart(product, size, quantity) {
    // Get the existing cart data from local storage or initialize an empty array
    let cartItems = JSON.parse(localStorage.getItem('cart')) || [];

    // Check if the product is already in the cart
    const existingItem = cartItems.find(item => parseInt(item.sku) === parseInt(product.sku) && item.size === size);

    if (existingItem) {
        // Update the quantity and size if the product is already in the cart
        existingItem.quantity += quantity;
    } else {
        // Add a new item to the cart
        const newItem = {
            sku: product.sku,
            size: size,
            quantity: quantity,
        };
        cartItems.push(newItem);
    }

    // Save the updated cart data to local storage
    localStorage.setItem('cart', JSON.stringify(cartItems));

    // Update the cart counter display
    updateCartCounter();
}

// Function to fetch and display related products
async function fetchRelatedProducts(currentSku, productData) {

    const currentProduct = productData.find(product => product.sku == currentSku);

    if (currentProduct) {
        // Filter products based on the pType of the current product
        const relatedProducts = productData.filter(product => product.type === currentProduct.type && parseInt(product.sku) !== parseInt(currentSku));
        // Display up to 4 related products
        const maxRelatedProducts = 4;

        for (let i = 0; i < maxRelatedProducts && i < relatedProducts.length; i++) {
            const relatedProduct = relatedProducts[i];

            // Create the related product HTML dynamically
            const relatedProductHTML = `
                <div class="col-4">
                    <div class="product">
                        <a href="./product-details.html?sku=${relatedProduct.sku}">
                            <img src="/static/img/${relatedProduct.first_image}" alt="${relatedProduct.fullName}">
                            <h4>${relatedProduct.fullName}</h4>
                            <div class="rating">
                                ${generateStarIcons(parseFloat(relatedProduct.star))}
                            </div>
                            <p>£${parseFloat(relatedProduct.price).toFixed(2)}</p>
                        </a>
                    </div>
                </div>
            `;

            // Append the related product HTML to the row
            relatedProductsRow.innerHTML += relatedProductHTML;
        }
    } else {
        console.log('Current product not found');
    }
}

// Function to update the cart counter display
function updateCartCounter() {
    const cartCounter = document.querySelector('.cartCounter');
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];

    // Update the cart counter based on the total quantity in the cart
    const totalQuantity = cartItems.reduce((total, item) => total + item.quantity, 0);
    cartCounter.innerHTML = totalQuantity.toString();

    // Show or hide the cart counter based on whether there are items in the cart
    cartCounter.style.display = totalQuantity === 0 ? 'none' : 'block';
}

//
// Function runs only in the Cart page
//

// Function to display cart items stored in local storage on the carts page
async function displayCartItems() {
    const productData = await getAllProducts('/api/v1/allproducts');
    const cartItemsContainer = document.getElementById('tableBody');
    const totalPriceContainer = document.querySelector('.totalPrice');
    const cartItems = JSON.parse(localStorage.getItem('cart')) || [];
    let total = 0;
    // check if there is anything in the cart
    if (cartItems.length > 0) {
        // Populate cart items dynamically
        cartItems.forEach(item => {
            // find product details based on the pSku value stored in the local storage
            const product = productData.find(product => product.sku === item.sku);
            if (product) {
                // generate html for cart page
                const cartItemHTML = `
                    <tr>
                        <td>
                            <div class="cart-info">
                                <img src="/static/img/${product.first_image}" alt="${product.fullName}">
                                <div>
                                    <p>${product.fullName}</p>
                                    <small>SKU-${product.sku}</small>
                                    <small>Price: £${parseFloat(product.price).toFixed(2)}</small>
                                    <a href="#" onclick="removeCartItem('${product.sku}', '${item.size}'); return false;">Remove</a>
                                </div>
                            </div>
                        </td>
                        <td><p>${item.size}</p></td>
                        <td><p>${item.quantity}</p></td>
                        <td><p>£${(item.quantity * parseFloat(product.price)).toFixed(2)}</p></td>
                    </tr>
                `;
                
                // Calculate the total price for the cart
                total += (item.quantity * product.price);

                // Append the cart item HTML to the cart items container
                cartItemsContainer.innerHTML += cartItemHTML;

                // Calculate tax and total
                const tax = total * 0.2;
                const subtotal = total * 0.8;

                // Update the total price table HTML
                const totalPriceHTML = `
                    <table>
                        <tbody>
                            <tr>
                                <td>Subtotal</td>
                                <td>£${(subtotal).toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Tax @ 20%</td>
                                <td>£${tax.toFixed(2)}</td>
                            </tr>
                            <tr>
                                <td>Total</td>
                                <td>£${total.toFixed(2)}</td>
                            </tr>
                        </tbody>
                    </table>
                `;
                totalPriceContainer.innerHTML = totalPriceHTML;
            } else {
                console.info('Product not found for SKU:', item.sku);
            }
        })
    };
}

function removeCartItem(sku, size) {
    let cartItems = JSON.parse(localStorage.getItem('cart')) || [];

    console.log(`values passed to function ${sku}, ${size}`);
    console.log(`valies in cartItems ${cartItems}`);
    
    // Remove item from the cart based on SKU and size
    cartItems = cartItems.filter(item => !(item.sku == sku && item.size == size));

    // Save the updated cart data to local storage
    localStorage.setItem('cart', JSON.stringify(cartItems));

    // Log cart items after removal
    console.log('Cart items after removal:', cartItems);

    // Update the cart display on the cart page
    //displayCartItems(); // Ensure productData is accessible
    updateCartCounter();
}


function addCartEventListners() {
    checkoutBtn.addEventListener('click', () => {
        event.preventDefault();
        showNotification2('Thank you for your purchase.');
    })
}

//
// Function run on Login page
//

// Function to add Event Listenrs on the Login page
function setupLoginEventListeners() {
    login.addEventListener('click', handleLogin);
    signup.addEventListener('click', handleSignup);
    // signupBlogintton.addEventListener('click', handleSignup);
    const title = document.querySelectorAll(".tab-header .title");
    title.forEach(function (title) {
        title.addEventListener("click", function () {
            const tabName = title.textContent.toLowerCase().trim();
            openTab(tabName);
        });
    });
    // Add event listeners to password fields
    document.querySelector('#upassword').addEventListener('input', checkPassword);
    document.querySelector('#confirmPassword').addEventListener('input', checkPassword);
}

// function to display login or sign-up fields on the login page
function openTab(tabName) {
    const tabs = document.getElementsByClassName("form-input");
    const tabHeader = document.getElementsByClassName("title");

    for (let i = 0; i < tabs.length; i++) {
        if (tabs[i].classList.contains(tabName)) {
            tabs[i].classList.add("active");
            tabHeader[i].classList.remove("notActive");
        } else {
            tabs[i].classList.remove("active");
            tabHeader[i].classList.add("notActive");
        }
    }
}

// Funciton to hash the password
function hashPassword(password) {
    return CryptoJS.SHA256(password).toString();
}

// Function to handle the login process
function handleLogin(event) {
    event.preventDefault();
    const enteredEmail = document.getElementById('email').value;
    const enteredPassword = document.getElementById('password').value;
    const passwordHash =  hashPassword(enteredPassword);
    
    fetch(`/api/v1/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: enteredEmail,
            password: passwordHash
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to login');
        }
        return response.json();
    })
    .then(data => {
        window.location.href = './accounts.html';
        return
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
    });
}

// Function to handle the signup process. It checks if all fields are completed. Functions are divided between handling sign-up and actual registration to allow for future improvement such as input validation.
function handleSignup(event) {
    event.preventDefault();
    
    const message = document.querySelector('#signupMessage');
    const passwordChheck = checkPassword();
    const checkInput = inputCheck();

    if (!passwordChheck && !checkInput) {
        message.classList.remove('hide');
    } else {
        message.classList.add('hide');
        registration();
    }
}

// This function passes the input data vai API to the backend.
function registration() {
    const firstName = document.querySelector('#ufname').value;
    const lastName = document.querySelector('#ulname').value;
    const email = document.querySelector('#uemail').value;
    const password = document.querySelector('#upassword').value;
    const confirmedPassword = document.querySelector('#confirmPassword').value;
    const checkBox = document.querySelector('#confirmBox').checked;

    const passwordHash = hashPassword(password);
    const confirmHash = hashPassword(confirmedPassword)

    const userData = {
        firstname: firstName,
        lastname: lastName,
        email: email,
        password: passwordHash,
        confirmedPassword: confirmHash,
        checkBox: checkBox
    };

    // Make a POST request to the API
    fetch('/api/v1/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle API response data here
        window.location.href = './index.html';
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });
}

function inputCheck() {
    const inputFields = document.querySelectorAll('#ufname, #ulname, #uemail, #upassword, #confirmPassword, #confirmBox');

    if(inputFields[0].value !== '' || 
       inputFields[1].value !== '' || 
       inputFields[2].value !== '' || 
       inputFields[3].value !== '' || 
       inputFields[4].value !== '' || 
       !inputFields[5].checked) {
        return true;
    } else {
        return false;
    }
}

function checkPassword() {
    const password = document.querySelector('#upassword').value;
    const confirmPassword = document.querySelector('#confirmPassword').value;
    const passwordInput = document.querySelector('#upassword');
    const confirmPasswordInput = document.querySelector('#confirmPassword');
    const passwordMessage = document.querySelector('#signupMessage');

    if (password !== confirmPassword) {
        passwordInput.classList.add('password-mismatch');
        confirmPasswordInput.classList.add('password-mismatch');
        passwordMessage.classList.remove('hide');
        return false; // Passwords don't match, return false
    } else {
        passwordInput.classList.remove('password-mismatch');
        confirmPasswordInput.classList.remove('password-mismatch');
        passwordMessage.classList.add('hide');
        return true; // Passwords match, return true
    }
}

//
// Function run on Contact page
//

// add event listners to the contact us page
function setupContactEventListeners() {
    reason.addEventListener('change', checkSelectedOptions);
    contactUs.addEventListener('click', contactMessage);
}

// Function to check options and display additional input fields
function checkSelectedOptions() {
    const productNo = document.getElementById('productNo');
    const orderNo = document.getElementById('orderNo');
    const selectedOption = document.getElementById('reason').value;

    if (selectedOption === 'product') {
        productNo.classList.remove('hidden');
        orderNo.classList.add('hidden');
    } else if (selectedOption === 'order') {
        orderNo.classList.remove('hidden');
        productNo.classList.add('hidden');
    } else {
        productNo.classList.add('hidden');
        orderNo.classList.add('hidden');
    }
}

// Display thank you message when contact us form is completed
function contactMessage(event) {
    event.preventDefault();
    const inputFields = document.querySelectorAll('#reason, #productNo, #orderNo, #name, #email, #textarea');
    const reasonSelect = document.getElementById('reason');
    const message = document.querySelector('.loginMessage');

    if (inputFields[3].value  && inputFields[4].value && inputFields[5].value){
        showNotification2('Thank you for contacting us. We will reply as soon as possible.');
        inputFields.forEach(function (inputField) {
            inputField.value = '';
        })
        reasonSelect.selectedIndex = 0;
        message.classList.add('hide');
    } else {
        message.classList.remove('hide');
    }
}

// 
// Accounts page functions
//

function displayAccountsPage() {
    fetch('/api/v1/protected', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Check if user is logged in
        if (data.message === "Success") {
            displayAccountInformation();
        } else if (data.message === "Not logged in") {
            // User is not logged in, redirect to login page
            window.location.href = './login.html';
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function displayAccountInformation() {
    fetch('/api/v1/accounts', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        printUserInformation(data);
        accountPageEventListener();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    })
}

function printUserInformation(data) {
    const userId = document.getElementById('userId');
    const firstName = document.getElementById('firstName');
    const lastName = document.getElementById('lastname');
    const phoneNumber = document.getElementById('phoneNumber');
    const emailElement = document.getElementById('email');
    const address = document.getElementById('address');
    const city = document.getElementById('city');
    const country = document.getElementById('country');
    const postCode = document.getElementById('postCode');
    const date = document.getElementById('date');

    // Set innerHTML of each <p> tag with corresponding data
    userId.value = data.user_id.toString().padStart(5,0);
    date.value = data.registration_datetime;
    firstName.value = data.fname;
    lastName.value = data.lname;
    phoneNumber.value = (data.phone || ""); 
    emailElement.value = data.email;
    address.value = (data.address || "");
    city.value = (data.city || "");
    country.value = (data.country || "");
    postCode.value = (data.postcode || "");
}

function accountPageEventListener() {
    const updateDetailsButton = document.getElementById('updateDetails');
    updateDetailsButton.addEventListener('click', updateInformation);
}

function updateInformation(event) {
    event.preventDefault();
    const uuserId = document.getElementById('userId').value;
    const uphoneNumber = document.getElementById('phoneNumber').value;
    const uaddress = document.getElementById('address').value;
    const ucity = document.getElementById('city').value;
    const ucountry = document.getElementById('country').value;
    const upostCode = document.getElementById('postCode').value;

    const data = {
        user_id: parseInt(uuserId),
        phoneNumber: uphoneNumber,
        address: uaddress,
        city: ucity,
        country: ucountry,
        postCode: upostCode
    };

    // Make a POST request to the API
    fetch('/api/v1/moreinfo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle API response data here
        showNotification('Details updated');
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });
}