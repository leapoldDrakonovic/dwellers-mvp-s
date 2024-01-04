const html = document.querySelector('html')
var houseArray = [];
var roomsArray = [];
var languageList = {
    filterHandover: {
        ENG: "Handover",
        HEB: "תפוסה"
    },
    filterRooms: {
        ENG: "Rooms",
        HEB: "חדרים"
    }
}

function buildingsFilteredShow() {
    var building_button = document.getElementById('search1');

    building_button.textContent = '';
    building_button.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-buildings';
    animation.textContent = 'Loading&#8230;';

    building_button.appendChild(animation);

    var metersMinForm = document.getElementById("min-inp-btn").value;
    var metersMaxForm = document.getElementById("max-inp-btn").value;
    var houseClassForm = houseArray;
    houseClassForm.forEach(element => {
        element.replace('+', '')
    })
    // document.getElementById("house-occupancy-inp-btn").value;

    var roomsNumberForm = roomsArray;
    roomsNumberForm.forEach(element => {
        element.replace('+', '')
    })
    // var CashTypeForm = document.getElementById("filter_type_of_cash").textContent;
    var priceMin = document.getElementById("min-price-inp-btn").value;
    var priceMax = document.getElementById("max-price-inp-btn").value;
    var buildingSearchForm = document.getElementById("search-input").value;

    var requestData = {
        "filters": {
            "all_size_m2_min": metersMinForm,
            "all_size_m2_max": metersMaxForm,
            "type_of_building": houseClassForm,
            "rooms": roomsNumberForm,
            // "CashTypeForm": CashTypeForm,
            "price_min": priceMin,
            "price_max": priceMax,
            "name": buildingSearchForm,
        },
        "configs": {
            "responseType": "smallData"
        }
    }
    $.ajax({ 
        url: "/db/tables/ListOfBuildings/get/filtered", 
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",
        success: function(data) {
            document.getElementById("cardblock-title").innerHTML = `
            Filtered
            <button class="clear-filter-btn white-blue-btn" id="clear-filter-btn">Clear Search</button>
            `;
            clearFilter()

            document.getElementById('main-loadmore-btn').style.display = "none";
            var buildingsDiv = document.getElementById("buildings-div");
            while (buildingsDiv.firstChild) {
                buildingsDiv.removeChild(buildingsDiv.firstChild);
            }

            data['data'].forEach(building => {
                // Создание всех элементов застройщика:
                var newBuilding = document.createElement('a');
                newBuilding.id = 'building-object-' + building['id'].toString();
                newBuilding.href = 'building?building_id=' + building['id'].toString();

                var buildingContext = document.createElement('div');
                buildingContext.className = 'card';
                

                var buildingLogo = document.createElement('div');
                buildingLogo.className = 'card-content';

                var logoImg = document.createElement('div');
                logoImg.className = 'card-img';

                try {
                    logoImg.style = 'background-repeat: no-repeat; background-size: cover; background-image: url(/static/assets/' + building['type'].toString() + '/' + building['group_id_for_image'].toString() + '/' + building['file_name'].toString() + ')'   
                } catch (error) {
                    logoImg.style = 'background-repeat: no-repeat; background-size: cover;'
                }

                var buildingInfo = document.createElement('div');
                buildingInfo.className = 'card-text';

                var buildingName = document.createElement('div');
                buildingName.className = 'JKName';
                buildingName.textContent = building['name'].toString(); // УДАЛИТЬ А В HTML
                
                // var buildingPrice = document.createElement('div');
                // buildingPrice.className = 'card-price';
                // buildingPrice.textContent = 'for $' + building['price_range_start'].toString() + 'kk';

                var buildingLocation = document.createElement('div');
                buildingLocation.className = 'card-location';
                buildingLocation.textContent = building['country'].toString() + ', ' + building['city'].toString();

                // Вкладывание элементов:
                buildingInfo.appendChild(buildingName);
                // buildingInfo.appendChild(buildingPrice);
                buildingInfo.appendChild(buildingLocation);

                buildingLogo.appendChild(logoImg);
                buildingLogo.appendChild(buildingInfo);

                buildingContext.appendChild(buildingLogo);

                newBuilding.appendChild(buildingContext);
                
                // Добавление полученного объекта на страницу:
                buildingsDiv.appendChild(newBuilding);
            });
            // Остановка анимации
            var animation = document.getElementById('loading-object-buildings');
            animation.remove();

            var button = document.getElementById('search1');
            button.textContent = 'Search';
            button.disabled = false;
            // Перемещение обзора пользователя на полученный список ЖК:
            document.getElementById('cardblock-title').scrollIntoView({
                behavior: 'smooth',
                block: 'center' // start?
              })
        },
        error: function() {
            alert('error');
        }
    });
}

