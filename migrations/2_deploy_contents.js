const SmartContractName = artifacts.require("BlockCertsOnchaining");
    module.exports = function(deployer) {
        deployer.deploy(SmartContractName);
    };
