Para executar o projeto, primeiro, é necessário definir a variável de ambiente PYTHONPATH:

```
export PYTHONPATH="caminho/ate/a/pasta/projeto/projeto_websocket"
```

Após isso, basta executar o servidor e informar o nome do arquivo que será recebido:

```
python3 server/udp_rdt_server.py
```

Por último, executar o cliente e, também, informar o nome do arquivo que será enviado, o qual deve ser o mesmo nome informado na etapa anterior:

```
python3 client/udp_rdt_client.py
```