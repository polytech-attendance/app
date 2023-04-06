const url = "./testDB.json";
const form = document.getElementById('regForm');
const email = document.getElementById('mail');
const password = document.getElementById('password');
const repassword = document.getElementById('repassword');
const incidentmail = 400;

//submission event for form 
form.addEventListener("submit",(e)=>{
    //implicitly 
    e.preventDefault();
    //validate input data
    Validate();
    //if all fields are valid, send a request to server
    if (SuccessMsg()){
        fetch('url', {
            method: "post",
            body: JSON.stringify({
                email: email.value,
                password: password.value
            }),
            headers: {
                'Content-Type':'application/json'
            }
        })
        .then(response => {
            //if email has been registered, refuse request 
            if (response.status === incidentmail){
                setErrorMsg(email, 'Почта была зарегистрирована');
            }
            else if (response.status === 200){

            }
            else {
                alert('error: '+response.status);
            }
        })
        .catch(error => {
            alert(error);
        })
    }
} );


//check if text is valid email 
const isEmail = (emailVal) =>{
    const filter =/^[\w-\.]+@edu.spbstu.+[\w-]{2,4}$/g;
    return emailVal.match(filter);
}

function Validate(){
    //1. get the data inside each field
    const emailVal = email.value.trim();
    const passwordVal = password.value.trim();
    const repasswordVal = repassword.value.trim();
    //validate
    //email
    if (emailVal === ""){
        setErrorMsg(email, 'Пустое поле нельзя!');
    }
    else if (!isEmail(emailVal)){
        setErrorMsg(email, 'Почта СПБПУ!');
    }
    else{
        setSuccessMsg(email);
    }
    
    //password
    if (passwordVal === ""){
        setErrorMsg(password, 'Пустое поле нельзя!');
    }
    else if (passwordVal.length < 8){
        setErrorMsg(password, 'Пароль должен имееть не меньше 8 характер!')
    }
    else setSuccessMsg(password);

    //reenter password
    if (repasswordVal === ""){
        setErrorMsg(repassword, 'Проверите пароль!');
    }
    else if (repasswordVal !== passwordVal){
        setErrorMsg(repassword, 'Пароль не соответствует!');
    }
    else setSuccessMsg(repassword);
}


//set 'error' mode to form field 
function setErrorMsg(input, errormsgs){
    //get the field (parent element)
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = "form-outline error";
    small.innerText = errormsgs;
}

//set 'success' mode to form field 
function setSuccessMsg(input){
    const formControl = input.parentElement;
    formControl.className = "form-outline success";
}

const SuccessMsg = () =>{
    //get all 'form-outline' elements - all fields
    let formContr = document.getElementsByClassName('form-outline');
    for (var i = 0; i < formContr.length; i++){
        if (formContr[i].className === "form-outline success"){
            let sRate = 0 + i;
            //show which field is valid
            console.log(sRate);
        }
        else return false;
    }
    return true;
}

