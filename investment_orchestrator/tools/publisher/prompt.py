def get_instruction(version:str="latest"):
    latest_version = "1.0"
    inst = dict()
    
    inst["1.0"] = """You are a publisher agent. Your job is to take content and publish it to a user-specified channel using the available tools."""
    
    if version in inst.keys():
        return inst[version]
    else:
        return inst[latest_version]
