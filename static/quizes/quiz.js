const url = window.location.href
const quizBox = document.getElementById('quiz-box')
const timerBox = document.getElementById('timer-box')

const activateTimer = (time) =>{

    if (time.toString().length < 2){
        timerBox.innerHTML = `<b>Remaining Time: 0${time}:00</b>`
    }else{
        timerBox.innerHTML = `<b>Remaining Time: ${time}:00</b>`
    }
    let minutes = time-1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(()=>{
        seconds --
        if (seconds<0){
            seconds = 59
            minutes --
        }
        if (minutes.toString().length <2){
            displayMinutes = '0'+minutes
        }else{
            displayMinutes = minutes
        }
        if (seconds.toString().length <2){
            displaySeconds = '0'+seconds
        }else{
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0){
            clearInterval(timer)
            sendData()
        }
        timerBox.innerHTML = `<b>Remaining Time: ${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}
$.ajax({
    type:'GET',
    url: `${url}data`,
    success: function(response){
        let data = response.data
        data.forEach(element => {
            for (const[question, answers] of Object.entries(element)){
                quizBox.innerHTML += `
                <hr>
                <div class="fw-bold text-start">
                    <b> ${question}</b>
                </div>
                `
                answers.forEach(answer =>{
                    quizBox.innerHTML += `
                    <div>
                        <input type="radio" class="ans" id="${question}-${answer}" name="${question}" value="${answer}">
                        <label for="${question}"> ${answer} </label>
                    </div>
                    `
                })
            }
        });
        activateTimer(response.time)
    },
    error: function(error){
        console.log(error)
    }

})

const quizForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0].value
    elements.forEach(el=>{
        if(el.checked){
            data[el.name] = el.value
        }else{
            if(!data[el.name]){
                data[el.name] = null
            }
        }
    })

    $.ajax({
        type:'POST',
        url: `${url}save/`,
        data: data,
        success: function(response){
            window.location.href = "https://byquiz.pythonanywhere.com/submit";
        },
        error: function(error){
            console.log('Broken')
        }
    })
}

quizForm.addEventListener('submit', e=>{
    e.preventDefault();

    sendData();

})