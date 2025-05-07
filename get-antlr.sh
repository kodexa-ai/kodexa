# Download ANTLR
curl -O https://www.antlr.org/download/antlr-4.13.1-complete.jar

# Generate Python3 code including visitor and listener interfaces
java -jar antlr-4.13.1-complete.jar -Dlanguage=Python3 -visitor -listener resources/KodexaSelector.g4 -o kodexa/selectors
