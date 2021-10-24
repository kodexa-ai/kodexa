#antlr4 -o /kodexa/selectors/impl -package kodexa.selectors.impl -listener -visitor -Dlanguage=Python3 -lib resources resources/selector.g4

datamodel-codegen --input resources/api-docs.yaml --output kodexa/model/objects.py --base-class kodexa.model.base.KodexaBaseModel
python -c "import sys;lines=sys.stdin.read();print(lines.replace('options: Optional[Dict[str, Dict[str, Any]]] = None','options: Optional[Dict[str, Any]] = None'))" < kodexa/model/objects.py > kodexa/model/objects_new.py
cp kodexa/model/objects_new.py kodexa/model/objects.py
rm kodexa/model/objects_new.py