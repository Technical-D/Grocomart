const menu = document.querySelector('#menu-bar');
const navbar = document.querySelector('.navbar');
const header = document.querySelector('.header-2');
const toTop = document.querySelector('.toTop')

menu.addEventListener('click', () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
});

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');

    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        toTop.style.display = 'flex';
        
    }else {
        toTop.style.display = "none";
    }
}

toTop.addEventListener('click', ()=> {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
})
