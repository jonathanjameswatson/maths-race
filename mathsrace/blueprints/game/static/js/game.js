const race = document.getElementById('race');
const hideGame = document.getElementById('hidegame');
const hostName = document.getElementById('hostname');
const newGameButton = document.getElementById('newgamebutton');
const hostNameTextbox = document.getElementById('hostnametextbox');
const joinButton = document.getElementById('joinbutton');
const leave = document.getElementById('leave');
const start = document.getElementById('start');
const errorLine = document.getElementById('errorline');
const playerTable = document.getElementById('playertable')

let clientPlayers = [];

const playersTemp = [{
  name: 'a',
  percent: 10,
}, {
  name: 'b',
  percent: 20,
}];

let answer = 0;

const socket = io.connect(`http://${document.domain}:${window.location.port}`);

const toggleFullScreen = () => {
  const doc = window.document;
  const docEl = doc.documentElement;

  const requestFullScreen = docEl.requestFullscreen
  || docEl.mozRequestFullScreen || docEl.webkitRequestFullScreen || docEl.msRequestFullscreen;
  const cancelFullScreen = doc.exitFullscreen || doc.mozCancelFullScreen
  || doc.webkitExitFullscreen || doc.msExitFullscreen;

  if (!doc.fullscreenElement && !doc.mozFullScreenElement
    && !doc.webkitFullscreenElement && !doc.msFullscreenElement) {
    requestFullScreen.call(docEl);
  } else {
    cancelFullScreen.call(doc);
  }
};

const movePlayer = (playerDiv, percent) => {
  if (window.getComputedStyle(race).getPropertyValue('flex-direction') === 'row') {
    playerDiv.style.top = `${percent - 6}%`;
    playerDiv.style.left = '5%';
  } else {
    playerDiv.style.top = 'auto';
    playerDiv.style.left = `${percent - 6}%`;
  }
};

const createLane = (player) => {
  const lane = document.createElement('div');
  lane.classList.add('lane');

  const playerDiv = document.createElement('div');
  playerDiv.classList.add('player');

  const textNode = document.createTextNode(player.name.split('').join(' '));

  lane.appendChild(playerDiv);
  lane.appendChild(textNode);

  race.appendChild(lane);

  return [lane, playerDiv];
};

const updatePlayers = (players) => {
  const playersNames = players.map(({ name }) => name);
  const clientPlayersNames = clientPlayers.map(({ name }) => name);

  const newPlayers = players.filter(player => clientPlayersNames.indexOf(player.name) === -1);
  const oldPlayers = clientPlayers.filter(player => playersNames.indexOf(player.name) === -1);
  const samePlayers = clientPlayers.filter(player => playersNames.indexOf(player.name) !== -1)

  newPlayers.forEach((player) => {
    [player.lane, player.div] = createLane(player);
  });

  oldPlayers.forEach((player) => {
    player.lane.remove();
  });

  samePlayers.forEach((player) => {
    player.percent = players.find(p => p.name === player.name).percent;
  });

  clientPlayers = samePlayers.concat(newPlayers);

  clientPlayers.forEach((player) => {
    movePlayer(player.div, player.percent);
  });
};

const resize = () => {
  clientPlayers.forEach((player) => {
    movePlayer(player.div, player.percent);
  });
};

const newGame = () => { socket.emit('m_new_game'); };

const joinGame = () => { socket.emit('m_join_game', hostNameTextbox.value); };

const leaveGame = () => {
  hideGame.style.visibility = 'hidden';
  hostName.innerHTML = 'Host name: none';
  newGameButton.disabled = false;
  joinButton.disabled = false;
  hostNameTextbox.disabled = false;
  leave.disabled = true;
};

const leaveGameButton = () => {
  leaveGame();
  socket.emit('m_user_leaving');
};

const resetPlayerTable = () => {
  Array(playerTable.rows.length - 1).fill(1).map((x, y) => x + y).reverse()
    .forEach((i) => {
      playerTable.deleteRow(i);
    });
};

socket.on('update', (json) => { updatePlayers(JSON.parse(json)); });

socket.on('joined_game', (host, playerList) => {
  hideGame.style.visibility = 'visible';
  hostName.innerHTML = `Host name: ${host}`;

  resetPlayerTable();
  playerList.forEach((playerName) => {
    const row = playerTable.insertRow();
    const cell = row.insertCell();
    cell.innerHTML = playerName;
  });

  newGameButton.disabled = true;
  joinButton.disabled = true;
  hostNameTextbox.disabled = true;
  leave.disabled = false;
});

socket.on('user_joined', (playerName) => {
  const row = playerTable.insertRow();
  const cell = row.insertCell();
  cell.innerHTML = playerName;
});

socket.on('user_left', (playerName) => {
  errorLine.innerHTML = playerName;
});

socket.on('room_closed', () => { leaveGame(); });

socket.on('overlay_error', (text) => {
  errorLine.innerHTML = text;
});


updatePlayers(playersTemp);

window.onresize = resize;
