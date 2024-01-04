
const galleryBtn = document.querySelector('#gallery-void-btn')
galleryBtn.addEventListener('click', showGalleryModal)

const htmlLang = document.querySelector('html').getAttribute('dir')

function showGalleryModal () {
    const modalWin = document.querySelector('.modal.modal-gallery')
    const body = document.getElementsByTagName('body')[0];
    modalWin.style.display = 'block'
    body.style.overflow = 'hidden';
    body.style.pointerEvents = 'none';
    modalWin.style.pointerEvents = 'all';

    const elemImg = Array.from(document.querySelectorAll('.gallery-modal-slider-element'))
    const scrollView = document.querySelector('.gallery-modal-slider-wrapper')
    scrollView.addEventListener('wheel', (event)=> {
        sliderWrapper.scrollLeft += event.deltaY;
    })

    elemImg.forEach(elem=>{
        elem.addEventListener('click', chooseImg)
    })
    elemImg[0].classList.add('active')
    loadWrapperImage (elemImg[0].style.backgroundImage)

    function chooseImg () {
        if(this.classList) {
            for (var j = 0; j < elemImg.length; j++) {
                elemImg[j].classList.remove('active');
            }
            this.classList.add('active')
            this.scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });

        }

        loadWrapperImage (this.style.backgroundImage)
    }

    // Логика кнопок в галереи

    const prevBtn = document.querySelector('#gallery-prev'),
          nextBtn = document.querySelector('#gallery-next')

    prevBtn.addEventListener('click', prevSlide)
    nextBtn.addEventListener('click', nextSlide)

    function nextSlide() {
        var currInd = elemImg.findIndex(el=>el.classList.contains('active'))
       if (htmlLang == 'rtl') {
            if (currInd == 0) {
                var length = elemImg.length
                elemImg[currInd].classList.remove('active')
                elemImg[length-1].classList.add('active')
                elemImg[length-1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
                loadWrapperImage(elemImg[length-1].style.backgroundImage)

                return
            }
            elemImg[currInd].classList.remove('active')
            elemImg[currInd-1].classList.add('active')
            elemImg[currInd-1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
            loadWrapperImage(elemImg[currInd-1].style.backgroundImage)
            return
       }

        if (currInd == (elemImg.length-1)) {
            elemImg[currInd].classList.remove('active')
            currInd = 0
            elemImg[currInd].classList.add('active')
            elemImg[currInd].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
    
            loadWrapperImage(elemImg[currInd].style.backgroundImage)

            return
        }
        elemImg[currInd].classList.remove('active')
        elemImg[currInd+1].classList.add('active')
        elemImg[currInd+1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });

        loadWrapperImage(elemImg[currInd+1].style.backgroundImage)
    }

    
    function prevSlide() {
        var currInd = elemImg.findIndex(el=>el.classList.contains('active'))
        if (htmlLang == 'rtl') {
            if (currInd == (elemImg.length-1)) {
                elemImg[currInd].classList.remove('active')
                currInd = 0
                elemImg[currInd].classList.add('active')
                elemImg[currInd].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
        
                
                loadWrapperImage(elemImg[currInd].style.backgroundImage)
    
                return
            }
            elemImg[currInd].classList.remove('active')
            elemImg[currInd+1].classList.add('active')
            elemImg[currInd+1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
    
            loadWrapperImage(elemImg[currInd+1].style.backgroundImage)
            return
        }
        if (currInd == 0) {
            var length = elemImg.length
            elemImg[currInd].classList.remove('active')
            elemImg[length-1].classList.add('active')
            elemImg[length-1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
            loadWrapperImage(elemImg[length-1].style.backgroundImage)

            return
        }
        elemImg[currInd].classList.remove('active')
        elemImg[currInd-1].classList.add('active')
        elemImg[currInd-1].scrollIntoView({ behavior: 'smooth', block: 'start', inline: "center"  });
        loadWrapperImage(elemImg[currInd-1].style.backgroundImage)
        

    }
    

    const closeBtn = document.querySelector('#gallery-x');
    closeBtn.addEventListener('click', ()=> {
        body.style.overflow = 'auto';
        body.style.pointerEvents = 'all';
        modalWin.style.display = 'none'
    })

    
    window.addEventListener("click", (e) => {
        const modals = document.querySelector(".modal-gallery")
        if (e.target == modals){
            body.style.overflow = 'auto';
            body.style.pointerEvents = 'all';
            modalWin.style.display = 'none'
        }
    })
    

    
}

function loadWrapperImage (image) {
    const viewWrapper = document.querySelector('.gallery-modal-view-wrapper')
    viewWrapper.style = `
    height: 100%;
    width: 100%;
    background: ${image};
    background-repeat: no-repeat;
    background-position: center;
    background-size:contain;
`
}








