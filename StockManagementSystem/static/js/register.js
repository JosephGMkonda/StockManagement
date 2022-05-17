const usernameField = document.querySelector("#usernameField")
const feedBackArea = document.querySelector('.invalid-feedback') 
const emailField = document.querySelector('#emailField')
const emailFeedBackArea = document.querySelector('.emailFeedBackArea')
const usernameSuccessOutput = document.querySelector('.usernameSuccessOutput')
const emailSuccessOutput = document.querySelector('.emailSuccessOutput')
const showPasswordToggle = document.querySelector('.showPasswordToggle')
const passwordField = document.querySelector('#passwordField')
const submitBtn = document.querySelector('.submit-btn')

const handleToggleInput = (e) => {
    if(showPasswordToggle.textContent=="SHOW"){
        showPasswordToggle.textContent="HIDE";
        passwordField.setAttribute("type","password");



    }
    else{
        showPasswordToggle.textContent="SHOW";
        passwordField.setAttribute("type","text");

    }


}

showPasswordToggle.addEventListener('click',handleToggleInput)


emailField.addEventListener("keyup" ,(e) => {

    const emailVal = e.target.value;
    emailSuccessOutput.textContent =`Chencking ${emailVal}`
    emailField.classList.remove('is-invalid')
    emailFeedBackArea.style.display="none"
    
    if(emailVal.length > 0){
        fetch("/authentication/email_validation",{
            body:JSON.stringify({email: emailVal}),
            method:"POST"
        })
        .then((res) =>res.json())
        .then((data) =>{
            console.log("data",data)
            emailSuccessOutput.style.display="none"
            if(data.email_error){
                submitBtn.disabled=true;
                emailField.classList.add('is-invalid')
                emailFeedBackArea.style.display="block"
                emailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`


            }else{
                submitBtn.removeAttribute('disabled')
            }
        })
    }

})


usernameField.addEventListener("keyup" , (e) => {

    const usernameVal = e.target.value;
    usernameField.classList.remove('is-invalid')
    feedBackArea.style.display="none"
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`
    
    if(usernameVal.length > 0){
        fetch("/authentication/username_validation",{
            body:JSON.stringify({username: usernameVal}),
            method:"POST"
        })
        .then((res) =>res.json())
        .then((data) =>{
            
            usernameSuccessOutput.style.display="none"
            if(data.username_error){
                submitBtn.disabled=true;
                usernameField.classList.add('is-invalid')
                feedBackArea.style.display="block"
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`


            }else{
                submitBtn.removeAttribute('disabled')
            }
        })
    }
    
})