pragma solidity >=0.4.24;

contract Ticket {
	address owner;
	bool ticket = false;
	address dealer;

	constructor() public {
		owner = msg.sender;
	}

	event getTicket(address player, bool checkTicket);

	function buy(address payable toPay) payable public {
		if (msg.value != 0.0045e18) {return;}
		toPay.transfer(msg.value);
		ticket = true;
		dealer = toPay;
	}

	function retire() public returns (bool) {
		if (msg.sender!=dealer) {
			emit getTicket(owner, false);
			return false;}
		if (ticket==false) {
			emit getTicket(owner, false);
			return false;}
		ticket = false;
		emit getTicket(owner, true);
		return true;
	}
}
