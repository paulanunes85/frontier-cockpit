"""
Client UBB executive action-proposal PDF (ms-identity editorial).
Requires template_css.py, components.py, charts.py from the
ms-identity-editorial-brief skill assets in the same directory,
plus weasyprint installed. Fill the metadata block and the chapter
copy for the client. PT-BR copy must carry full accents.
This file is the validated BTG v1.0.0 build; treat it as the master:
replace client name, numbers, charts data and dates, keep the structure.
"""
#!/usr/bin/env python3
import pathlib, sys
# editorial deps ship in assets/editorial/ next to this template
_here = pathlib.Path(__file__).parent
for cand in (_here/'editorial', _here):
    if (cand/'template_css.py').exists():
        sys.path.insert(0, str(cand)); break
from template_css import CSS
from components import (
    ms_logo, gh_logo, runhead, folio, kicker, section_header,
    sidebar, pull_quote, data_card, data_strip,
    callout, callouts, chart_card, hero_number, bullets,
)
from charts import chart_line, chart_h_bar, chart_donut

TOPIC          = "Proposta_Acao_UBB_BTG"
ISSUE          = 1
COVER_EYEBROW  = "GitHub Copilot · Usage-Based Billing · Banco BTG Pactual"
COVER_TITLE    = "A conta sob controle<br>antes de setembro.<br><em>Nossa proposta de ação.</em>"
COVER_LEDE     = ("A transição do GitHub Copilot para cobrança por consumo não muda o preço do assento. "
                  "Muda o que fica visível: o uso de IA acima do que já vem incluído. Este documento apresenta "
                  "os três cenários auditados de abril de 2026, a janela promocional que protege a fatura ate "
                  "1 de setembro, e o plano conjunto, comercial e técnico, que mantem o orçamento previsível "
                  "enquanto a adoção continua crescendo.")
PERIOD_LINE    = "<strong>Base auditada:</strong> abril de 2026"
EXTRA_META     = "<strong>Escopo:</strong> 4.131 assentos · Enterprise &nbsp;·&nbsp; <strong>Emitido:</strong> 2026-06-12"
RUNHEAD_TITLE  = "BTG Pactual, proposta de ação UBB"
CLOSE_QUOTE    = "Custo por consumo não se preve com precisao. Se controla com arquitetura, governança e um plano com datas."
VERSION        = "v1_0_0"
DATE           = "2026-06-12"
LOCALE         = "ptBR"

HERE = pathlib.Path(__file__).parent
OUT_BASE  = f"{TOPIC}_Editorial_{VERSION}_{DATE}_{LOCALE}"
OUT_PRINT = HERE / f"{OUT_BASE}_print.html"
OUT_HTML  = HERE / f"{OUT_BASE}.html"
OUT_PDF   = HERE / f"{OUT_BASE}.pdf"

LEDE_CARDS = [
    data_card("Hoje (modelo PRU)", "US$ 130.948", "por mês · base abr/2026", accent="blue"),
    data_card("Com promoção (jun-ago)", "US$ 137.624", "por mês · +5% vs hoje", accent="green"),
    data_card("Sem ação (set+)", "US$ 231.704", "por mês · +77% vs hoje", accent="red"),
    data_card("Salto de setembro", "+US$ 94 mil", "por mês, no fim da promoção", accent="yellow"),
]

TOC_ENTRIES = [
    ("01", "Resumo executivo",        "A tese e os quatro números que importam",        "03"),
    ("02", "O que mudou, de fato",    "Preço do assento igual; consumo agora visível",  "04"),
    ("03", "Os três cenários",        "Hoje, com promoção e sem ação, lado a lado",     "05"),
    ("04", "Onde está o custo",       "Mix de modelos e o peso da releitura de contexto","06"),
    ("05", "Trilha comercial",        "Pre-Purchase Plan e a janela de decisão",        "07"),
    ("06", "Trilha técnica, R1 a R7", "O programa de eficiência e a curva de resgate",  "08"),
    ("07", "Plano de 6 meses",        "Cadencia, governança e o checkpoint de setembro","09"),
    ("08", "Próximos passos",         "O que pedimos e o que entregamos",               "10"),
    ("A",  "Apêndice",                "Cenários anualizados, premissas e fontes",       "11"),
]