function clearFilter () {
    var clearBtn = document.querySelector('#clear-filter-btn')

    clearBtn.addEventListener('click', ()=>{
        document.getElementById("cardblock-title").innerHTML = `Buildings`

        document.getElementById("min-inp-btn").value = ''
        document.getElementById("max-inp-btn").value = ''

        document.getElementById("min-price-inp-btn").value = ''
        document.getElementById("max-price-inp-btn").value = ''

        if (html.getAttribute('dir') == 'rtl') {
            document.querySelector("#fbRoom").querySelector('.filter-text').innerHTML = languageList.filterRooms.HEB
            document.querySelector("#fbHouse").querySelector('.filter-text').innerHTML = languageList.filterHandover.HEB
        } else {
            document.querySelector("#fbRoom").querySelector('.filter-text').innerHTML = languageList.filterRooms.ENG
            document.querySelector("#fbHouse").querySelector('.filter-text').innerHTML = languageList.filterHandover.ENG
        }


        let checkboxes = document.querySelectorAll('input[type="checkbox"]')
        checkboxes.forEach(checkbox => {checkbox.checked = false})

        roomsArray = [];
        houseArray = [];

        // var CashTypeForm = document.getElementById("filter_type_of_cash").textContent;

        // For RS reset
        /*
        document.getElementById("range-min").value = document.getElementById("range-min").min 
        document.getElementById("range-max").value = document.getElementById("range-max").max 

        var inputMin = document.querySelectorAll('.input-min')
        var inputMax = document.querySelectorAll('.input-max')

        var fieldMin = document.querySelectorAll('.field-min')
        var fieldMax = document.querySelectorAll('.field-max')

        var ranges = document.querySelectorAll(".slider .progress")

        ranges.forEach(range=> {
            range.style.left = 0;
            range.style.right = 0;
        })


        if (html.getAttribute('dir') == 'rtl') {
            fieldMin.forEach(field => {
                field.style.right = '-5%'
            })
    
            fieldMax.forEach(field=>{
                field.style.right = '95%'
            })
        }

        fieldMin.forEach(field => {
            field.style.left = '-5%'
        })

        fieldMax.forEach(field=>{
            field.style.left = '95%'
        })
        inputMin.forEach(min=> {
            min.value = document.getElementById("range-min").min 
        })

        inputMax.forEach(max=> {
            max.value = document.getElementById("range-max").max 
        })
        */



        document.getElementById("search-input").value = ''

        buildingsFilteredUpdateNumber()

        var requestData = {
            "data": {
                "response_length": 12
            }
        }

        $.ajax({ 
            url: "/db/tables/ListOfBuildings/get/simpled", 
            data: JSON.stringify(requestData),
            contentType: "application/json",
            dataType: 'json',
            method: "POST",
            success: function(data) {
    
                document.getElementById('main-loadmore-btn').style.display = "block";
                var buildingsDiv = document.getElementById("buildings-div");
                while (buildingsDiv.firstChild) {
                    buildingsDiv.removeChild(buildingsDiv.firstChild);
                }
    
                data['data'].forEach(building => {
                    // Создание всех элементов застройщика:
                    var newBuilding = document.createElement('a');
                    newBuilding.id = 'building-object-' + building['id'].toString();
                    newBuilding.href = 'building?building_id=' + building['id'].toString();
    
                    var buildingContext = document.createElement('div');
                    buildingContext.className = 'card';
                    
    
                    var buildingLogo = document.createElement('div');
                    buildingLogo.className = 'card-content';
    
                    var logoImg = document.createElement('div');
                    logoImg.className = 'card-img';
    
                    try {
                        logoImg.style = 'background-repeat: no-repeat; background-size: cover; background-image: url(/static/assets/' + building['type'].toString() + '/' + building['group_id_for_image'].toString() + '/' + building['file_name'].toString() + ')'   
                    } catch (error) {
                        logoImg.style = 'background-repeat: no-repeat; background-size: cover;'
                    }
    
                    var buildingInfo = document.createElement('div');
                    buildingInfo.className = 'card-text';
    
                    var buildingName = document.createElement('div');
                    buildingName.className = 'JKName';
                    buildingName.textContent = building['name'].toString(); // УДАЛИТЬ А В HTML
                    
                    // var buildingPrice = document.createElement('div');
                    // buildingPrice.className = 'card-price';
                    // buildingPrice.textContent = 'for $' + building['price_range_start'].toString() + 'kk';
    
                    var buildingLocation = document.createElement('div');
                    buildingLocation.className = 'card-location';
                    buildingLocation.textContent = building['country'].toString() + ', ' + building['city'].toString();
    
                    // Вкладывание элементов:
                    buildingInfo.appendChild(buildingName);
                    // buildingInfo.appendChild(buildingPrice);
                    buildingInfo.appendChild(buildingLocation);
    
                    buildingLogo.appendChild(logoImg);
                    buildingLogo.appendChild(buildingInfo);
    
                    buildingContext.appendChild(buildingLogo);
    
                    newBuilding.appendChild(buildingContext);
                    
                    // Добавление полученного объекта на страницу:
                    buildingsDiv.appendChild(newBuilding);
                });
            },
            error: function() {
                alert('error');
            }

    })
})
}

