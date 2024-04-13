
document.querySelector("#add-name").addEventListener('click',function(){
    var modal = document.querySelector("#productModal");
    if(modal){
        modal.classList.add('active');
        modal.style.display="none"
        modal.style.display="block"
        
    }


})


document.querySelector(".close").addEventListener('click', function() {
    var modal = document.querySelector("#productModal");
    if (modal) {
        modal.classList.remove('active');
        modal.style.display = "none"; 
    }
});



function searchProducts() {
    
    var searchQuery = document.getElementById("searchProductField").value.trim();

    if (searchQuery.length === 0) {
        
        document.getElementById("productList").innerHTML = "";
        return;
    }

    

    
    fetch(`search-product/?query=${searchQuery}`)
        .then(response => response.json())
        .then(data => {
            
            var productListHtml = "";
            data.forEach(product => {
                productListHtml += `
                    <div class="form-check">
                        <input class="form-check-input" type="radio" name="selectedProduct" value="${product.id}" id="product_${product.id}">
                        <label class="form-check-label" for="product_${product.id}">
                            ${product.name}
                        </label>
                    </div>
                `;
            });

            
            document.getElementById("productList").innerHTML = productListHtml;
        })
        .catch(error => {
            console.error('Error fetching products:', error);
        });

        
}


document.getElementById("searchProductField").addEventListener('input', searchProducts);



function populateFormFields(productName, productCategory) {
    document.getElementById("add-name").value = productName;
    document.getElementById("category-input").value = productCategory;
}


document.addEventListener('change', function(event) {
    if (event.target && event.target.type === 'radio' && event.target.name === 'selectedProduct') {
        // Radio button is clicked, get selected product details
        const selectedProductLabel = event.target.nextElementSibling.textContent;
        

        // Populate form fields with selected product data
        populateFormFields(selectedProductLabel);
    }
});