MESES = ["Jun","Jul","Ago","Set","Out","Nov","Dez","Jan","Fev","Mar","Abr","Mai"]
SEM_ACAO   = [138,138,138,232,232,232,232,232,232,232,232,232]
COM_PLANO  = [138,138,138,221,212,203,194,188,182,179,177,176]
# com plano: licenças 127k + overage com programa (ramp curve) in US$ k

MIX_ROWS = [
    ("Modelo frontier A", 100516),
    ("Modelo premium B",   59960),
    ("Modelo frontier C",  19004),
    ("Modelo premium D",   10514),
    ("Modelo standard E",   9623),
    ("Modelo standard F",    9297),
    ("Demais 24 modelos",  22790),
]

def html_open():
    return f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8">
<title>{RUNHEAD_TITLE}</title>
<meta name="author" content="Frontier Cockpit Team, Software Global Black Belt">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>"""

def page_cover():
    return f"""
<section class="page" style="padding:0">
  <div class="cover">
    <div class="cover-top">
      <span class="left">{ms_logo(14)}Frontier Cockpit Team &nbsp;|&nbsp; Software Global Black Belt</span>
      <span>Vol. 01 &nbsp;/&nbsp; FY27 &nbsp;/&nbsp; Confidencial · BTG Pactual</span>
    </div>
    <div class="cover-mid">
      <div class="eyebrow">{COVER_EYEBROW}</div>
      <h1 class="title">{COVER_TITLE}</h1>
      <p class="lede">{COVER_LEDE}</p>
    </div>
    <div class="cover-bottom">
      <div class="cover-issue"><strong>Edição {ISSUE:02d}.</strong> {PERIOD_LINE}<br>{EXTRA_META}</div>
      <div class="cover-by"><span class="name">Frontier Cockpit Team</span>Software Global Black Belt<br>frontier-cockpit@example.com</div>
    </div>
    <div class="cover-bar">
      <i style="background:#F25022"></i><i style="background:#7FBA00"></i>
      <i style="background:#00A4EF"></i><i style="background:#FFB900"></i>
    </div>
  </div>
</section>"""

def page_masthead():
    toc = "".join(f'<li><span class="n">{n}</span><span class="t">{t}<span>{d}</span></span><span class="p">{p}</span></li>'
                  for (n,t,d,p) in TOC_ENTRIES)
    return f"""
<section class="page">
  {runhead(RUNHEAD_TITLE, "Sumário")}
  <div style="padding-top:11mm">
    <div class="kicker">Da Software Global Black Belt para o time BTG Pactual</div>
    <h2 class="mt-title">Um documento de decisão, não de venda: os números, as opções e um plano com datas.</h2>
    <p class="mt-deck">Oito capítulos e um apêndice. Os números vem do relatório oficial de billing do GitHub de abril de 2026 e sao os mesmos que sustentam o kit de transição compartilhado com o time. Cada cenário e rastreável as premissas do apêndice.</p>
  </div>
  <div class="mt-grid">
    <div><div class="toc-h">Nesta edição</div><ol class="toc-l">{toc}</ol></div>
    <div>
      {sidebar("Como ler", "Comece pelos quatro números do resumo. Depois o capítulo 3, os cenários, e o capítulo 8, o que decidir ate setembro. O resto e evidência.")}
      <div style="margin-top:5mm">{sidebar("A tese, em uma linha", "O preço do assento não mudou; o consumo acima do incluído agora e visível, e ha uma janela até 1 de setembro para decidir com vantagem.", accent="red")}</div>
    </div>
  </div>
  {folio(2, "Sumário")}
</section>"""

def page_lede():
    return f"""
