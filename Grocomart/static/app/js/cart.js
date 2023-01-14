const updateBtns = document.getElementsByClassName('update-cart');


for(let i =0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', () => {
        var productId = updateBtns[i].getAttribute('data-product');
        var action = updateBtns[i].getAttribute('data-action');
        console.log(`Product Id: ${productId}, Action: ${action}`);
        console.log(`User: ${user}`);

        if (user == 'AnonymousUser'){
                window.location = '/login/'
        }else{
            updateUserOrder(productId, action)
        }
    })
}


function updateUserOrder(productId, action){
    console.log("User authenticted sending data..")

    const url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        }, 
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log("Data:" , data);
        location.reload()
    })

}