const callbackButton = document.querySelector('#callback-btn')
callbackButton.addEventListener('click', showCallbackWindow)

function showCallbackWindow () {
    const modalWin = document.querySelector('.modal.modal-callback')
    const body = document.getElementsByTagName('body')[0];
    var inputs = modalWin.querySelectorAll('input')

    modalWin.style.display = 'block'
    body.style.overflow = 'hidden';
    body.style.pointerEvents = 'none';
    modalWin.style.pointerEvents = 'all';

    const closeBtn = modalWin.querySelector('#modal-callback-x')
    closeBtn.addEventListener('click', ()=> {
        body.style.overflow = 'auto';
        body.style.pointerEvents = 'all';
        modalWin.style.display = 'none'

        inputs.forEach(input=> {
            input.style.border = ''
        })
    })



    window.addEventListener("click", (e) => {
        const modals = document.querySelector(".modal-callback")
        if (e.target == modals){
            body.style.overflow = 'auto';
            body.style.pointerEvents = 'all';
            modalWin.style.display = 'none'
        }
    })
}

function sendCallBackMail() {
    // Для начала сделать проверку на то, все ли данные введены
    // Если хотя бы одно поле не заполнено, выделяем его и оповещаем пользователя о том, что данных не хватает


    const modalWin = document.querySelector('.modal.modal-callback')
    const body = document.getElementsByTagName('body')[0];
    var inputs = modalWin.querySelectorAll('input')
    var descriptionValue = modalWin.querySelector('#callback-description')

    var isValid = true
    inputs.forEach(input=> {
        if (input.value == '') {
            input.style.border = '1px solid red'
            isValid = false
        } else {
            input.style.border = ''
        }
    })


        if (isValid) {
            body.style.overflow = 'auto';
            body.style.pointerEvents = 'all';
            modalWin.style.display = 'none'

            var modalSuc = document.createElement('div')
            modalSuc.className = 'modal modal-callback-success'
            modalSuc.style.display = 'block'

            var htmlDir = document.querySelector('html').getAttribute('dir')

            var requestData = {
                "data": {
                    "email": document.getElementById("email-input").value,
                    "number": document.getElementById("number-input").value,
                    "name": document.getElementById("name-input").value,
                    "surname": document.getElementById("surname-input").value,
                    // 'description': description.value,
                    "building_id": document.getElementById("building-id-value").value,
                },
                "destination": {
                    "builder_id": document.getElementById("builder-id-value").value,
                }
            }


            $.ajax({ 
                url: "/actions/mail/send",
                data: JSON.stringify(requestData),
                contentType: "application/json",
                dataType: 'json',
                method: "POST",
                success: function(data) {
        
                    if (data['state']) {

                        switch (htmlDir) {
                            case 'rtl':
                                modalSuc.innerHTML = `
                                <div class="modal-callback-success-wrapper">
                                    <div class="succsess-text">
                                        בקשתך הצליחה. דוא"ל נשלח למפתח
                                    </div>
                                </div>
                                `
                                break;
                        
                            default:
                                modalSuc.innerHTML = `
                                <div class="modal-callback-success-wrapper">
                                    <div class="succsess-text">
                                        Your request was successful. Email sent to developer!
                                    </div>
                                </div>
                                `
                                break;
                        }

                    }
                    else {
                                modalSuc.innerHTML = `
                                <div class="modal-callback-success-wrapper">
                                    <div class="succsess-text">
                                       Something went wrong and we are already working on resolving the issue. Please try again later!
                                    </div>
                                </div>
                            `
                    }
        
                    body.appendChild(modalSuc)
                        setTimeout(()=>{
                        modalSuc.remove()
                        },
                    3000)
                    // Условия, для того чтобы понять, было ли отправлено письмо
        
                    // Действия на стороне фронта
                    
            },
            error: function() {
                alert('error');
            }
        });
        
        }

}