<section class="page tint">
  {runhead(RUNHEAD_TITLE, "Capítulo 01, Resumo executivo")}
  <div style="padding-top:12mm">
    {section_header("Capítulo 01", "Resumo executivo", "Quatro números decidem esta conversa.", bar=True)}
    <div class="two-col">
      <p class="body"><strong style="color:var(--ink)">A mudança não é de preço, é de visibilidade.</strong> As licenças do BTG Pactual seguem em US$ 127.249 por mês, com os mesmos US$ 19 e US$ 39 por assento. O que muda em junho é que o consumo de IA acima do que já vem incluído no assento passa a ser medido e cobrado, em vez de degradar silenciosamente a experiência como no modelo antigo.</p>
      <p class="body">O consumo auditado de abril foi de US$ 231.704 em tokens, 1,82 vez o pool incluído. A promoção de 90 dias amplia o pool e segura a fatura em US$ 137.624 por mês, apenas 5% acima de hoje, até 1 de setembro de 2026.</p>
      <p class="body">Sem decisão até lá, a fatura salta cerca de US$ 94 mil em um único mês. Com o plano desta proposta, trilha comercial e trilha técnica em paralelo, a exposição anual cai na origem, por eficiência, sem reduzir a adoção.</p>
    </div>
    {pull_quote("Adoção crescendo 23% ao mês não é o problema. É o ativo. O plano protege o orçamento sem frear o time.", "A leitura correta do momento")}
    {data_strip(LEDE_CARDS)}
  </div>
  {folio(3, "Resumo executivo")}
</section>"""

def ch(num, label, slug, headline, body, name, tinted=False):
    cls = " tint" if tinted else ""
    return f"""
<section class="page{cls}">
  {runhead(RUNHEAD_TITLE, f"{label}, {slug}")}
  <div style="padding-top:12mm">
    {section_header(label, slug, headline)}
    {body}
  </div>
  {folio(num, name)}
</section>"""

def page_close():
    ms_big = ('<svg width="28mm" height="28mm" viewBox="0 0 17 17" xmlns="http://www.w3.org/2000/svg">'
              '<rect x="0" y="0" width="8" height="8" fill="#F25022"/><rect x="9" y="0" width="8" height="8" fill="#7FBA00"/>'
              '<rect x="0" y="9" width="8" height="8" fill="#00A4EF"/><rect x="9" y="9" width="8" height="8" fill="#FFB900"/></svg>')
    return f"""
<section class="page dark">
  <div class="close">
    <div class="marks">{ms_big}{gh_logo("28mm")}</div>
    <div class="lbl">Microsoft &nbsp;+&nbsp; GitHub</div>
    <div class="q">{CLOSE_QUOTE}</div>
    <div class="rule"></div>
    <div class="sig">Fim do documento</div>
  </div>
</section>"""

# ----- chapter bodies -----
body2 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">O modelo antigo nunca foi ilimitado.</strong> O PRU tinha um teto, só que opaco: ao bater no limite a experiência degradava sem aviso e sem fatura. O novo modelo troca o limite invisível por um medidor visível, com pool de créditos incluído em cada assento e compartilhado entre toda a organização.</p>
  <p class="body">Esse pooling importa. Usuários leves financiam usuários pesados dentro do mesmo pool, nenhum crédito individual expira, e a cobertura real do consumo do BTG é de 55%, contra cerca de 34% se cada usuário tivesse um balde isolado. Sao aproximadamente US$ 48 mil por mês que o pooling já evita hoje.</p>
</div>
{callouts([
  callout("INALTERADO", "Preço por assento", "US$ 19 Business e US$ 39 Enterprise, os mesmos valores. Licenças seguem em US$ 127.249 por mês.", accent="blue"),
  callout("NOVO", "Consumo visível", "Uso de IA acima do pool incluído aparece na fatura a US$ 0,01 por crédito, com telemetria por organização.", accent="yellow"),
  callout("PROTECAO", "Promoção de 90 dias", "De junho a agosto o pool incluído quase dobra: 3.000 créditos por assento Business e 7.000 por Enterprise.", accent="green"),
])}
{sidebar("Por que a fatura cresceu, entao", "Não foi reajuste. O consumo de IA do BTG cresceu 268% em dez meses, sinal de adoção saudável. O que muda e que esse volume agora tem medidor, e medidor se governa.")}
"""

