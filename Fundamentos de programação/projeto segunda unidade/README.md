# Sistema de Gerenciamento de Treinos de Corrida 🏃‍♂️

## Descrição do Projeto
Este projeto foi desenvolvido para ajudar Pedro, um atleta de corrida, a monitorar e melhorar seu desempenho. O **Sistema de Gerenciamento de Treinos de Corrida** permite que ele registre e acompanhe seus treinos e competições, definindo metas e desafios, além de receber sugestões de treinos personalizadas. Este sistema foi pensado para simplificar o acompanhamento de desempenho e promover uma experiência interativa e motivadora para o atleta.

## Funcionalidades
### 1. CRUD de Treinos e Competições
- Pedro pode **Adicionar**, **Visualizar**, **Atualizar** e **Excluir** registros de treinos e competições.
- Interface interativa baseada em menus para facilitar a navegação.

### 2. Cadastro de Treinos e Competições
- Registro de informações detalhadas de cada treino e competição, incluindo:
  - Data
  - Distância percorrida (em km)
  - Tempo (em horas, minutos e segundos)
  - Localização
  - Condições climáticas

### 3. Filtragem por Distância ou Tempo
- Permite que Pedro filtre seus registros com base em critérios específicos:
  - **Distância percorrida**: analise os treinos em diferentes distâncias.
  - **Tempo**: ajuda a identificar treinos com tempos específicos para diferentes distâncias.

### 4. Armazenamento de Dados
- Os dados são armazenados em um **banco de dados local** utilizando arquivos `.csv`.
- As informações são persistentes, permitindo que Pedro acesse e revise seu histórico de treinos e competições a qualquer momento.

### 5. Metas e Desafios
- Pedro pode definir metas pessoais, como:
  - **Correr uma certa distância mensalmente** (por exemplo, 100 km/mês).
  - **Melhorar o tempo em uma determinada distância** (ex: reduzir o tempo para 5 km).
- O sistema acompanha o progresso de Pedro e fornece notificações sobre o cumprimento dessas metas.

### 6. Sugestões de Treinos Aleatórios
- O sistema sugere treinos aleatórios baseados no histórico de Pedro.
- Essas sugestões ajudam Pedro a variar sua rotina, promovendo a melhoria contínua de seu desempenho.

### 7. Funcionalidade Extra: Sugestão de Treino com Base em Médias de Distância e Tempo
- O sistema calcula automaticamente as médias de distância e tempo de Pedro e sugere treinos alinhados com essas médias, levando em consideração também a localização e condições climáticas ideais para o treino.

## Tecnologias Utilizadas
- **Python**: linguagem principal do sistema.
- **csv** para manipulação e leitura de arquivos.
- **matplotlib** para criar telas gráficas.

## Como Usar
1. **Clonar o Repositório**:
    ```bash
    git clone https://github.com/usuario/sistema-gerenciamento-treinos
    cd sistema-gerenciamento-treinos
    ```
2. **Instalar Dependências**:
   - Instale o `matplotlib`:
      ```bash
      pip install matplotlib
      ```

3. **Executar o Sistema**:
    ```bash
    python main.py
    ```

4. **Navegação no Menu**:
   - Utilize o menu interativo para acessar as funcionalidades do sistema.

## Estrutura do Projeto
- `main.py`: Arquivo principal que inicializa o sistema.
- `data/`: Diretório para armazenar os dados de treinos e competições em formato `.csv`.

## Melhorias Futuras
- Integração com APIs de previsão do tempo para dados climáticos em tempo real.
- Implementação de uma interface gráfica (GUI) para facilitar o uso do sistema.
- Expansão das opções de filtragem para análise mais detalhada de desempenho.

## Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests ou abrir issues para sugestões de novas funcionalidades.

---

Divirta-se monitorando seus treinos e competições com o **Sistema de Gerenciamento de Treinos de Corrida**! 💪
