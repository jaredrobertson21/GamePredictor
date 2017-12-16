const gamePredictions = {};
const gameButton = document.querySelectorAll(".game");
const submitPredictions = document.querySelector("#submit");

gameButton.forEach(function(gameWinner) {
    gameWinner.addEventListener('click', function(){
        let gameId = gameWinner.id.slice(-12);
        gamePredictions[gameId] = gameWinner.id.slice(0,-12); 
    });
})

submitPredictions.addEventListener('click', function(){
    axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/games/submit_data/',
        data: gamePredictions,
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken',
        headers: {'X-Requested-With': 'XMLHttpRequest',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'},
    }).then(function(response){
        alert('Predictions submitted successfully!');
    }).catch(function(error){
        alert('Error: Submission failed');
    })  
})