curve = chart_line(MESES, [
    {"label":"Sem ação (US$ mil/mês)", "data":SEM_ACAO, "color":"#F25022", "fill":True},
    {"label":"Com o plano desta proposta", "data":COM_PLANO, "color":"#00A4EF"},
], w=560, h=300)
body3 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">Três cenários, uma janela.</strong> Hoje o BTG paga US$ 130.948 por mês no modelo antigo. Com a promoção ativa, a fatura projetada é US$ 137.624, práticamente estável. Quando a promoção expira em 1 de setembro, o consumo atual sobre o pool padrão leva a conta a US$ 231.704 por mês, um salto de US$ 94 mil de uma vez.</p>
  <p class="body">A linha azul mostra o mesmo período com o plano em execução: o programa de eficiência amadurece mês a mês e dobra a curva para baixo, sem reduzir assentos nem frear a adoção. A diferença acumulada entre as duas linhas no ano fiscal é de aproximadamente US$ 495 mil.</p>
</div>
{chart_card("A curva de setembro", "Fatura mensal projetada, US$ mil, jun/26 a mai/27", curve)}
{sidebar("Leitura do gráfico", "O degrau vermelho em setembro é o fim da promoção com o consumo de hoje. A linha azul não depende de desconto: é eficiência técnica, que reduz a conta na origem.", accent="red")}
"""

mix = chart_h_bar(MIX_ROWS, "#00A4EF", w=560, h=270, pad_l=150)
body4 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">O custo tem endereço.</strong> Dois modelos de ponta concentram 69% da fatura de tokens de abril. E 83,5% de todo o volume de tokens é releitura de contexto: o mesmo material reapresentado ao modelo a cada interação. Esses dois fatos definem onde o programa de eficiência ataca primeiro.</p>
  <p class="body">Concentração em modelos caros se trata com política de roteamento, a tarefa certa no modelo certo. Releitura se trata com curadoria de contexto e cache de prefixos estáveis. Nenhuma das duas medidas reduz a qualidade do trabalho; ambas reduzem o desperdicio.</p>
</div>
{chart_card("Mix de modelos, abril de 2026", "Custo de tokens por classe de modelo, US$", mix)}
{sidebar("Por que nomes genéricos", "As classes acima preservam o detalhe por fornecedor para a conversa técnica. O kit de transição compartilhado com o time traz o mix completo, modelo a modelo.")}
"""

body5 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">A trilha comercial tem nome: Pre-Purchase Plan.</strong> O P3 é a compra antecipada de créditos de consumo com desconto por faixa de compromisso. Ele converte um custo variável imprevisível em um valor contratado, com governança de queima e visibilidade mensal.</p>
  <p class="body">A faixa publicada parte de 15%. Para o perfil de consumo do BTG, recomendamos avaliar condições acima da tabela, sujeitas a elegibilidade e aprovação interna, de modo que o pacote supere o desconto Azure já contratado e faca sentido financeiro imediato.</p>
