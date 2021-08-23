openapi-generator generate -i https://lehua.kodexa.ai/v3/api-docs -g python -o /tmp/client -p packageName=kodexa.client -p generateSourceCodeOnly=true
rm -rf kodexa/client
cp -r /tmp/client/kodexa/client kodexa/.
rm -rf kodexa/client/docs
rm -rf kodexa/client/test

antlr -Dlanguage=Python3 resources/selector.g4 -o kodexa/selectors