function buildingsFilteredUpdateNumber() {


    console.log(houseArray, roomsArray);

    var counter = document.getElementById('search-count-1');
    var text_results = document.getElementById('search-subtitle-1');
    counter.textContent = '';
    counter.disabled = true;
    text_results.textContent = '';
    text_results.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-buildings';
    animation.textContent = 'Loading&#8230;';

    counter.appendChild(animation);

    var metersMinForm = document.getElementById("min-inp-btn").value;
    var metersMaxForm = document.getElementById("max-inp-btn").value;
    var houseClassForm = houseArray;
    houseClassForm.forEach(element => {
        element.replace('+', '')
    })

    var roomsNumberForm = roomsArray;
    roomsNumberForm.forEach(element => {
        element.replace('+', '')
    })
    var CashTypeForm = document.getElementById("filter_type_of_cash").textContent;
    var priceMin = document.getElementById("min-price-inp-btn").value;
    var priceMax = document.getElementById("max-price-inp-btn").value;
    var buildingSearchForm = document.getElementById("search-input").value;
    
    var requestData = {
        "filters": {
            "all_size_m2_min": metersMinForm,
            "all_size_m2_max": metersMaxForm,
            "type_of_building": houseClassForm,
            "rooms": roomsNumberForm,
            // "CashTypeForm": CashTypeForm,
            "price_min": priceMin,
            "price_max": priceMax,
            "name": buildingSearchForm,
        },
        "configs": {
            "responseType": "length"
        }
    }

    // Добавление в ссылку на карту отмеченных фильтров, чтобы пользователь сразу мог перейти на карту с этими фильтрами
    let mapLink = document.getElementById("mainMapLink");
    let mapLinkRequestData = {
        "filters": {
            "all_size_m2_min": metersMinForm,
            "all_size_m2_max": metersMaxForm,
            "type_of_building": houseClassForm,
            "rooms": roomsNumberForm,
            // "CashTypeForm": CashTypeForm,
            "price_min": priceMin,
            "price_max": priceMax,
            "name": buildingSearchForm,
        },
        "configs": {
            "responseType": "fullData"
        }
    }
    mapLink.href = "/map?filters=" + JSON.stringify(mapLinkRequestData);
    $.ajax({ 
        url: "/db/tables/ListOfBuildings/get/filtered",
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",
        success: function(data) {
            // Остановка анимации
            let animation = document.getElementById('loading-object-buildings');
            animation.remove();

            let text_results = document.getElementById('search-subtitle-1');
            text_results.textContent = 'results';
            text_results.disabled = false;

            let counter = document.getElementById("search-count-1");
            counter.innerHTML = `${data["data"]}`;
            counter.disabled = false;
         },
         error: function() {
             alert('error');
        }
    });
}


