while( document.readyState='complete')
{
    console.log('loaded')
    ready()
}




function ready() {
    var removeCartItemButtons = document.getElementById('removebutton')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    var addToCartButtons = document.getElementById('addtocartbutton')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    // updateCartTotal()
}


function addToCartClicked(event) {
    var button = event.target
    var shopItem = button.parentElement.parentElement
    var name = shopItem.getElementById('productname')[0].innerText
    var price = shopItem.getElementById('productprice')[0].innerText
    var imageSrc = shopItem.getElementById('productimg')[0].src
    console.log(name,price)
    // addItemToCart(title, price, imageSrc)
    // updateCartTotal()
}

