import spacy
nlp = spacy.load("en_core_web_sm")

CROPS = {
    "rice","wheat","maize","cotton","tomato","banana",
    "groundnut","chilli","onion","potato","sugarcane"
}

STAGES = {
    "sowing","tillering","flowering","vegetative",
    "panicle","knee","harvest"
}

SYMPTOMS = {
    "yellow","yellowing","brown","spots","spot","curl",
    "wilting","wilt","rot","blast","blight","mildew",
    "rust","hopper","borer","aphid","thrips","whitefly"
}

def extract_slots(tokens):
    slots = {}
    for t in tokens:
        if t in CROPS:
            slots["crop"] = t
        if t in STAGES:
            slots["stage"] = t
        if t in SYMPTOMS:
            slots["symptom"] = t
    return slots

def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in {"GPE", "LOC"}:
            return ent.text.lower()
    return None
