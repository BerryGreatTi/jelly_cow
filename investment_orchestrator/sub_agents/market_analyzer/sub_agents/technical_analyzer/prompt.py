def get_instruction(version:str="latest"):
    latest_version = "1.0"
    inst = dict()
    
    inst["1.0"] = (
        "You are a specialist in technical analysis."
        " Analyze the given asset's price charts, volume, and key indicators (MA, RSI, MACD)."
        " The tools for this are not yet implemented."
    )


    if version in inst.keys():
        return inst[version]
    else:
        return inst[latest_version]
