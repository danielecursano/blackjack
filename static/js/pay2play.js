const ethereumButton = document.querySelector('.connect');

if (window.location.pathname == '/') {
	document.getElementById('play_btn').disabled = true;
}

let accounts = [];

ethereumButton.addEventListener('click', () => {
	    if (jQuery('#main_btn').hasClass('sendEthButton')){
	if (ethereum.networkVersion != '3') {
		alert('Connect to ropsten!');
		return;
	}
	ethereum.request({
	    method: 'eth_sendTransaction',
	    params: [
		{
		from: accounts[0],
		to: '0x997515C1CA7a0F2cCf670d215765B1bAf11FeCD7',
		value: '10000000000000',	
		},
	    ],
	    })
	    .then((txHash) => enableButton(txHash))
	    .catch((error) => console.error, disableButton());
			
	}
});

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

