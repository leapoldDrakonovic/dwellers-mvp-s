var rsWrappers = document.querySelectorAll('.rs-wrapper')

rsWrappers.forEach(rs => {
const rangeInput = rs.querySelectorAll(".range-input input"),
    priceInput = rs.querySelectorAll(".field input"),
    range = rs.querySelector(".slider .progress"),
    fieldMin = rs.querySelector('.field-min'),
    fieldMax = rs.querySelector('.field-max');

let priceGap = 1;

range.style.left = 0;
range.style.right = 0;

priceInput[0].value = document.getElementById('range-min').value;
priceInput[1].value = document.getElementById('range-max').value;

fieldMax.style.right = 95 + '%';
fieldMin.style.right = -5 + '%';

priceInput.forEach(input =>{
    input.addEventListener("input", e => {
        let minPrice = parseInt(priceInput[0].value),
        maxPrice = parseInt(priceInput[1].value);



        
        if((maxPrice - minPrice >= priceGap) && maxPrice <= rangeInput[1].max){
            if(e.target.className === "input-min"){
                rangeInput[0].value = minPrice;
                range.style.right = ((minPrice / rangeInput[0].max) * 100) + "%";
    
            }else{
                rangeInput[1].value = maxPrice;
                range.style.left = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
               
            }
        }
        
        
        
    });
});

rangeInput.forEach(input =>{
    input.addEventListener("input", e =>{
        let minVal = parseInt(rangeInput[0].value),
        maxVal = parseInt(rangeInput[1].value);

       
        if((maxVal - minVal) < priceGap){
            if(e.target.className === "range-min"){
                rangeInput[0].value = maxVal - priceGap
            }else{
                rangeInput[1].value = minVal + priceGap;
            }
        }else{
            priceInput[0].value = minVal;
            priceInput[1].value = maxVal;
            range.style.right = ((minVal / rangeInput[0].max) * 100) + "%";
            range.style.left = 100 - (maxVal / rangeInput[1].max) * 100 + "%";

            fieldMax.style.right = ((maxVal / rangeInput[1].max)) * 100-5 + '%';
            fieldMin.style.right = ((minVal / rangeInput[0].max) * 100-5) + "%";
            

            
        }

    });
});
})




// async (event) => {
//     try {
//         await fetch('', {
//             method: 'POST',
//             headers: {
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify()
//         })
//     } catch (error) {
//         console.error(error);
//     }
// }