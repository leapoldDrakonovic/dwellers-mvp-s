
const flatSlides = document.querySelectorAll ('.flat-page-slider-slide'),
    flatBGI = document.querySelector(".flat-page-main-section-bgi");

flatSlides[0].classList.add ('active')

/*
var beginBtn = document.querySelector('#begin-btn')
beginBtn.addEventListener('click', ()=> {
    for (var j = 0; j < flatSlides.length; j++) {
        flatSlides[j].classList.remove('active');
    }
    flatSlides[0].classList.add ('active')
    flatBGI.style.backgroundImage = `url(${flatSlides[0].src})`
    flatSlides[0].scrollIntoView({ behavior: 'smooth', block: 'end', inline: "start"  })
    // beginBtn.style.display = 'none'
    showTitleAndPrice ()
})
*/

flatSlides.forEach(slide => {
    slide.addEventListener('click', chooseSlide)
})


var planBlock = document.querySelector('.flat-page-main-section-content-upBlock-plan')
var length = flatSlides.length
planBlock.addEventListener('click', ()=> {
    for (var j = 0; j < flatSlides.length; j++) {
        flatSlides[j].classList.remove('active');
    }
    flatSlides[length-1].classList.add('active')
    flatBGI.style.backgroundImage = `url(${flatSlides[length-1].src})`
    flatSlides[length-1].scrollIntoView({ behavior: 'smooth', block: 'end', inline: "start"  })
    // beginBtn.style.display = 'block'

    showTitleAndPrice ()
})




let slideIndex = 0

function chooseSlide () {
    if(this.classList) {
        for (var j = 0; j < flatSlides.length; j++) {
            flatSlides[j].classList.remove('active');
        }

        this.classList.add('active')
        this.scrollIntoView({ behavior: 'smooth', block: 'end', inline: "center"  })
    }

    // var isFirstElement = flatSlides[0].classList.contains('active')
    // if (!isFirstElement) {
    //     beginBtn.style.display = 'block'
    // }
    flatBGI.style.backgroundImage = `url(${this.src})`

    showTitleAndPrice ()
    
    
}

function showTitleAndPrice () {
    const content = document.querySelector('.flat-page-main-section-content-upBlock')
    const priceBox = document.querySelector('.flat-page-main-section-content-downBlock-pricebox')
    const downBlock = document.querySelector (".flat-page-main-section-content-downBlock")
    if (!flatSlides[0].classList.contains('active')){
         content.style.display = 'none'
        priceBox.style.display = 'none'
        downBlock.style.bottom = '6%'
    } else {
        downBlock.style.bottom = '-10%'
        content.style.display = 'flex'
        priceBox.style.display = 'block'
        // flatBGI.style = `
        //     background: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, rgba(0, 0, 0, 0) 100%), url("${flatSlides[0].src}");
        //     filter: drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25));
        // `
    }
}