function buildingsFilteredShowMap() {
    var building_button = document.getElementById('search1');

    building_button.textContent = '';
    building_button.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-buildings';
    animation.textContent = 'Loading&#8230;';

    building_button.appendChild(animation);

    var metersMinForm = document.getElementById("min-inp-btn").value;
    var metersMaxForm = document.getElementById("max-inp-btn").value;
    var houseClassForm = houseArray;
    houseClassForm.forEach(element => {
        element.replace('+', '')
    })
    // document.getElementById("house-occupancy-inp-btn").value;

    var roomsNumberForm = roomsArray;
    roomsNumberForm.forEach(element => {
        element.replace('+', '')
    })
    var CashTypeForm = document.getElementById("filter_type_of_cash").textContent;
    var buildingSearchForm = document.getElementById("search-input").value;

    var price_min = document.querySelector("#min-price-inp-btn").value
    var price_max = document.querySelector("#max-price-inp-btn").value

    var requestData = {
        "filters": {
            "all_size_m2_min": metersMinForm,
            "all_size_m2_max": metersMaxForm,
            "type_of_building": houseClassForm,
            "rooms": roomsNumberForm,
            "price_min": price_min,
            "price_max": price_max,
            // "CashTypeForm": CashTypeForm,
            "name": buildingSearchForm,
        },
        "configs": {
            "responseType": "fullData"
        }
    }

    $.ajax({ 
        url: "/db/tables/ListOfBuildings/get/filtered", 
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",
        success: function(data) {
            var buildingsWrapper = document.getElementById("map-page-results-cards-wrapper");
            while (buildingsWrapper.firstChild) {
                buildingsWrapper.removeChild(buildingsWrapper.firstChild);
            }

            window.deleteMapPoints()
            var mapPoints = [];
            data['data'].forEach(building => {
                // Создание всех элементов застройщика:
                var newBuildingCard = document.createElement('div');
                newBuildingCard.className = "map-page-card";
                newBuildingCard.id = building['id'].toString() + "-page-card"
                newBuildingCard.setAttribute('onclick', "map.flyTo({center: [" + building['coord_y'].toString() + ", " + building['coord_x'].toString() + "],zoom: 15}); for (let object of document.getElementsByClassName('map-page-card')) {object.classList.remove('map-page-card-clicked')}; document.getElementById('" + building['id'].toString() + "-page-card').classList.add('map-page-card-clicked')");

                var newBuildingCardUp = document.createElement('div');
                newBuildingCardUp.className = 'map-page-card-up';

                var mapPageCardImg = document.createElement('div');
                mapPageCardImg.className = 'map-page-card-img';

                try {
                    mapPageCardImg.style = 'background-repeat: no-repeat; background-size: 100% 100%; background-image: url(/static/assets/' + building['type'].toString() + '/' + building['group_id_for_image'].toString() + '/' + building['file_name'].toString() + ')'  
                } catch (error) {
                    mapPageCardImg.style = 'background-repeat: no-repeat; background-size: 100% 100%;'
                }

                var mapPageCardListWrapper = document.createElement('div');
                mapPageCardListWrapper.className = 'map-page-card-list-wrapper';

                var mapPageCardList = document.createElement('ul');
                mapPageCardList.className = 'map-page-card-down';

                var mapPageCardName = document.createElement('div');
                mapPageCardName.className = 'map-page-card-name';

                var newBuildingCardDown = document.createElement('div');
                newBuildingCardDown.className = 'map-page-card-down';
                

                mapPageCardListWrapper.appendChild(newBuildingCardDown);


                for (const [key, flats] of Object.entries(building['grouped_flats'])) {
                    var mapPageCardListElement = document.createElement('div');
                    mapPageCardListElement.className = 'map-page-card-list-element';


                    var mapPageCardListElementName = document.createElement('div');
                    mapPageCardListElementName.className = 'map-page-card-list-element-name';
                    if (key == 0) {
                        mapPageCardListElementName.textContent = 'studios';
                    }
                    else {
                        mapPageCardListElementName.textContent = key.toString() + '-rooms';
                    }
                    var mapPageCardListElementM2Price = document.createElement('div');
                    mapPageCardListElementM2Price.className = 'map-page-card-list-element-price';
                    mapPageCardListElementM2Price.textContent = 'for ' + flats[0]['min_m2_value'].toString() + ' m²';

                    var mapPageCardListElementPrice = document.createElement('div');
                    mapPageCardListElementPrice.className = 'map-page-card-list-element-plan';
                    mapPageCardListElementPrice.innerHTML = 'for $' + `<span class="price">${flats[0]['min_price_value']}</span>`;

                    function formatPrices() {
                        const priceElements = document.querySelectorAll('.price');
                      
                        priceElements.forEach((element) => {
                          const priceString = element.textContent.trim();
                          const priceNumber = parseFloat(priceString.replace(/\s/g, '')); // Удаляем пробелы из строки и преобразуем в число
                      
                          if (!isNaN(priceNumber)) {
                            const formattedPrice = priceNumber.toLocaleString(); // Форматируем число с разделителем тысяч
                            element.textContent = formattedPrice;
                          }
                        });
                    }

                    formatPrices()

                    mapPageCardListElement.appendChild(mapPageCardListElementName);
                    mapPageCardListElement.appendChild(mapPageCardListElementM2Price);
                    mapPageCardListElement.appendChild(mapPageCardListElementPrice);
                    mapPageCardListWrapper.appendChild(mapPageCardListElement);
                  }


                var newBuildingCardName = document.createElement('div');
                newBuildingCardName.className = 'map-page-card-name';
                var newBuildingCardNameHref = document.createElement('a');
                newBuildingCardNameHref.href = '/building?building_id=' + building['id'].toString();
                newBuildingCardNameHref.target = '_blank';
                newBuildingCardNameHref.textContent = building.name;

                var newBuildingCardPrice = document.createElement('div');
                newBuildingCardPrice.className = 'map-page-card-price';
                // newBuildingCardPrice.textContent = 'for $' + building['price_range_start'].toString() + 'kk';

                var newBuildingCardLocation = document.createElement('div');
                newBuildingCardLocation.className = 'map-page-card-location';
                newBuildingCardLocation.textContent = building['country'] + ', ' + building['city'];

                newBuildingCardName.appendChild(newBuildingCardNameHref);

                newBuildingCardDown.appendChild(newBuildingCardName);
                newBuildingCardDown.appendChild(newBuildingCardPrice);
                newBuildingCardDown.appendChild(newBuildingCardLocation);

                mapPageCardListWrapper.appendChild(mapPageCardList);

                newBuildingCardUp.appendChild(mapPageCardImg);
                newBuildingCard.appendChild(newBuildingCardUp);

                newBuildingCardUp.appendChild(mapPageCardListWrapper);


                buildingsWrapper.append(newBuildingCard);
                
                mapPoints.push([
                    building['coord_x'],
                    building['coord_y'],
                    building['id'],
                    building['name'],
                    building['country'],
                    building['city']
                ]);

            });

            window.addMapPoints(mapPoints);

            // Остановка анимации
            var animation = document.getElementById('loading-object-buildings');
            animation.remove();

            var button = document.getElementById('search1');
            button.innerHTML = `
            <img src="/static/assets/UIsvgs/search_icon.svg" alt="">
            `;
            button.disabled = false;
        },
        error: function() {
            alert('error');
        }
    });
}

