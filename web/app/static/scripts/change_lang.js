const changeLangBtnWrapper = document.querySelectorAll('.language-button-wrapper')

changeLangBtnWrapper.forEach(wrapper=>{

  var langBtn = wrapper.querySelector('.language-button')
  var langList = wrapper.querySelector('.btn-list')
  var langImg = wrapper.querySelector('#language-img')
  const langListItems = wrapper.querySelectorAll('.btn-item')
  
  
  langBtn.addEventListener('click', chooseLanguage)
  langList.addEventListener('click', (event) => {
      const langItem = event.target.closest('.btn-item');
      if (langItem) {
        let language = langItem.dataset.value;
        switch (language) {
          case 'EN':
            setLanguage(language);
            break;
    
          case 'HE':
            setLanguage(language);
            break;
        }
    
        langList.classList.remove('visible');
      }
    });
  
  
  function chooseLanguage (event) {
      event.stopPropagation()
      langList.classList.toggle('visible')
  
  }
})


function setLanguage (language) {
    let currentURL = window.location.href
    $.ajax({ 
        url: `/lang/update/${language}`,
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify({"fromUrl": currentURL}),
        success: function() {
            location.href = currentURL;
        },
        error: function() {
            alert('error');
        }
    });
}