</div>
{callouts([
  callout("O QUE E", "Compromisso com desconto", "Creditos pre-comprados, queimados conforme o uso, com faixas de desconto crescentes por volume.", accent="blue"),
  callout("CRITERIO", "Superar o ACD atual", "A proposta só se sustenta se o desconto efetivo superar o Azure Commitment Discount vigente do BTG. Esse é o nosso critério, declarado.", accent="yellow"),
  callout("JANELA", "Decidir antes de setembro", "Fechar o P3 dentro da janela promocional evita pagar overage cheio enquanto o contrato tramita.", accent="red"),
])}
{sidebar("O que não prometemos", "Condições acima da tabela dependem de aprovação e elegibilidade. Trabalhamos com faixas e critérios declarados, nunca com número garantido antes da aprovação.", accent="red")}
"""

body6 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">A trilha técnica vale mais que o desconto.</strong> São sete alavancas de eficiência, R1 a R7, da contenção de output ao roteamento de modelos, da curadoria de contexto ao cache, dos primitivos de repositório aos orçamentos com alerta. Um início enxuto entrega 20 a 30% de redução de consumo; um programa maduro, 55 a 70%. Sempre faixa com fonte, nunca promessa.</p>
  <p class="body">Aplicada a curva de maturação típica, a configuração enxuta já produz cerca de US$ 495 mil de resgate no ano fiscal, redução na origem, que não custa nada ao BTG além de disciplina de engenharia, e que nos ajudamos a implantar.</p>
</div>
{callouts([
  callout("R1 · R2", "Output e roteamento", "Blocos de instrução contra verbosidade; política tarefa-modelo com início no modelo leve. Atacam a fatura inteira.", accent="red"),
  callout("R4 · R5", "Contexto e cache", "Contexto enxuto por turno e prefixos estáveis em cache. Atacam os 83,5% de releitura.", accent="blue"),
  callout("R6 · R7", "Primitivos e orçamentos", "Prompts e agentes versionados no repositório; tetos com alerta em 80%. Sustentam o ganho no tempo.", accent="green"),
])}
{hero_number("Resgate projetado no ano fiscal", "US$ 495 mil", "Composição", "eficiência técnica, sem depender de desconto")}
"""

body7 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">Execucao em cadencia, com uma trava.</strong> O plano roda em três janelas de 30 dias: baseline e governança, instrumentação, otimização. Encontros quinzenais de acompanhamento e um checkpoint mensal conjunto. A revisão de setembro é a trava do plano: a promoção expira, o overage real aparece, e decidimos juntos os próximos passos com dados, não com projecao.</p>
  <p class="body">A governança acompanha três camadas de métrica: custo sob controle, fundação construida, valor organizacional entregue. Orçamentos por usuário e por centro de custo, com alerta em 80% do teto, impedem o pico do loop descontrolado sem cortar o regime de trabalho.</p>
</div>
{callouts([
  callout("DIAS 1-30", "Baseline e governança", "Projecao validada, allowlist de modelos publicada, orçamentos no piloto, time treinado no que muda.", accent="blue"),
  callout("DIAS 31-60", "Instrumentação", "Cache em producao, painel de FinOps no ar, revisão semanal do mix de modelos.", accent="green"),
  callout("DIAS 61-90", "Otimização e revisão", "Primitivos publicados, agentes governados, pacote de evidências para o checkpoint de setembro.", accent="yellow"),
])}
{sidebar("O checkpoint de setembro", "Data marcada: primeira semana de setembro de 2026. Pauta: overage real versus projetado, marcos do programa, e a decisão comercial com os números na mesa.", accent="red")}
"""

body8 = f"""
<div class="two-col">
  <p class="body"><strong style="color:var(--ink)">O que pedimos ao BTG Pactual.</strong> Três nomes: um patrocinador executivo, um ponto focal de plataforma e um ponto focal de FinOps. Acesso ao painel de billing da organização. E uma data na agenda para o kickoff do programa, dentro de junho, para aproveitar a janela promocional inteira.</p>
  <p class="body"><strong style="color:var(--ink)">O que a Microsoft entrega.</strong> O kit de transição completo com motor de cenários e acompanhamento, o programa R1 a R7 com enablement do time, a estruturacao da proposta comercial com critérios declarados, e presenca quinzenal até o checkpoint de setembro.</p>
