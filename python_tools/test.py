from onchaining_tools import connections as conn


cc = conn.ContractConnection()

cc.functions.issue(123)
print(cc.functions.getStatus(123))
cc.functions.revoke(123)
print(cc.functions.getStatus(123))
