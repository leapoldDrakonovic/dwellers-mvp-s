const showPlanBtn = document.querySelector('#showPlan-btn')


showPlanBtn.addEventListener('click', showPlanModal)

function showPlanModal () {
   
    const body = document.getElementsByTagName('body')[0]
    const modalWin = document.querySelector('.modal.modal-plan-static')
    modalWin.style.display = 'block'
    body.style.overflow = 'hidden';
    body.style.pointerEvents = 'none';
    modalWin.style.pointerEvents = 'all';

    window.addEventListener("click", (e) => {
        if (e.target == modalWin){
            body.style.overflow = 'auto';
            body.style.pointerEvents = 'all';
            modalWin.style.display = 'none'
        }
    })

    const mod = document.querySelector("#modal-plan-flat")
    mod.addEventListener("click", (event) => {
        console.log(event)
    })
}