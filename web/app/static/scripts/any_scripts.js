function buildersShowMore(){
    var builder_button = document.getElementById('builders-show-more-button');

    builder_button.textContent = '';
    builder_button.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-builders';
    animation.textContent = 'Loading&#8230;';

    builder_button.appendChild(animation);

    var buildersDiv = document.getElementById('builders-div');
    var buildersDivObjects = buildersDiv.children;

    var requestData = {"builders_ids": [], "response_length": 7, "same_builder": [false, false]};

    for (var i = 0; i < buildersDivObjects.length; i++) {
        requestData['builders_ids'].push(buildersDivObjects[i].id.split('-')[2])
    }

    $.ajax({ 
        url: "/db/tables/ListOfBuilders/get", 
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",

       	success: function(data) {
            data['data'].forEach(builder => {
                // Создание всех элементов застройщика:
                var newBuilder = document.createElement('a');
                newBuilder.id = 'builder-object-' + builder['id'].toString();
                newBuilder.href = 'builder?builder_id=' + builder['id'].toString();

                var builderContext = document.createElement('div');
                builderContext.className = 'builder-context';

                var builderLogo = document.createElement('div');
                builderLogo.className = 'builder-logo';

                var logoImg = document.createElement('img');
                try {
                    logoImg.src = '/static/assets/' + builder['type'].toString() + '/' + builder['group_id'].toString() + '/' + builder['file_name'].toString();
                } catch (error) {
                    
                }

                var builderInfo = document.createElement('div');
                builderInfo.className = 'builder-info';

                var builderName = document.createElement('div');
                builderName.className = 'bi-name';
                builderName.textContent = builder['name'].toString();

                // var builderPrice = document.createElement('div');
                // builderPrice.className = 'bi-price';
                // builderPrice.textContent = 'for $' + builder['price_range_start'].toString() + 'kk min';

                // Вкладывание элементов:
                builderLogo.appendChild(logoImg);
                
                builderInfo.appendChild(builderName);
                // builderInfo.appendChild(builderPrice);

                builderContext.appendChild(builderLogo);
                builderContext.appendChild(builderInfo);

                newBuilder.appendChild(builderContext);
                
                // Добавление полученного объекта на страницу:
                buildersDiv.appendChild(newBuilder);
            });

            var animation = document.getElementById('loading-object-builders');
            animation.remove();

            var button = document.getElementById('builders-show-more-button');
            button.textContent = 'Load more';

            button.disabled = false;

            if (data['buttons_off']) {
                button.style.display = 'none';
            }
        },
        error: function() {
            alert('error');
        }
    });
}

function buildingsShowMore(){
    var building_button = document.getElementById('main-loadmore-btn');

    building_button.textContent = '';
    building_button.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-buildings';
    animation.textContent = 'Loading&#8230;';

    building_button.appendChild(animation);

    var buildingsDiv = document.getElementById('buildings-div');
    var buildingsDivObjects = buildingsDiv.children;

    var requestData = {"buildings_ids": [], "response_length": 9, "same_builder": [false, false]};

    for (var i = 0; i < buildingsDivObjects.length; i++) {
        if (buildingsDivObjects[i].tagName == 'A') {
            requestData['buildings_ids'].push(buildingsDivObjects[i].id.split('-')[2])
        }
    }

    $.ajax({ 
        url: "/db/tables/ListOfBuildings/get", 
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",
        success: function(data) {
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

            var animation = document.getElementById('loading-object-buildings');
            animation.remove();

            var button = document.getElementById('main-loadmore-btn');
            button.textContent = 'Load more';
            button.disabled = false;

            if (data['buttons_off']) {
                button.style.display = 'none';
            }
        },
        error: function() {
            alert('error');
        }
    });
}

