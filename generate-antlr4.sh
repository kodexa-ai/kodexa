antlr4 -o /kodexa/selectors/impl -package kodexa.selectors.impl -listener -visitor -Dlanguage=Python3 -lib resources resources/selector.g4


datamodel-codegen --input resources/api-docs.yaml --output kodexa/model/objects.py