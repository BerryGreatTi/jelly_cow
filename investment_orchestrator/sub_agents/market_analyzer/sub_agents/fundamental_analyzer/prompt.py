def get_instruction(version:str="latest"):
    latest_version = "1.0"
    inst = dict()
    
    inst["1.0"] = """You are a specialist in fundamental analysis. Analyze the given company's financial health, valuation, and competitive advantages. The tools for this are not yet implemented."""
    
    if version in inst.keys():
        return inst[version]
    else:
        return inst[latest_version]