function buildingsSameBuilderShowMore(){
    var building_button = document.getElementById('builders-loadmore-buildings-btn');

    building_button.textContent = '';
    building_button.disabled = true;
    
    var animation = document.createElement('div');
    animation.className = 'loading';
    animation.id = 'loading-object-new-buildings';
    animation.textContent = 'Loading&#8230;';

    building_button.appendChild(animation);

    var buildingsDiv = document.getElementById('builder-buildings');
    var buildingsDivObjects = buildingsDiv.children;

    var requestData = {"buildings_ids": [], "response_length": 3, "same_builder": [true, parseInt(buildingsDivObjects[0].id.split('-')[1])]};

    for (var i = 0; i < buildingsDivObjects.length; i++) {
        if (buildingsDivObjects[i].tagName == 'A') {
            requestData['buildings_ids'].push(buildingsDivObjects[i].id.split('-')[3])
        }
    }

    $.ajax({ 
        url: "/db/tables/ListOfBuildings/get", 
        data: JSON.stringify(requestData),
        contentType: "application/json",
        dataType: 'json',
        method: "POST",
        success: function(data) {
            data['data'].forEach(building => {
                // Создание всех элементов застройщика:
                var newBuilding = document.createElement('a');
                newBuilding.id = 'builder-' + building['group_id'] + 'object-' + building['id'].toString();
                newBuilding.href = 'building?building_id=' + building['id'].toString();

                var builderPageCard = document.createElement('div');
                builderPageCard.className = 'builder-page-card'

                var builderPageCardImgContainer = document.createElement('div');
                builderPageCardImgContainer.className = 'builder-page-card-img';

                builderPageCard.appendChild(builderPageCardImgContainer);

                var builderPageCardImage = document.createElement('img');
                try {
                    builderPageCardImage.src = "/static/assets/" + building['type'].toString() + '/' + building['group_id_for_image'].toString() + '/' + building['file_name'].toString();
                } catch (error) {
                    
                }

                builderPageCardImgContainer.appendChild(builderPageCardImage);

                var builderPageCardTextContent = document.createElement('div');
                builderPageCardTextContent.className = 'builder-page-card-textcontent';

                var builderPageCardTitle = document.createElement('div');
                builderPageCardTitle.className = 'builder-page-card-title';
                builderPageCardTitle.textContent = building['name'];

                var builderPageCardAdress = document.createElement('div');
                builderPageCardAdress.className = 'builder-page-card-adress';
                builderPageCardAdress.textContent = building['address'];

                var builderPageCardFlatlist = document.createElement('div');
                builderPageCardFlatlist.className = 'builder-page-card-flatlist';

                for (const [key, flats] of Object.entries(building['grouped_flats'])) {
                    var cardFlatlistObject = document.createElement('div');
                    cardFlatlistObject.className = 'card-flatlist-object';

                    var cardFlatlistTitle = document.createElement('div');
                    cardFlatlistTitle.className = 'card-flatlist-title';
                    if (key == 0) {
                        cardFlatlistTitle.textContent = 'studios';
                    }
                    else {
                        cardFlatlistTitle.textContent = key.toString() + '-rooms';
                    }
                    var cardFlatlistSquare = document.createElement('div');
                    cardFlatlistSquare.className = 'card-flatlist-square';
                    cardFlatlistSquare.textContent = 'for ' + flats[0]['min_m2_value'].toString() + ' m²';

                    var cardFlatlistPrice = document.createElement('div');
                    cardFlatlistPrice.className = 'card-flatlist-price';
                    cardFlatlistPrice.textContent = 'for $' + flats[0]['min_price_value'];

                    cardFlatlistObject.appendChild(cardFlatlistTitle);
                    cardFlatlistObject.appendChild(cardFlatlistSquare);
                    cardFlatlistObject.appendChild(cardFlatlistPrice);

                    builderPageCardFlatlist.appendChild(cardFlatlistObject);
                }

                builderPageCardTextContent.appendChild(builderPageCardTitle);
                builderPageCardTextContent.appendChild(builderPageCardAdress);
                builderPageCardTextContent.appendChild(builderPageCardFlatlist);

                builderPageCard.appendChild(builderPageCardImgContainer);
                builderPageCard.appendChild(builderPageCardTextContent);

                newBuilding.appendChild(builderPageCard);

                buildingsDiv.appendChild(newBuilding);
            });

            var animation = document.getElementById('loading-object-new-buildings');
            animation.remove();

            var button = document.getElementById('builders-loadmore-buildings-btn');
            button.textContent = 'Load more';
            button.disabled = false;

            if (data['buttons_off']) {
                button.style.display = 'none';
            }
        },
        error: function() {
            alert('error');
        }
    });
}
