pragma solidity >=0.4.0 <0.9.0;

contract Pass {
	// dict to contain address of players and bool
	// if true the player can play 
	// owner is the one who build for the first time the contract
	// and will receive the amount of eth for each ticket
	mapping(address => bool) public db;
	address payable owner;
	uint price = 0.0045e18;

	constructor() public {
		owner = msg.sender;
	}

	function buy() payable public {
	// function payable to give the owner the amount of eth
	// once the player pays the ticket he can play
		if (msg.value != price) {
			owner.transfer(msg.value);
			return ;
		}
		
		owner.transfer(msg.value);
		db[msg.sender] = true;
	}

	function retire(address player) public returns (bool) {
	// function to check if player can play or not
	// when function is called it returns the boolean
	// but map is not update
	// bool to false only when the function is run 
	// with a transaction
		if (msg.sender != owner) {
			return false;
		}
		if (db[player]) {
			db[player] = false;
			return true;
		} else {
			return false;
		}
	}
}
