let web3 = new Web3('https://ropsten.infura.io/v3/4ef94712ce884095ad5a2404003f36e5');
const ethereumButton = document.querySelector('.connect');

const abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"player","type":"address"},{"indexed":false,"internalType":"bool","name":"checkTicket","type":"bool"}],"name":"getTicket","type":"event"},{"inputs":[{"internalType":"address payable","name":"toPay","type":"address"}],"name":"buy","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"retire","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]

if (window.location.pathname == '/') {
	document.getElementById('play_btn').disabled = true;
}

let accounts = [];
const addressRecipient = '0x997515C1CA7a0F2cCf670d215765B1bAf11FeCD7';
const contractAddress = '0xeBEee8BBF68887666059a4F86B1Fed12c8BB58b2';
ethereumButton.addEventListener('click', () => {
	    if (jQuery('#main_btn').hasClass('sendEthButton')){
	if (ethereum.networkVersion != '777') {
		alert('Connect to ropsten!');
		return;
	}
		getTicket();
	}
});

async function getTicket() {
	let contract = new web3.eth.Contract(abi, contractAddress, {from: accounts[0]});
	const data = contract.methods.buy(addressRecipient).encodeABI();
	const txObject = {
		data: data,
		value: web3.utils.toHex(web3.utils.toWei('0.0045', 'ether')),
		to: contractAddress,
		from: accounts[0]
	}
	ethereum.request({
	    method: 'eth_sendTransaction',
	    params: [txObject],
	    })
	    .then((txHash) => enableButton(txHash))
	    .catch((error) => console.error, disableButton());
}


function enableButton(hash) {
	console.log(hash);
	document.getElementById("txHash").value = hash;	
	document.getElementById('play_btn').disabled = false;
	document.getElementById('play_btn').classList.remove('btn-secondary');
	document.getElementById('play_btn').classList.add('btn-success');
}

function disableButton() {
	document.getElementById('play_btn').disabled = true;
}


ethereumButton.addEventListener('click', () => {
	document.getElementById("main_btn").classList.remove('connect');
	document.getElementById("main_btn").classList.add('sendEthButton');
	document.querySelector('#main_btn').innerText = 'Buy ticket';
	getAccount();
});

async function getAccount() {
	accounts = await ethereum.request({ method: 'eth_requestAccounts'});
}
