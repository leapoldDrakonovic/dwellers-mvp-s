
// <========================

// Apart page flat logic
const flatListBtn = document.querySelectorAll('.apartment-flatlist-element-flats')
flatListBtn.forEach((elem)=> {
    elem.style.cursor = "pointer"
    elem.onclick = showApartPlan;
    
})

function showApartPlan() {
    const apartWrapper = document.querySelector('.apartment-plans-wrapper')
    const flatIcon = this.children[0]

    if (apartWrapper.style.display === "none") {
        apartWrapper.style.display ='block' 
        flatIcon.style.transform = 'rotate(180deg)'
    } else {
        apartWrapper.style.display = 'none';
        flatIcon.style.transform = 'rotate(360deg)'
    }


}

// Achors

const anchors = document.querySelectorAll('a[href*="#"]');
for (let anchor of anchors) {
    anchor.addEventListener('click', (event)=> {
        const sectionSearch = document.querySelector('#search')
        if(event.target.getAttribute('href') == '/#search' && !sectionSearch) return
        if(event.target.getAttribute('href') == '/#search' && !!sectionSearch) {
            event.preventDefault()
            var blockID = anchor.getAttribute('href')
            let firstChr = blockID.charAt(0)
            if (firstChr == '/') {blockID = blockID.slice(1)}
            document.querySelector(''+blockID).scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            })
            return
        }
        event.preventDefault()
        var blockID = anchor.getAttribute('href')
        document.querySelector(''+blockID).scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        })
    })
}



// Plans on flatlist


var flatListElements = document.querySelectorAll('.apartment-flatlist-element')

flatListElements.forEach(flatListElem=> {
    var planBtn = flatListElem.querySelector('.apartment-flatlist-element-plan')
    var plan = flatListElem.querySelector('.plan-wrapper')
    planBtn.addEventListener('mouseenter', showFlatlistPlan)
    planBtn.addEventListener('mouseleave', showFlatlistPlan)
    planBtn.addEventListener('click', openPlanModal)
    

    function openPlanModal () {
        var modalWin = document.createElement('div')
        modalWin.className = 'modal modal-plan'
        var planImg = plan.querySelector('img')
        modalWin.innerHTML = `
        <div class="flatplan-modal-window">
            <div class="flatplan-modal-window-wrapper">
                <img src="${planImg.src}" alt="">
        </div>
        `

        const body = document.querySelector('body')
        body.appendChild(modalWin)

        modalWin.style.display = 'block'
        body.style.overflow = 'hidden';
        body.style.pointerEvents = 'none';
        modalWin.style.pointerEvents = 'all';

        window.addEventListener("click", (e) => {
            const modals = document.querySelector(".modal.modal-plan")
            if (e.target == modals){
                body.style.overflow = 'auto';
                body.style.pointerEvents = 'all';
                modalWin.style.display = 'none'
                modalWin.remove()
            }
        })
    }

    function showFlatlistPlan() {       
        if (plan.style.display == 'block') {
            plan.style.display = 'none' 
        } else {
            plan.style.display = 'block'
            
        }


    }
})



function formatPrices() {
    const priceElements = document.querySelectorAll('.price');
    console.log(priceElements); // Предполагаем, что цены имеют класс 'price'
  
    priceElements.forEach((element) => {
      const priceString = element.textContent.trim();
      const priceNumber = parseFloat(priceString.replace(/\s/g, '')); // Удаляем пробелы из строки и преобразуем в число
  
      if (!isNaN(priceNumber)) {
        const formattedPrice = priceNumber.toLocaleString(); // Форматируем число с разделителем тысяч
        element.textContent = formattedPrice;
      }
    });
  }
  
  // Вызываем функцию для форматирования всех цен на странице при загрузке страницы

  document.addEventListener('DOMContentLoaded', formatPrices)