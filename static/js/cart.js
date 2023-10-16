var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId : ', productId, 'action : ', action)

        console.log('USER : ', user)
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action)
        }
        else {
            // console.log('User loged in , sending data....')
            updateUserOrderCart(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in!!!!!')

    /* our cookie cart looks like this
    // cart={
       1:{'quantity': 4},
       4:{'quantity': 0},
       6:{'quantity': 3}

     } */

// ye cart main.html wala hai     
    if (action == 'add_new') {
        // if (cart[productId] == undefined) {
        //     cart[productId] = {'quantity': 1}
        // }
        // else {
        //     pass
        // }
        cart[productId] = {'quantity': 1}

    }

    if(action == 'add')
    {
        cart[productId]['quantity'] += 1
    }

    if (action == 'remove') {

        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]
        }

    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

    location.reload()
}

function updateUserOrderCart(productId, action) {
    console.log('User loged in , sending data....')

    var url = '/update_item/'  // the url where we have to send the data

    // Now using fetch API we sending the data to the backend (BUT WE CAN'T SEND THE DATA TO THE BACKEND IN DJANGO WITHOUT CSRF TOKENS  (WE HAVE TO USE CSRF TOKEN WHICH IS USE ONLY WITH THE FORMS IN DJANGO) WE SIMPLY WRITE THE CODE OF CSRF TOKEN IN MAIN.HTML AND USE IT HERE)
    fetch(url, {
        method: 'POST', // as we sending the data the method will be 'POST'
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken //taking care of csrf token

        },
        body: JSON.stringify({ 'productId': productId, 'action': action }) // from here we send the data to the backend, the send is in the object form the we stringify it.
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