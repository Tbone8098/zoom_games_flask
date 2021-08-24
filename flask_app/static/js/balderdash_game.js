var socket = io();
socket.on('connect', function () {
    socket.emit('connected', { data: 'I\'m connected!' });
});

socket.on('connected_resp', (data) => {
    console.log(data['msg']);
    var playerList = document.querySelector('.player-list')
    var is_there = false
    for (const player of playerList.children) {
        if (player.getAttribute('player_id') == data['player_info']['id']){
            is_there = true
        }
    }
    if (!is_there){
        playerList.innerHTML += `
        <li class="${data['player_info']['id']}">${data['player_info']['username']}</li>
        `
        alert(`${data['player_info']['username']} has joined the game`)
    }
})


var leaveGame = document.querySelector('#leave-game')

leaveGame.addEventListener('click', () => {
    socket.emit('leave_game')
})

socket.on("leave_game_resp", (data) => {
    window.location.href = '/balderdash'
})

socket.on("leave_game_resp_broadcast", (data) => {
    console.log(`${data['username']} has left the game`);
    var playerList = document.querySelector('.player-list')
    for (const player of playerList.children) {
        console.log(player.textContent);
        if (data['username'] === player.textContent){
            alert(`${player.textContent} is leaving the game`);
            player.remove()
        }
    }
})

