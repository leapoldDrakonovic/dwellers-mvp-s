// Burger menu

const navPopup = document.getElementById('navPopup')
const burgerOpenBtn = document.getElementById ('header-burger')
const burgerCloseBtn = document.querySelector ('.nav-menu-popup-back')
const burgerLinks = document.querySelectorAll ('.burger-nav-item')


burgerOpenBtn.addEventListener('click', showPopupMenu);
burgerCloseBtn.addEventListener('click', showPopupMenu);

function showPopupMenu () {
    const body = document.getElementsByTagName('body')[0]

    navPopup.classList.toggle('active')
    
    navPopup.classList.value === 'nav-menu-popup active' 
    ? body.style.overflowY = 'hidden' 
    : body.style.overflowY = 'scroll'

    
    burgerLinks.forEach(link=> {
        link.onclick = () => {
            navPopup.classList.remove('active')
            body.style.overflowY = 'scroll'
        }
    })
}