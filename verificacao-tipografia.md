# Verificação de tipografia e interface: sala.html (olivia-kalicinski.vercel.app)

**Escopo:** a sala desenhada, as duas faixas, a moldura de hover e a página do CV
**Entrada:** CSS + estilo computado medido no navegador em 390×844 e 1440×900 · **Meio:** web (celular e computador)
**Tipos de texto considerados:** corrido (CV), display (nome, títulos), rótulo (faixas, molduras) · **Idioma:** inglês
**O que não foi possível verificar com esta entrada:** anel de foco por teclado, ampliação de texto a 200%, leitura em aparelho real, contraste de não‑texto (fio das seções, sublinhado dos links)

## Resumo

Três coisas de verdade: o subtítulo do topo e a linha de local do CV ficam abaixo de 4,5:1 — e a
linha de local cai para 2,89:1 quando passa sobre o traço do desenho; a câmera tem 32×27 px de
área clicável no celular, menos de um terço do alvo recomendado; e o painel do CV, mesmo invisível,
continua recebendo o cursor de teclado — quem navega com Tab cai dentro de uma página que não está
na tela. O resto é ofício: corpo pequeno demais em três lugares e um rótulo de seção menor que o
título que ele encabeça. A estrutura e a hierarquia estão boas e não devem ser mexidas para
consertar o resto.

## Placar por lente

| lente | verificados | passa | falha | não verificável |
|---|---|---|---|---|
| estrutura e hierarquia | 6 | 6 | 0 | 1 |
| legibilidade | 6 | 4 | 2 | 2 |
| ofício tipográfico | 5 | 3 | 2 | 1 |
| cor, percepção e informação | 2 | 2 | 0 | 2 |
| padrões de interface | 5 | 2 | 3 | 2 |

## Problemas

### [A1] O subtítulo do topo fica abaixo do limiar de contraste
- **Gravidade:** Alto
- **Critério:** LEG-37 / LUX-39 — texto normal ≥ 4,5:1
- **Medido × esperado:** 4,26:1 × 4,5:1. `.faixa.alta small`, 9,5 px, `opacity:.58`, cor efetiva rgb(115,113,104) sobre rgb(243,239,228)
- **Evidência:** "GROWTH · BRANDING · CODE", logo abaixo do nome, em todas as telas
- **Base:** estilo computado + razão calculada (fórmula sRGB)
- **Força da fonte:** Segunda mão (Yablonski p. 101 e Wathan/Schoger p. 162, ambos repassando WCAG 1.4.3) · **Tipo:** legibilidade
- **Correção proposta:** `opacity:.58` → `.62` (4,84:1) ou `.66` (5,55:1). Calculei os dois; prefiro `.66`, que deixa margem para a compressão de tela.
- **Fonte:** Yablonski, *Leis da UX*, p. 101

### [A2] A linha de local do CV some sobre o traço do desenho
- **Gravidade:** Alto
- **Critério:** LEG-37 / LUX-39
- **Medido × esperado:** 3,20:1 sobre papel liso e **2,89:1** sobre o trecho em que o painel cobre o traço mais escuro × 4,5:1. `.dentro .onde`, 11 px, cor #8b8577
- **Evidência:** "Rio de Janeiro, Brazil", "Independent · Miguel Pereira…", abaixo de cada cargo do CV
- **Base:** estilo computado; o fundo efetivo rgb(232,228,218) é Inferido (0,94 de papel + 0,06 de lápis a rgb(60,58,54))
- **Força da fonte:** Segunda mão · **Tipo:** legibilidade
- **Correção proposta:** #8b8577 → **#635e52** (5,62:1 sobre papel, 5,08:1 sobre o pior fundo)
- **Fonte:** Wathan e Schoger, *Refactoring UI*, p. 162

### [A3] A câmera tem alvo de 32×27 px no celular
- **Gravidade:** Alto
- **Critério:** LUX-01 / INT-120 — 44×44 pt (Apple) e 48×48 dp (Material)
- **Medido × esperado:** 32×27 px × 44×44. Em 1440 px sobe para 62×36, ainda abaixo na altura
- **Evidência:** porta `foto` (THE PHOTOGRAPHY), medida em 390×844
- **Base:** `getBoundingClientRect` no navegador
- **Força da fonte:** Segunda mão — a tabela de Yablonski não traz procedência e **não** deriva de Fitts · **Tipo:** interface
- **Correção proposta:** `min-width:44px;min-height:44px` em `.porta` resolve as cinco de uma vez sem tocar no desenho; a área cresce para fora do objeto, o que não é visível porque a porta é invisível.
- **Fonte:** Yablonski, cap. 2, Tab. 2-1, pp. 18–19

