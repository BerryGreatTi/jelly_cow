def get_instruction(version:str="latest"):
    latest_version = "1.0"
    inst = dict()
    
    inst["1.0"] = (
        "You are a specialist in news and sentiment analysis."
        " Find recent news, analyze market sentiment, and identify key issues related to the given asset."
        " The tools for this are not yet implemented."
    )


    if version in inst.keys():
        return inst[version]
    else:
        return inst[latest_version]
