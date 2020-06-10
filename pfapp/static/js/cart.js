if (document.readyState == 'loading') {
    document.addEventListener('DOMContentLoaded', ready)
} else {
    ready()
}

function ready() {

    iscartempty()

    var removeCartItemButtons = document.getElementsByClassName('removebutton')
    for (var i = 0; i < removeCartItemButtons.length; i++) {
        var button = removeCartItemButtons[i]
        button.addEventListener('click', removeCartItem)
    }

    var addToCartButtons = document.getElementsByClassName('addtocartbutton')
    for (var i = 0; i < addToCartButtons.length; i++) {
        var button = addToCartButtons[i]
        button.addEventListener('click', addToCartClicked)
    }

    document.getElementById('btn-purchase').addEventListener('click', purchaseClicked)

    // document.getElementById('reviewbtn').addEventListener('click', addreview)
}

// function addreview () {
//     var reviewee = $("[name='reviewee']").val();
//     var reviewtext = $("[name='reviewtext']").val();
//     var rating = $("input[name='star']:checked").val();
//     var el = document.getElementsByName("csrfmiddlewaretoken")
//     var csrf_value = el[0].getAttribute("value")
//     console.log(reviewee)
//     console.log(reviewtext)
//     console.log(rating)
//     data = {'reviewee':reviewee,'reviewtext':reviewtext,'rating':rating}
//     $.ajax(
//         {
//             url: '/addreview/',
//             type: 'POST',
//             data: {'data':data},
//             headers:{"X-CSRFToken": csrf_value },
//             success:function(response){
//                 alert('Your review is submitted.\n ');
//                 location.reload();
//             },
//             error:function(){
//                 alert('Please try again later.\n ');
//                 location.reload();
//             },
            
//         });

// }


function purchaseClicked() {
    var cartItems = document.getElementsByClassName('cart_items')[0]
    var cartItemids = cartItems.getElementsByClassName('contrid')
    var listofids = []
    var consumerid = parseFloat(document.getElementsByClassName('as_bf')[0].innerText)
    var farmerid = parseFloat(document.getElementsByClassName('fm_cs')[0].innerText)
    var el = document.getElementsByName("csrfmiddlewaretoken")
    var csrf_value = el[0].getAttribute("value")
    // var dict = {cid:userid, list:listofids[],'CSRFToken': csrf_value}
    // console.log('initial list:'+listofids)
    for (var i = 0; i < cartItemids.length; i++) {
        // console.log('number of ids'+cartItemids.length)
        var proid = parseFloat(cartItemids[i].innerText)
        listofids[i]=proid
    }
    var total = document.getElementById('totalpriceelement').innerText
    console.log(total)
    var data = {'consumerid':consumerid,'farmerid':farmerid,'listofids':listofids,'total':total}
    console.log(data)
    var data1 = JSON.stringify(data)
    console.log(data1)
    $.ajax(
        {
            url: '/checkout/',
            type: 'POST',
            data: {'data':data1},
            headers:{"X-CSRFToken": csrf_value },
            success:function(response){
                alert('Your purchase order is submitted.\n ');
                window.location.href = '/orders/';
            },
            error:function(){
                alert('Please try again later.\n ');
                location.reload();
            },
            
        });
    
}

function removeCartItem(event) {
    var buttonClicked = event.target
    buttonClicked.parentElement.parentElement.remove()
    iscartempty()
    updateCartTotal()
    iscartempty()
}

function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart_items')[0]
    // console.log(cartItemContainer)
    var cartRows = cartItemContainer.getElementsByClassName('cart_row')
    // console.log(cartRows)
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('price')[0]
        var price = parseFloat(priceElement.innerText.replace('₹', '').replace('/- Indian Rupees',''))
        total = total + price;
    }
    total = Math.round(total * 100) / 100
    document.getElementById('totalpriceelement').innerText ='Total : ' + '₹' + total +'/- Indian Rupees'
    iscartempty()
}

function addToCartClicked(event) {
    var button = event.target
    var shopItem = button.parentElement.parentElement
    var title = shopItem.getElementsByClassName('productname')[0].innerText
    var price = shopItem.getElementsByClassName('productprice')[0].innerText
    var id = shopItem.getElementsByClassName('contractid')[0].innerText
    // console.log(title,price,id)
    iscartempty()
    addItemToCart(title, price, id)
}

function addItemToCart(title, price,id) {
    var cartRow = document.createElement('div')
    cartRow.classList.add('cart_row_items')
    var cartItems = document.getElementsByClassName('cart_items')[0]
    var cartItemNames = cartItems.getElementsByClassName('name')
    for (var i = 0; i < cartItemNames.length; i++) {
        if (cartItemNames[i].innerText == title) {
            alert('This item is already added to the cart')
            return
        }
    }
    var cartRowContents = `
    <div class="row cart_row" style="padding: 5px;">
        <div style="display: none;"><h5 class="contrid" id='contrid'>${id}</h5></div>
        <div class="col-sm-3"><h5 class="name">${title}</h5></div> 
        <div class="col-sm-6"><h5 class="price">${price}</h5></div>
        <div class="col-sm-3">
            <button type="button" class="btn btn-danger removebutton" style="float: right;" id="removebutton" >Remove</button>
        </div>
    </div>`
    cartRow.innerHTML = cartRowContents
    cartItems.append(cartRow)
    // console.log(cartRow)
    cartRow.getElementsByClassName('removebutton')[0].addEventListener('click', removeCartItem)
    updateCartTotal()
    iscartempty()

}

function iscartempty(){
    if (document.getElementById('cart_items').hasChildNodes() == true)
    {
        document.getElementById('cartemptymsg').innerText = ''
    }
    else {
        document.getElementById('cartemptymsg').innerText = 'Cart is Empty'
    }
}