// Search input request listener

var searchFilterInputs = document.querySelectorAll('.search-input')
searchFilterInputs.forEach(input=>{
    input.addEventListener('change', buildingsFilteredUpdateNumber)
})

// Range Slider request listener
// Оставьте пока может для расширения

/*
var rangeSliders = document.querySelectorAll('.rangeslider-container')
rangeSliders.forEach(rs=> {
    var rangeMin = rs.querySelectorAll('input[type="range"]')[0]
    var rangeMax = rs.querySelectorAll('input[type="range"]')[1]
    rangeMin.addEventListener('change', buildingsFilteredUpdateNumber)
    rangeMax.addEventListener('change', buildingsFilteredUpdateNumber)
})
*/ 

// MAIN FILTER BTNS POPUP CHOOSE LIST
var filterBtnWrappers = document.querySelectorAll('.filter-button-wrapper')

filterBtnWrappers.forEach( filterWrapper => {
    var filterBtn = filterWrapper.querySelector('.filter-button')
    var filterList = filterWrapper.querySelector('.btn-list')
    var filterText = filterWrapper.querySelector('.filter-text')
    var dataInput = filterWrapper.querySelector('.filter-btn-inp')

    var inpList = filterWrapper.querySelector('.btn-list-inp.m2-inp')
    var m2Inp = filterWrapper.querySelectorAll('.inp-filter')
    var minInp = filterWrapper.querySelector('#min-inp-btn')
    var maxInp = filterWrapper.querySelector('#max-inp-btn')
    var priceInpList = filterWrapper.querySelector('.btn-list-inp.price-inp') //Price inp list
    var priceInpMin = filterWrapper.querySelector('#min-price-inp-btn') //Price inp's
    var priceInpMax = filterWrapper.querySelector('#max-price-inp-btn') //Price inp's

// Под м2
    if (!!inpList) {
            filterBtn.addEventListener('click', (event)=> {
            event.stopPropagation()
            inpList.classList.toggle('visible')
        })

        inpList.addEventListener('click', (event)=> {
            event.stopPropagation()
        })

         // Получение значений инпутов        
        minInp.addEventListener('change', ()=>{
            buildingsFilteredUpdateNumber()
        })
        maxInp.addEventListener('change', ()=>{
            buildingsFilteredUpdateNumber()
        })

        minInp.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        maxInp.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        
         // Очистка инпутов
         var clearBtnM2 = filterWrapper.querySelector('#filter-btn-clear')
         clearBtnM2.addEventListener('click', (event)=> {
            event.preventDefault() 
            m2Inp.forEach(input=> {
                input.value = ''
                buildingsFilteredUpdateNumber()
                })
         })

        document.addEventListener('click', (event) => {
            if(event.target !== filterBtn) {
                inpList.classList.remove('visible')
            }
        })

        return
    }

    // Функционал для цены
    if (!!priceInpList) {

        filterBtn.addEventListener('click', (event)=> {
            event.stopPropagation()
            priceInpList.classList.toggle('visible')
        })

        priceInpList.addEventListener('click', (event)=> {
            event.stopPropagation()
        })

         // Получение значений инпутов        
        priceInpMin.addEventListener('change', ()=>{
            buildingsFilteredUpdateNumber()
        })
        priceInpMax.addEventListener('change', ()=>{
            buildingsFilteredUpdateNumber()
        })

        priceInpMin.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        priceInpMax.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })

        var clearBtnPrice = filterWrapper.querySelector('#filter-btn-clear-price')
        clearBtnPrice.addEventListener('click', (event)=> {
            event.preventDefault()
            priceInpMax.value = ''
            priceInpMin.value = ''
            buildingsFilteredUpdateNumber()
        })

       document.addEventListener('click', (event) => {
           if(event.target !== filterBtn) {
                priceInpList.classList.remove('visible')
           }
       })

       return
    }

    filterBtn.addEventListener('click', (event)=> {
        event.stopPropagation()
        filterList.classList.toggle('visible')
    })

    // Функционал для чекбоксов
    var filterListItems = filterWrapper.querySelectorAll('.btn-item')
    var checkboxArray = new Array()

    filterListItems.forEach(listItem=>{
        listItem.addEventListener('click', (event)=> {
            event.stopPropagation()

            // Clear function
            if (listItem.dataset.value === 'clear' || listItem.dataset.value === 'all') {
                let checkboxes = filterWrapper.querySelectorAll('input[type="checkbox"]')
                checkboxes.forEach(checkbox => {checkbox.checked = false})
                filterText.innerText = filterText.dataset.value
                dataInput.value = ''
                filterList.classList.remove('visible')
                checkboxArray = []
                if (listItem.dataset.value === 'clear') {
                    roomsArray = []
                } else if (listItem.dataset.value === 'all') {
                    houseArray = []
                }

                buildingsFilteredUpdateNumber()
                return
            }

            // Checkbox choose funct
            
            var checkbox = listItem.querySelector('input[type="checkbox"]')
            let isChecked = checkbox.checked
            checkbox.checked = !isChecked
            if (!isChecked) {
                if (!checkboxArray.includes(checkbox.value)) {
                    checkboxArray.push(checkbox.value)
                } 
            } else {
                let index = checkboxArray.indexOf(checkbox.value)
                    if (index !==-1) {
                        checkboxArray.splice(index, 1);
                    }
            }

            if (html.getAttribute('dir') == 'rtl') {
                filterText.innerHTML = 'אפשרויות' + ' ' + `${checkboxArray.length}`  
            } else {
                filterText.innerHTML = `${checkboxArray.length}` + ` ` +'Opt.'
            }

            // Сделать таргет ивента для определения какой массив отправлять


            if (listItem.parentNode.id == 'dropdownRoom') {
                roomsArray = checkboxArray
            } else if (listItem.parentNode.id == 'dropdownHouse') {
                houseArray = checkboxArray
            }

            if (houseArray.length === 0 && listItem.parentNode.id == 'dropdownHouse') {
                filterText.innerText = filterText.dataset.value                
            }

            if (roomsArray.length === 0 && listItem.parentNode.id == 'dropdownRoom') {
                filterText.innerText = filterText.dataset.value
            }

            buildingsFilteredUpdateNumber()

            // Оставить если будет функиця выбора валюты
            /*
            if (filterBtn.id == 'fbUsd') {
                var moneyIconURL = {
                    _USD: `{{ url_for('static', filename='assets/UIsvgs/DollarSvg.svg') }}`,
                    _EUR: `'{{ url_for('static', filename='assets/UIsvgs/EuroSvg.svg') }}'`,
                    _SHE: `{{ url_for('static', filename='assets/UIsvgs/ShekSvg.svg') }}`,
                    USD: `/static/assets/UIsvgs/DollarSvg.svg`,
                    EUR: `/static/assets/UIsvgs/EuroSvg.svg`,
                    SHE: `/static/assets/UIsvgs/ShekSvg.svg`,
                }
    
                var moneyIconElement = filterBtn.children[0]
    
                switch (listItem.dataset.value) {
                    case `USD`:
                        moneyIconElement.src = moneyIconURL.USD
                        break;
                    
                    case `EUR`:
                        moneyIconElement.src = moneyIconURL.EUR
                        break;
    
                    case `SHE`:
                        moneyIconElement.src = moneyIconURL.SHE
                        break;
                
                    default:
                        moneyIconElement.src = moneyIconURL.USD
                        break;
                }
            }
            */
        })
    })

    document.addEventListener('click', (event) => {
        if(event.target !== filterBtn) {
            filterList.classList.remove('visible')
        }
    })

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Tab' || event.key === 'Escape') {
            filterList.classList.remove('visible')
        }
    })

})
// <========================