### [A4] O CV fechado continua no caminho do teclado
- **Gravidade:** Alto
- **Critério:** sem ID na Biblioteca — conteúdo escondido só por `opacity` e `pointer-events` segue focável
- **Medido × esperado:** três elementos focáveis (o botão "Back to the room" e dois links de contato) com `offsetParent` ativo enquanto `.dentro` está invisível × nenhum
- **Evidência:** `.dentro` sem a classe `no` tem `display:block`, `opacity:0`, `pointer-events:none`
- **Base:** DOM medido no navegador
- **Força da fonte:** Externo (padrão de acessibilidade; não citei norma com versão, então **não** usei isso para subir a gravidade — ela vem do dano: a pessoa tabula para fora da tela sem saber onde está) · **Tipo:** interface
- **Correção proposta:** `.dentro{visibility:hidden}` e `.dentro.no{visibility:visible}`, junto com a transição que já existe; ou `inert` no elemento enquanto fechado.
- **Fonte:** fora da bibliografia

### [M1] Os tópicos do CV ficam a 13,5 px no celular
- **Gravidade:** Médio (ofício)
- **Critério:** LEG-01 — 16 px como piso em tela
- **Medido × esperado:** 13,5 px em 390 px de largura × 16 px. No computador sobe para 16 px e passa
- **Evidência:** `.dentro ul li` — são 40 tópicos, o grosso do CV
- **Base:** estilo computado · **Força da fonte:** Autor (Rutter, SxSW 2013, slide 27; Santa Maria, p. 89–90) · **Tipo:** legibilidade
- **Correção proposta:** `clamp(13.5px,3.4vw,16px)` → `clamp(15px,3.6vw,16px)`
- **Fonte:** Santa Maria, *On Web Typography*, p. 89–90

### [M2] A faixa de contato fica a 9,75 px no celular
- **Gravidade:** Médio (ofício)
- **Critério:** LEG-06 — texto secundário; a Biblioteca não dá piso numérico
- **Medido × esperado:** 9,75 px × "não menor que o necessário para a distância"; contraste passa (6,55:1)
- **Evidência:** `.faixa.baixa` — e é onde moram o e-mail, o CV e o LinkedIn, ou seja, a única navegação da página
- **Base:** estilo computado · **Força da fonte:** Autor · **Tipo:** legibilidade
- **Correção proposta:** `clamp(9px,2.5vw,12.5px)` → `clamp(11px,2.8vw,12.5px)`
- **Fonte:** Santa Maria, p. 89–90

### [M3] A coluna de datas do CV passa raspando no contraste
- **Gravidade:** Médio
- **Critério:** LEG-37 / LUX-39
- **Medido × esperado:** 4,70:1 sobre papel, **4,25:1** sobre o traço × 4,5:1. `.dentro .quando`, 11,5 px, #6f6a5c
- **Evidência:** a coluna "January 2025 — present" de cada entrada
- **Base:** estilo computado; fundo efetivo Inferido · **Força da fonte:** Segunda mão · **Tipo:** legibilidade
- **Correção proposta:** #6f6a5c → **#635e52** (5,62:1 / 5,08:1), o mesmo tom do [A2]
- **Fonte:** Yablonski, p. 101

### [M4] O rótulo da seção é menor que o título que ele encabeça
- **Gravidade:** Médio (ofício)
- **Critério:** OFI-28 — escala declarada e mantida; GRA-35 — hierarquia de tamanho
- **Medido × esperado:** `h3` da seção a 11 px × `b` do cargo a 23 px no computador. O continente é cinco vezes menor que o conteúdo
- **Evidência:** "EXPERIENCE" sobre "Head of Growth · Lets Fly"
- **Base:** estilo computado · **Força da fonte:** Autor · **Tipo:** ofício
- **Correção proposta:** é uma convenção de rótulo (*eyebrow*) e funciona porque o fio separa as seções. Se incomodar, o caminho é subir o `h3` para ~14 px com o mesmo peso, não baixar o cargo.
- **Fonte:** Bringhurst via Santa Maria, p. 126–128

