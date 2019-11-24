pragma solidity >0.5.0;

contract BlockCerts_Onchaining{
    smartcontract public sc;
    
    modifier onlyIssuer(){
        require(msg.sender == sc.issuerID);
        _;
    }
    
    struct smartcontract{
        address issuerID; //would like to have them constant, but can't be!
        address recipientID; //should be "to" Adress which is currently left blank/dummy inserted!, is the input data the SC adress?
        
        bool revoked;
        
        //ANOTHER NICE OPTION to store state, returns list positions (waiting = 0)
        //enum State {Waiting, Valid, Revoked}; 
        //State public state;
    }
    
    constructor() public{
        sc.issuerID = msg.sender; //msg.sender is the one deploying this SC
        //smartcontract.recipientID = msg.recipient; //--> needs to be initializedf from python call!
        sc.revoked = false;
        //smartcontract.state = State.Waiting;
    }

    //GETTER SETTER
    function getRecipientID() public view returns(address){
        return sc.recipientID;
    }
    
    function getIssuerID() public view returns(address){
        return sc.issuerID;
    }
    
    //REVOCATION
    function revoke() public onlyIssuer{ //have to make sure only the issuer revokes
        //smartcontract.state = State.Revoked;
        sc.revoked = true;
    }
    
    function getRevoked() public view returns(bool){
        return sc.revoked;
    }
    
    /*//ACTIVATION
    function setActivate() public onlyIssuer{ //have to make sure only the issuer revokes
        smartcontract.state = State.Activate;
    }*/
}
