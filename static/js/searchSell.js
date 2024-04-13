

const searchField = document.querySelector('#searchField')
const tableOutput = document.querySelector(".table-output")
const appTable = document.querySelector(".app-table")
const paginationContainer = document.querySelector(".pagination-container")
const tbody = document.querySelector(".table-body")


tableOutput.style.display = "none"

searchField.addEventListener('keyup',(e) =>{
   const searchValue = e.target.value;

    if(searchValue.trim().length > 0){
        paginationContainer.style.display="none"

        tbody.innerHTML="";
    
            fetch("/search-product",{
                body:JSON.stringify({searchText: searchValue}),
                method:"POST"
            })
            .then((res) =>res.json())
            .then((data) =>{

            console.log("data",data)
            appTable.style.display="none"
            tableOutput.style.display="block"

            if(data.length==0){
                tableOutput.innerHTML="No result found"


            }else{

                data.forEach((item) => {

                    tbody.innerHTML += `
                    <tr>
                    
                    <td>${item.name}</td>
                    <td>${item.amount}</td>
                    <td>${item.qauntity}</td>
                    <td>${item.date}</td>
    
                   
    
                    </tr>
                    
                    `


                })

               
                          
            }

                

            })
                
                
              
    }else{
        tableOutput.style.display="none"
        appTable.style.display="block"
        paginationContainer.style.display="block"

    }
})