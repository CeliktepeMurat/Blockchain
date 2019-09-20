// istcoin İCO

// Version of compiler
pragma solidity ^0.5.11;

contract istcoin_ico{
    
    // Introducing the maximum number of istcoin
    uint public max_istcoin = 1000000;
    
    // Introducing TL to istcoin conversion rate
    uint public tl_to_istcoin = 1000;
    
    // Introducing the number of istcoin that have been bought by the investors
    uint public total_istcoin_bought = 0;
    
    // Mapping from the investor address to its equity in istcoin and tl
    mapping(address => uint) equity_istcoin;
    mapping(address => uint) equity_tl;
    
    //Checking if an investor can but istcoin
    modifier can_buy_istcoins(uint tl_invested){
        require(tl_invested * tl_to_istcoin + total_istcoin_bought <= max_istcoin);
        _;
    }
    
    //Getting equity in istcoin on an investor
    // view means that there will be no changing inside the function
    function equity_in_istcoin(address investor) external view returns (uint){
        return equity_istcoin[investor];
    }
    
    //Getting equity in tl on an investor
    function equity_in_tl(address investor) external view returns (uint){
        return equity_tl[investor];
    }
    
    // Buying istcoin
    function buy_istcoin(address investor, uint tl_invested) external can_buy_istcoins(tl_invested){
        uint istcoin_bought = tl_invested * tl_to_istcoin;
        equity_istcoin[investor] += istcoin_bought;
        equity_tl[investor] = equity_istcoin[investor] / 1000;
        total_istcoin_bought += istcoin_bought;
    }
    
    // Selling istcoin
    function sell_istcoin(address investor, uint istcoin_sold) external {
        equity_istcoin[investor] -= istcoin_sold;
        equity_tl[investor] = equity_istcoin[investor] / 1000;
        total_istcoin_bought -= istcoin_sold;
    }
}
