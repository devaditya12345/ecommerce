var updateBtns = document.getElementsByClassName('update-wishlist')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId : ', productId)

        console.log('USER : ', user)
        if (user == 'AnonymousUser') {
            alterCookieItem(productId, action)
        }
        else {
            // console.log('User loged in , sending data....')
            updateWishListUserOrder(productId)
        }
    })
}

var deleteBtns = document.getElementsByClassName('delete-wishlist')

for (var i = 0; i < deleteBtns.length; i++) {
    deleteBtns[i].addEventListener('click', function () {
        var wishlistProductID = this.dataset.wishlist
        var action = this.dataset.action
        

        console.log('USER : ', user)
        if (user == 'AnonymousUser') {
            alterCookieItem(wishlistProductID, action)
        }
        else {
            // console.log('User loged in , sending data....')
            deleteWishlistItem(wishlistProductID)
        }
    })
}

function alterCookieItem(productId, action) {
    console.log('Not logged in!!!!!')

    if (action == 'one') {

        if (wishlistcart[productId] == undefined) {
            // wishlistcart[productId] = {'quantity': 1}
            wishlistcart[productId] = 1
        }

        // wishlistcart[productId] = 1
    }

    if (action == 'remove') {

        wishlistcart[productId] -= 1

        if (wishlistcart[productId]<= 0) {
            console.log('Remove Item')
            delete wishlistcart[productId]
        }

    }

    console.log('wishlistcart :', wishlistcart)
    document.cookie = 'wishlistcart=' + JSON.stringify(wishlistcart) + ";domain=;path=/"

    location.reload()
}

function updateWishListUserOrder(productId) {
    console.log('User loged in , sending data....')

    var url = '/create_wishlist_item/'  // the url where we have to send the data

    // Now using fetch API we sending the data to the backend (BUT WE CAN'T SEND THE DATA TO THE BACKEND IN DJANGO WITHOUT CSRF TOKENS  (WE HAVE TO USE CSRF TOKEN WHICH IS USE ONLY WITH THE FORMS IN DJANGO) WE SIMPLY WRITE THE CODE OF CSRF TOKEN IN MAIN.HTML AND USE IT HERE)
    fetch(url, {
        method: 'POST', // as we sending the data the method will be 'POST'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken //taking care of csrf token

        },
        body: JSON.stringify({ 'product_id': productId }) // from here we send the data to the backend, the send is in the object form the we stringify it.
    })

        // here we get the response from the backend and convert it into a json object
        .then((response) => {
            return response.json()
        })

        //here we console the response as the data
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}

// #Mast tha ye
function deleteWishlistItem(wishlistProductID) {
    console.log('User loged in , sending data....')

    var url = `/delete_wishlist_item/${wishlistProductID}`  // the url where we have to send the data
    console.log("URL:", url)
    // Now using fetch API we sending the data to the backend (BUT WE CAN'T SEND THE DATA TO THE BACKEND IN DJANGO WITHOUT CSRF TOKENS  (WE HAVE TO USE CSRF TOKEN WHICH IS USE ONLY WITH THE FORMS IN DJANGO) WE SIMPLY WRITE THE CODE OF CSRF TOKEN IN MAIN.HTML AND USE IT HERE)
    fetch(url, {
        method: 'DELETE', // as we sending the data the method will be 'POST'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken //taking care of csrf token

        }
    })

        // here we get the response from the backend and convert it into a json object
        .then((response) => {
            return response.json()
        })

        //here we console the response as the data
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}