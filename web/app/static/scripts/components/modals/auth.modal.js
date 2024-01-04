const loginHeader = document.querySelector('#login');
const loginBm = document.querySelector('#login-bm');
if (loginHeader.dataset.value == 'Login') {
    loginHeader.onclick = openAuthWindow;
} // TEMP
if (loginBm.dataset.value == 'LoginBM') {
    loginBm.onclick = openAuthWindow;
} // TEMP

function openAuthWindow (event) {
    event.stopPropagation()
    const body = document.getElementsByTagName('body')[0];
    const modalWin = document.querySelector('.modal.auth-modal')
    modalWin.style.display = 'block'
 
    
    body.style.overflow = 'hidden';
    body.style.pointerEvents = 'none';
    modalWin.style.pointerEvents = 'all';


    const closeBtn = document.querySelector('#auth-x-btn');
    closeBtn.addEventListener('click', ()=> {
        body.style.overflow = 'auto';
        body.style.pointerEvents = 'all';
        modalWin.style.display = 'none'
    })

    window.addEventListener("click", (e) => {
        const modals = document.querySelector(".auth-modal")
        if (e.target == modals){
            body.style.overflow = 'auto';
            body.style.pointerEvents = 'all';
            modalWin.style.display = 'none'
        }
    })


}

