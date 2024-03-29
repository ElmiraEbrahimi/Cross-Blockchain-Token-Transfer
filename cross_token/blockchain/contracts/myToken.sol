// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract myToken {
    string public name = 'myToken';
    string public symbol = 'MTN';
    string public standard = 'myToken v0.1';
    uint8 public decimals = 18;
    uint public totalSupply;
    address Owner;
    address thirdParty;

    mapping(address => uint) public balanceView;
    mapping(address => mapping(address => uint)) public allowing;

    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);
    event Burning(address indexed _owner, address indexed _outerTo, uint256 _value, address _twinContract);
    event Minting(address indexed _outerFrom, address indexed _to, uint256 _value, address _twinContract);

    modifier onlyOwner{
        require(msg.sender == Owner, "Access Denied");
        _;
    }

    constructor(address tParty){
        Owner = msg.sender;
        thirdParty = tParty;
    }

    function initial(uint _value) public onlyOwner {
        totalSupply = _value;
        balanceView[msg.sender] += _value;
        Owner = msg.sender;
        emit Transfer(0x0000000000000000000000000000000000000000, msg.sender, _value);
    }

    function transfer(address _to, uint256 _value) public onlyOwner {
        require(balanceView[msg.sender] >= _value, 'BALANCE NOT ENOUGH');
        balanceView[msg.sender] -= _value;
        balanceView[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
    }

    function approve(address _spender, uint256 _value) public onlyOwner {
        allowing[Owner][_spender] += _value;
        emit Approval(Owner, _spender, _value);
    }

    function transferFrom(address _from, address _to, uint256 _value) public {
        require(msg.sender == _from, "Access Denied");
        require(balanceView[_from] >= _value, 'BALANCE NOT ENOUGH');
        require(allowing[Owner][_from] >= _value, 'PAYMENT IS NOT ALLOWED');

        balanceView[_from] -= _value;
        balanceView[_to] += _value;

        allowing[Owner][_from] -= _value;

        emit Transfer(_from, _to, _value);
    }

    function balanceOf(address _owner) public view returns (uint256){
        return balanceView[_owner];
    }

    function totalSupplyAmount() public view returns (uint256){
        return totalSupply;
    }

    function allowance(address _owner, address _spender) public view returns (uint256){
        return allowing[_owner][_spender];
    }

    function burn(address _outerTo, uint256 _value, address _contract) public {
        require(balanceView[msg.sender] >= _value, "Your balance is not enough!");
        balanceView[msg.sender] -= _value;
        allowing[Owner][msg.sender] -= _value;
        totalSupply -= _value;
        emit Burning(msg.sender, _outerTo, _value, _contract);
    }

    function mint(bool status, address _outerFrom, address _to, uint256 _value, address _contract) public {
        require(msg.sender == thirdParty, "Access Denied");
        require(status, "Account is not allowed to mint");
        balanceView[_to] += _value;
        allowing[Owner][_to] += _value;
        totalSupply += _value;
        emit Minting(_outerFrom, _to, _value, _contract);
    }
}