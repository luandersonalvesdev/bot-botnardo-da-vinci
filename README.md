# Botnardo Da Vinci

O Botnardo Da Vinci é um bot que cria uma obra de arte única a cada dia, durante 90 dias `(10/02/2024 - 10/05/2024)` em horários aleatórios (fuso UTC), e compartilha no Twitter. O processo de funcionamento é o seguinte:

1. **Prompt Criativo:** O bot interage com o modelo GPT-3.5 da OpenAI no modo chat, gerando um `prompt` criativo e totalmente aleatório.
2. **Geração de Imagem:** Utiliza o modelo DALL·E 2 para criar uma imagem única com base no `prompt` gerado.
3. **Publicação no Twitter:** Posta a imagem no Twitter com um texto e o `prompt` da imagem nos comentários.

Este ciclo se repete diariamente durante 90 dias `(10/02/2024 - 10/05/2024)`, resultando em uma coleção única de obras de arte geradas pelo Botnardo Da Vinci.

## Detalhes Técnicos

- **Linguagem:** Python
- **APIs Utilizadas:** Twitter API e OpenAI
- **Execução:** Agendado para ocorrer uma vez por dia em horário aleatório (fuso UTC).

Siga [@BotnardoDaVinci](https://twitter.com/BotnardoDaVinci) no Twitter para acompanhar as incríveis criações diárias!
