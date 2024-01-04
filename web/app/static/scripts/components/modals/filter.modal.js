const filterModalBtn = document.querySelector('#filter-modal-btn');
filterModalBtn.addEventListener('click', showFilterModal) 

function showFilterModal () {    
    const body = document.getElementsByTagName('body')[0];
    const modalWin = document.querySelector('.modal.modal-filter')
    
    modalWin.style.display = 'block'
    body.style.overflow = 'hidden';
    body.style.pointerEvents = 'none';
    modalWin.style.pointerEvents = 'all';

    const closeBtn = document.querySelector('#filter-modal-x-btn');
    closeBtn.addEventListener('click', ()=> {
        body.style.overflow = 'auto';
        body.style.pointerEvents = 'all';
        modalWin.style.display = 'none'
    })
}




