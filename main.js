function loadProducts(category, keyword='', page=1, suppliers='') {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.getElementById("container").innerHTML = xhr.responseText;
        }
    };
    xhr.open("GET", "loadProducts.php?category=" + encodeURIComponent(category) + "&keyword=" + encodeURIComponent(keyword) + "&page=" + page + "&suppliers=" + encodeURIComponent(suppliers) , true);
    xhr.send();
}

/* Filter supplier*/

document.addEventListener('DOMContentLoaded', function() {
    const checkboxes = document.querySelectorAll('.filterSupplier');
    let checkedBoxes = [];

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function(event) {
            if (event.target.checked) {
                
                checkedBoxes.push(checkbox.id);
            } else {
                
                checkedBoxes = checkedBoxes.filter(id => id !== checkbox.id);
            }

            var keyword = document.getElementById("search-input").value.trim();
            keyword = keyword.replace(/["';]/g, '');

            cat = window.location.hash.slice(1);

            suppliers = ""
            if (checkedBoxes.length != 0){
                suppliers = checkedBoxes.join(','); 
                loadProducts(cat,keyword,undefined,suppliers);
                
            }else{
                
                loadProducts(cat,keyword);
                
            } 

        });
        
    });

    /* Reset checkboxes */

    const listItems = document.querySelectorAll('#nav li');
    listItems.forEach((li) => {
        li.addEventListener('click', function() {
            const checkboxes = document.querySelectorAll('.filterSupplier');
            checkboxes.forEach((checkbox) => {
                checkbox.checked = false;
            });
            checkedBoxes = [];
            document.getElementById("search-input").value = ''
        });
    });

});


/* Search */
function searchProducts(category){
    var checkboxes = document.querySelectorAll('input[type="checkbox"]');
    var checkedID = [];
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checkedID.push(checkbox.id);
        }
    });

    var keyword = document.getElementById("search-input").value.trim();
    keyword = keyword.replace(/["';]/g, '');

    if (checkedID.length != 0){
        var suppliers = checkedID.join(',');

        loadProducts(category.slice(1), keyword,undefined,suppliers); 
    }else{
        loadProducts(category.slice(1), keyword); 
    }

   
}

/* Pagination */
function changePage(category, keyword, page, supps) {
    loadProducts(category, keyword, page, supps);
}

/* Initial Configuratoins */
if (window.location.hash == ''){
    document.getElementById("load").click();
}else {
    loadProducts(window.location.hash.slice(1));
}


/* Filter discount TO:DO*/
