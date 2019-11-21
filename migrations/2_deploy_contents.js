var BlockCertsOnchaining = artifacts.require("BlockCertsOnchaining");
	module.exports = function(deployer) {
	deployer.deploy(BlockCertsOnchaining);
};