</div>
{bullets([
  "<strong>Semana 1:</strong> kickoff, baseline validada e allowlist de modelos publicada.",
  "<strong>Semana 4:</strong> orçamentos ativos no piloto e painel de FinOps no ar.",
  "<strong>Semana 8:</strong> cache e curadoria de contexto em producao nos repositórios de maior consumo.",
  "<strong>Semana 12:</strong> pacote de revisão de setembro pronto, com overage real versus projetado.",
  "<strong>Primeira semana de setembro:</strong> checkpoint conjunto e decisão comercial com dados.",
])}
{pull_quote("Nenhuma decisão precisa ser tomada no escuro. A janela existe exatamente para decidir com vantagem.", "Próximo passo: agendar o kickoff")}
"""

# appendix
def page_appendix():
    rows = [
        ("Hoje, modelo PRU", "130.948", "1.571.376", "base auditada de abril de 2026"),
        ("Com promoção, jun-ago", "137.624", "1.651.488", "+5% vs hoje, pool promocional"),
        ("Sem ação, set em diante", "231.704", "2.780.448", "+77% vs hoje, pool padrão"),
        ("Com o plano, regime maduro", "~176.000", "~2.100.000", "eficiência técnica, faixa enxuta"),
    ]
    trs = "".join(f"<tr><td>{a}</td><td style='text-align:right'>{b}</td><td style='text-align:right'>{c}</td><td>{d}</td></tr>" for a,b,c,d in rows)
    return f"""
<section class="page">
  {runhead(RUNHEAD_TITLE, "Apêndice, cenários e premissas")}
  <div style="padding-top:12mm">
    {section_header("Apêndice", "Cenários e premissas", "Cada número, sua origem.")}
    <table class="ed-table">
      <thead><tr><th>Cenário</th><th style="text-align:right">US$/mês</th><th style="text-align:right">US$/ano</th><th>Nota</th></tr></thead>
      <tbody>{trs}</tbody>
    </table>
    {sidebar("Fontes", "Relatório oficial de billing do GitHub Copilot, mês fiscal abril de 2026. Tabela de planos publicada do GitHub Copilot Business e Enterprise. Faixas de eficiência R1 a R7 documentadas com a mecânica oficial do produto. Valores promocionais e datas: comunicação oficial da promoção de 90 dias, expiração em 2026-09-01.")}
    <div style="margin-top:5mm">{sidebar("Premissas declaradas", "Cenários assumem o consumo de abril constante; o crescimento recente de 23% ao mês torna os cenários sem ação conservadores. A curva com plano usa maturação típica de programa e faixa enxuta de 20 a 30% de redução. Condições comerciais acima da tabela publicada dependem de elegibilidade e aprovação.", accent="yellow")}</div>
  </div>
  {folio(11, "Apêndice")}
</section>"""

def render():
    H = [html_open(), page_cover(), page_masthead(), page_lede()]
    H.append(ch(4, "Capítulo 02", "O que mudou, de fato", "O preço do assento e o mesmo. O medidor e novo.", body2, "O que mudou"))
    H.append(ch(5, "Capítulo 03", "Os três cenários", "A janela fecha em 1 de setembro.", body3, "Os três cenários", tinted=True))
    H.append(ch(6, "Capítulo 04", "Onde está o custo", "Dois modelos, 69% da fatura. Releitura, 83,5% do volume.", body4, "Onde está o custo"))
    H.append(ch(7, "Capítulo 05", "Trilha comercial", "Compromisso com desconto, com critério declarado.", body5, "Trilha comercial", tinted=True))
    H.append(ch(8, "Capítulo 06", "Trilha técnica, R1 a R7", "Eficiência que vale mais que o desconto.", body6, "Trilha técnica"))
    H.append(ch(9, "Capítulo 07", "Plano de 6 meses", "Cadencia quinzenal, checkpoint em setembro.", body7, "Plano de 6 meses", tinted=True))
    H.append(ch(10, "Capítulo 08", "Próximos passos", "Três nomes, um acesso, uma data.", body8, "Próximos passos"))
    H.append(page_appendix())
    H.append(page_close())
    H.append("</body></html>")
    return "".join(H)

html = render()
OUT_PRINT.write_text(html, encoding="utf-8")
OUT_HTML.write_text(html, encoding="utf-8")
import weasyprint
weasyprint.HTML(filename=str(OUT_PRINT)).write_pdf(target=str(OUT_PDF))
print("ok:", OUT_PDF.name)