### [M5] "CLICK HERE" a 10 px
- **Gravidade:** Médio (ofício)
- **Critério:** LEG-06
- **Medido × esperado:** 10 px, caixa-alta, `letter-spacing:1,6px` × sem piso na Biblioteca
- **Evidência:** `.cartao i`, dentro da moldura de lápis
- **Base:** estilo computado · **Força da fonte:** Autor · **Tipo:** ofício
- **Correção proposta:** 11,5 px. A moldura cresce junto, porque é `border-image`.
- **Fonte:** Santa Maria, p. 89–90

## Baixos agrupados

- Alvo do violão com 40 px de largura no celular → resolvido pelo mesmo `min-width:44px` do [A3] (LUX-01, Segunda mão).
- `sala.html#toque` é um atalho de conferência e está em produção → tirar antes de divulgar o endereço (sem critério; higiene).
- `<meta name="robots" content="noindex">` continua na página → enquanto estiver lá, ninguém acha o site pesquisando seu nome (sem critério; decisão sua).
- A faixa de baixo tem três links colados em 390 px (e-mail, CV, LinkedIn) com 9,75 px → o espaçamento entre alvos vizinhos (≥ 8 dp, LUX-03, Segunda mão) não foi medido; some se o [M2] for aplicado.

## O que passou

- **Medida da linha:** 50 caracteres no texto corrido e 72 nos tópicos, no computador — dentro de 45 a 75 (LEG-12, Autor). Não mexa na largura da folha ao consertar o corpo.
- **Entrelinha:** 1,42 no corpo e 1,55 nos tópicos — dentro de 1,2 a 1,8 (LEG-08, Autor).
- **Hierarquia do CV:** título 56 px → cargo 23 px → corpo 20 px → datas 11,5 px. Quatro degraus claros, sem empate (GRA-34, Autor).
- **Contraste do corpo:** 8,18:1 sobre papel e 7,40:1 sobre o traço (Segunda mão). O texto que importa está folgado.
- **Duas famílias** (Fraunces e Archivo) mais a sua letra como imagem — dentro do que Santa Maria recomenda (1 a 2) (OFI-37, Autor).
- **O nome tem texto alternativo** e as cinco portas têm `aria-label`.

## Não dá para verificar com esta entrada

- **Anel de foco por teclado** (LUX-41, Segunda mão, sem espessura nem contraste na Biblioteca). Medi com `.focus()` programático, que não dispara `:focus-visible` — o resultado "sem contorno" não vale. Pedido: navegar a página inteira com Tab e fotografar cada parada.
- **Texto ampliado a 200%** (LEG-40). Todo o corpo usa `clamp()` com `vw`, que não responde ao aumento de fonte do navegador. Pedido: abrir com zoom de texto em 200% e ver o que quebra.
- **Contraste de não-texto**: o fio das seções (#ddd6c5), o sublinhado dos links do CV (#b9b2a1) e a borda da moldura. A Biblioteca só cobre texto; o limiar viria da norma, como fonte Externa.
- **Leitura em aparelho real**: tudo foi medido em navegador de computador emulando 390 px. Densidade de pixel, brilho e tamanho físico mudam o que se lê.
- **Densidade e carga** do CV (5.262 px de altura no celular, INF-01 a INF-08): nenhuma fonte da Biblioteca mede. Só teste com pessoas responde se a pessoa rola até o fim.

## Perguntas abertas

- **Medida da linha: 13, ~35 ou 45 a 75 caracteres** (`criterios-legibilidade.md`, PA-1). Os 50 e 72 caracteres daqui passam na faixa de Bringhurst, que é preferência, não velocidade. Se a meta fosse velocidade de leitura, a régua seria outra.
- **Texto pequeno como escolha de marca.** As faixas a 9,75 px e o "CLICK HERE" a 10 px são coerentes com o desenho a lápis — discrição é parte da peça. A Biblioteca não dá piso para texto secundário, então a decisão é sua, não do critério.

## Risco de liso

Não se aplica: o objeto já carrega contraste deliberado além da grade (`GRA-59`) — a ilustração a
lápis, a sua letra no topo, a moldura desenhada à mão. Fonte conferida; ponte Inferida.

## Próxima verificação recomendada

Abrir a página num celular de verdade e percorrê-la só com o Tab. As duas dúvidas mais caras que
sobraram — anel de foco e comportamento com texto ampliado — se resolvem nessa única passada, e
nenhuma das duas dá para responder de dentro do emulador.
