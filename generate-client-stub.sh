openapi-generator generate -i https://lehua.kodexa.ai/v3/api-docs -g python -o /tmp/client -p packageName=kodexa.client
rm -rf kodexa/client
cp -r /tmp/client/kodexa/client kodexa/.