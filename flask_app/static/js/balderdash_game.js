var socket = io();
socket.on('connect', function () {
    socket.emit('connected', { data: 'I\'m connected!' });
});

socket.on('connected_resp', (data) => {
    console.log(data);
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
    } else {
        console.log("Name is there");
    }
})
