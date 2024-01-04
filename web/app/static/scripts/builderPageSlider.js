// builder page slider ====>

let slideIndex = 1;

showSlides(slideIndex);

setInterval(nextSlide, 5000)


function nextSlide() {
    showSlides(slideIndex += 1);
}


function previousSlide() {
    showSlides(slideIndex -= 1);
}


function currentSlide(n) {
    showSlides(slideIndex = n);
}


function showSlides(n) {
    
    let slides = document.getElementsByClassName("slide");

    if (n > slides.length) {
      slideIndex = 1
    }
    if (n < 1) {
        slideIndex = slides.length
    }

    for (let slide of slides) {
        slide.classList.remove('active')
    }

    slides[slideIndex - 1].classList.add('active')

    /*
    let slides = document.getElementsByClassName("slide");

    let need_to_make_active = false;
    let nothing_active_so_make_first_active = true;

    for (let slide in slides) {
        if ('active' == slide.classList) {
            slide.classList.remove('active');
            need_to_make_active = true;
        }
        else if (need_to_make_active) {
            slide.classList.add('active');
            nothing_active_so_make_first_active = false;
            need_to_make_active = false;
        }
    }

    if (nothing_active_so_make_first_active) {
        slides[0].classList.add('active');   
    }
    */
}

