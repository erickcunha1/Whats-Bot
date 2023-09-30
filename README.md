# Enviador de Mensagens no WhatsApp

Este projeto utiliza Selenium e Pandas para automatizar o envio de mensagens via WhatsApp Web. Ele é capaz de lidar com números de telefone inválidos e enviar mensagens personalizadas.

## Sumário

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Utilização](#utilização)
- [Contribuição](#contribuição)
- [Licença](#licença)

## Introdução

Este projeto em Python permite enviar mensagens personalizadas para contatos do WhatsApp usando um navegador web controlado pelo Selenium. Ele verifica números inválidos e os trata de maneira apropriada.

## Pré-requisitos

Certifique-se de ter os seguintes itens instalados antes de executar o script:

- Python 3.x
- Selenium
- Pandas
- ChromeDriver
- WebDriver Manager para Chrome
- Navegador Chrome

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto:

```bash
git clone https://github.com/your-username/whatsapp-message-sender.git
cd whatsapp-message-sender
```

2. Instale os pacotes Python necessários usando pip:

```bash
pip install pandas selenium webdriver-manager
```

## Utilização

1. Modifique o arquivo `data.csv` para incluir os nomes e números dos contatos.
2. Execute o script usando o seguinte comando:

```bash
python main.py
```

O script abrirá automaticamente o WhatsApp Web, enviará mensagens para os contatos especificados e lidará com números de telefone inválidos, adicionando-os ao arquivo `numeros_invalidos.txt`.

## Contribuição

Sinta-se à vontade para contribuir para este projeto abrindo problemas ou criando solicitações de pull. Suas contribuições são muito apreciadas.