// MAP FILTER BTNS POPUP CHOOSE LIST
var mapFilterBtnWrappers = document.querySelectorAll('.map-filter-button-wrapper')

mapFilterBtnWrappers.forEach( filterWrapper => {
    var filterBtn = filterWrapper.querySelector('.filter-button')
    var filterList = filterWrapper.querySelector('.btn-list')
    var filterText = filterWrapper.querySelector('.filter-text')
    var dataInput = filterWrapper.querySelector('.filter-btn-inp')

    var inpList = filterWrapper.querySelector('.btn-list-inp.m2-inp')
    var m2Inp = filterWrapper.querySelectorAll('.inp-filter')
    var minInp = filterWrapper.querySelector('#min-inp-btn')
    var maxInp = filterWrapper.querySelector('#max-inp-btn')
    var priceInpList = filterWrapper.querySelector('.btn-list-inp.price-inp') //Price inp list
    var priceInpMin = filterWrapper.querySelector('#min-price-inp-btn') //Price inp's
    var priceInpMax = filterWrapper.querySelector('#max-price-inp-btn') //Price inp's

// Под м2
    if (!!inpList) {
            filterBtn.addEventListener('click', (event)=> {
            event.stopPropagation()
            inpList.classList.toggle('visible')
        })

        inpList.addEventListener('click', (event)=> {
            event.stopPropagation()
        })


        minInp.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        maxInp.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        
         // Очистка инпутов
         var clearBtnM2 = filterWrapper.querySelector('#filter-btn-clear')
         clearBtnM2.addEventListener('click', (event)=> {
            event.preventDefault() 
            m2Inp.forEach(input=> {
                input.value = ''
                })
         })

        document.addEventListener('click', (event) => {
            if(event.target !== filterBtn) {
                inpList.classList.remove('visible')
            }
        })

        return
    }


    // Функционал для цены
    if (!!priceInpList) {

        filterBtn.addEventListener('click', (event)=> {
            event.stopPropagation()
            priceInpList.classList.toggle('visible')
        })

        priceInpList.addEventListener('click', (event)=> {
            event.stopPropagation()
        })

        priceInpMin.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })
        priceInpMax.addEventListener('input', (event)=>{
            const input = event.target;
            input.value = input.value.replace(/\D/g, '');
        })

        var clearBtnPrice = filterWrapper.querySelector('#filter-btn-clear-price')
        clearBtnPrice.addEventListener('click', (event)=> {
            event.preventDefault()
            priceInpMax.value = ''
            priceInpMin.value = ''
        })

       document.addEventListener('click', (event) => {
           if(event.target !== filterBtn) {
                priceInpList.classList.remove('visible')
           }
       })

       return
    }

    filterBtn.addEventListener('click', (event)=> {
        event.stopPropagation()
        filterList.classList.toggle('visible')
    })

    // Функционал для чекбоксов
    var filterListItems = filterWrapper.querySelectorAll('.btn-item')
    var checkboxArray = new Array()

    filterListItems.forEach(listItem=>{
        listItem.addEventListener('click', (event)=> {
            event.stopPropagation()

            // Clear function
            if (listItem.dataset.value === 'clear' || listItem.dataset.value === 'all') {
                let checkboxes = filterWrapper.querySelectorAll('input[type="checkbox"]')
                checkboxes.forEach(checkbox => {checkbox.checked = false})
                filterText.innerText = filterText.dataset.value
                dataInput.value = ''
                filterList.classList.remove('visible')
                checkboxArray = []
                if (listItem.dataset.value === 'clear') {
                    roomsArray = []
                } else if (listItem.dataset.value === 'all') {
                    houseArray = []
                }

                
                return
            }

            // Checkbox choose funct
            
            var checkbox = listItem.querySelector('input[type="checkbox"]')
            let isChecked = checkbox.checked
            checkbox.checked = !isChecked
            if (!isChecked) {
                if (!checkboxArray.includes(checkbox.value)) {
                    checkboxArray.push(checkbox.value)
                } 
            } else {
                let index = checkboxArray.indexOf(checkbox.value)
                    if (index !==-1) {
                        checkboxArray.splice(index, 1);
                    }
            }

            if (checkboxArray.length == -1) {
                filterText.innerHTML = filterText.dataset.value
            }


            if (html.getAttribute('dir') == 'rtl') {
                filterText.innerHTML = 'אפשרויות' + ' ' + `${checkboxArray.length}`  
            } else {
                filterText.innerHTML = `${checkboxArray.length}` + ` ` +'Opt.'
            }

            // Сделать таргет ивента для определения какой массив отправлять
            
            if (listItem.parentNode.id == 'dropdownRoom') {
                roomsArray = checkboxArray
            } else if (listItem.parentNode.id == 'dropdownHouse') {
                houseArray = checkboxArray
            }

            if (houseArray.length === 0 && listItem.parentNode.id == 'dropdownHouse') {
                filterText.innerText = filterText.dataset.value                
            }

            if (roomsArray.length === 0 && listItem.parentNode.id == 'dropdownRoom') {
                filterText.innerText = filterText.dataset.value
                
            }

            // dataInput.value = listItem.dataset.value
            
            // Оставить если будет функиця выбора валюты
            /*
            if (filterBtn.id == 'fbUsd') {
                var moneyIconURL = {
                    _USD: `{{ url_for('static', filename='assets/UIsvgs/DollarSvg.svg') }}`,
                    _EUR: `'{{ url_for('static', filename='assets/UIsvgs/EuroSvg.svg') }}'`,
                    _SHE: `{{ url_for('static', filename='assets/UIsvgs/ShekSvg.svg') }}`,
                    USD: `/static/assets/UIsvgs/DollarSvg.svg`,
                    EUR: `/static/assets/UIsvgs/EuroSvg.svg`,
                    SHE: `/static/assets/UIsvgs/ShekSvg.svg`,
                }
    
                var moneyIconElement = filterBtn.children[0]
    
                switch (listItem.dataset.value) {
                    case `USD`:
                        moneyIconElement.src = moneyIconURL.USD
                        break;
                    
                    case `EUR`:
                        moneyIconElement.src = moneyIconURL.EUR
                        break;
    
                    case `SHE`:
                        moneyIconElement.src = moneyIconURL.SHE
                        break;
                
                    default:
                        moneyIconElement.src = moneyIconURL.USD
                        break;
                }
            }
            */
        })
    })

    document.addEventListener('click', (event) => {
        if(event.target !== filterBtn) {
            filterList.classList.remove('visible')
        }
    })

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Tab' || event.key === 'Escape') {
            filterList.classList.remove('visible')
        }
    })

})

function validateInput() {
    const inputField = this;
    const isValid = inputField.checkValidity();
  
    if (!isValid) {
      // Если введенное значение не соответствует шаблону, очистить поле ввода
      inputField.value = '';
    }
  }
