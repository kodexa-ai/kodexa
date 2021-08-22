openapi-generator generate -i https://lehua.kodexa.ai/v3/api-docs -g python -o /tmp/client -p packageName=kodexa.client -p generateSourceCodeOnly=true -p
rm -rf kodexa/client
cp -r /tmp/client/kodexa/client kodexa/.