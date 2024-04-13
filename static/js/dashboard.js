const renderChart=(data,label) => {

 var ctx = document.getElementById('myChart');

 const backgroundColors = label.map(() => {
    return '#' + Math.floor(Math.random() * 16777215).toString(16);
  });

  new Chart(ctx, {
    type: 'pie',
    data: {
      labels: label,
      datasets: [{
        label: 'product_summary_TotalPrices',
        data: data,
        backgroundColor: backgroundColors,
        borderWidth: 1
      }]
    },
    options: {
      title: {
        display:true,
        text: 'Products TotalPrice Summary'

      }
    }
  });

}

const getChartData = () => {
   fetch('product_summary_amount').then(res=>res.json()).then(results=>{
    console.log("data", results)
    const categoty_summary_data = results.category_summary;
    const [label,data] = [
        Object.keys(categoty_summary_data),
        Object.values(categoty_summary_data)
    ] 

    renderChart(data,label)

   })

}
document.onload=getChartData()
  
  
  
const renderBarChart = (label, data) => {

    var quantity = document.getElementById('PIEAmount');
    const backgroundColors = label.map(() => {
        return '#' + Math.floor(Math.random() * 16777215).toString(16);
      });
    

  new Chart(quantity, {
    type: 'bar',
    data: {
      labels: label,
      datasets: [{
        label: ' Product Quantity Summary',
        data: data,
        backgroundColor: backgroundColors,
        borderWidth: 1
      }]
    },
    options: {
      
        display:true,
        text: 'Products Quantity Summary'
      
    }
  });

}

  

const getBarChatData = () => {
    fetch('category_quantity_summary').then(res=>res.json()).then(results=>{
     console.log("data", results)
     const categoty_summary_data = results.category_summary;
     const [label,data] = [
         Object.keys(categoty_summary_data),
         Object.values(categoty_summary_data)
     ] 
 
     renderBarChart(label,data)
 
    })
 
 }
 document.onload=getBarChatData()