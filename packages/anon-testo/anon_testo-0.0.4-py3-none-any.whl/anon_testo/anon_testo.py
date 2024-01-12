from presidio_analyzer import (
    AnalyzerEngine, 
    RecognizerRegistry, 
    PatternRecognizer
    )
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import (
    PhoneRecognizer, 
    SpacyRecognizer, 
    ItFiscalCodeRecognizer, 
    ItVatCodeRecognizer
    )

from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

import json

def nlpInput(input:dict):
#REQUIRES: Valid GateNLP document as input
#MODIFIES: input
#EFFECTS: Deletes PII from the annotations and returns them in a DenyList ready to be used by Presidio
    try:
        parsedText = input
        text = parsedText['annotation_sets']["entities"]["annotations"]
        denyList = []
        for annotazione in text:
            if annotazione["features"]["ner"]["type"] != "articolo_di_legge" and annotazione["features"]["ner"]["type"] != "data":
                for parola in annotazione["features"]["ner"]["normalized_text"].split():
                    denyList.append(parola)
                annotazione["features"]["title"] = ""
                annotazione["features"]["ner"]["normalized_text"]= "" 
        parsedText['annotation_sets']["entities"]["annotations"] = text

        #with open("testAnnotazioniRisultato.json", "w") as fileOutput:
        #json.dump(parsedText, fileOutput, indent=4)
                
        for parola in parsedText['features']["parte"].lower().split():
            denyList.append(parola)

        for parola in parsedText['features']["controparte"].lower().split():
            denyList.append(parola)

        for parolaGiudice in parsedText['features']["nomegiudice"].lower().split():
            denyList.append(parolaGiudice)   

        codFiscaleGiudice = parsedText['features']["cf_giudice"]
        denyList.append(codFiscaleGiudice)

        codFiscaleSender = parsedText['features']["senderid"]    
        denyList.append(codFiscaleSender)

        return [denyList, parsedText]
    except:
        print("L'input non è in un formato supportato")

def analisiTesto(denyList:list,testo:json):
#REQUIRES: Validated GateNLP document and DenyList as inputs
#MODIFIES: //
#EFFECTS: Creates the Analyzer and identifies PII via DenyList and other Recognizers
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [
        {"lang_code": "it", "model_name": "it_core_news_lg"},
        ],
    }

    metadataList_recognizer = PatternRecognizer(supported_language="it", supported_entity= "PERSON", deny_list= denyList, deny_list_score=1)
    telephone_recognizer_italian = PhoneRecognizer(supported_language= "it")
    spacyDefault_recognizer_italian = SpacyRecognizer(supported_language= "it", context= ["avv. ", "sig. "])
    fiscalCode_italian = ItFiscalCodeRecognizer(context="C.F. ")
    pIva_italian = ItVatCodeRecognizer(context="C.F. ")
    
    registry = RecognizerRegistry()
    registry.add_recognizer(metadataList_recognizer)
    registry.add_recognizer(telephone_recognizer_italian)
    registry.add_recognizer(spacyDefault_recognizer_italian)
    registry.add_recognizer(fiscalCode_italian)
    registry.add_recognizer(pIva_italian)

    provider = NlpEngineProvider(nlp_configuration = configuration)
    nlp_engine_with_italian = provider.create_engine()

    # Passiamo il provider all'engine
    analyzer = AnalyzerEngine(
    nlp_engine = nlp_engine_with_italian,
    registry = registry,
    supported_languages = "it")

    entity_list = ["PERSON", "IT_FISCAL_CODE", "IT_VAT_CODE", "ORGANIZATION", "LOCATION", "DATE", "TIME"]
    
    try:
        results = analyzer.analyze(text = testo["text"], 
                           language = "it", 
                           entities = entity_list,
                           score_threshold = 0.35,
                           return_decision_process= True)
        return (results)
    except:
        print("Analisi fallita")

def anonimTesto(testo:json, risultatiAnalisi:list):
#REQUIRES: Validated GateNLP document text and analysis result as input
#MODIFIES: Validated GateNLP document
#EFFECTS: Creates the Anonymizer and masks the identified PIIs
    engine = AnonymizerEngine()
    # Rinomino gli operatori da quelli di Default ad una versione in italiano
    it_operators = {
        "PERSON": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        "LOCATION": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        "ORGANIZATION": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        "PHONE_NUMBER": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        "IT_FISCAL_CODE": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        "IT_VAT_CODE": OperatorConfig("mask", {"masking_char": "*", "chars_to_mask": 30, "from_end": 0}),
        }

    result = engine.anonymize(testo["text"], risultatiAnalisi, operators = it_operators)

    return result.text

def nlpOutput(nlpRipulito:json, anonimTesto:str):
#REQUIRES: Validated GateNLP document text and anonymized result as input
#MODIFIES: inputNLP
#EFFECTS: Returns the new anonymized GateNLP
    try:
        documentoAnonimizzato = nlpRipulito
        documentoAnonimizzato["text"] = anonimTesto

        return documentoAnonimizzato
    except:
        print("Ritorno del gateNLP modificato fallito")

