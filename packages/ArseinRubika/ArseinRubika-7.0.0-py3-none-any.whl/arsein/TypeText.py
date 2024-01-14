def TypeText(Type:str = None,text:str = None,guid:str = None):
	if Type == "MentionText":
		if guid and text != None:
			return [{"from_index":0,"length":len(text),"mention_text_object_guid":guid,"type":"MentionText"}]
	if Type == "Mono":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Mono"}]
	elif Type == "Bold":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Bold"}]
	elif Type == "Italic":
		if text != None:
			return [{"from_index": 0, "length": len(text), "type": "Italic"}]

