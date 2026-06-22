# -*- coding: utf-8 -*-
"""BTG executive deck, I18N content (3 locales) + notes s1..s14."""

PT = {
 "meta": {"title": "BTG Pactual, o programa de seis meses"},
 "labels": {"author": "Autora", "role": "Função", "duration": "Cliente", "date": "Data"},
 "cover": {
   "eyebrow": "GitHub Copilot · Usage-Based Billing · Banco BTG Pactual",
   "part1": "O programa de seis meses.",
   "keyword1": "Eficiência, governança e parceria até dezembro.",
   "subtitle": "Como vamos trabalhar juntos na transição para cobrança por consumo: o resgate técnico de seis meses, o apoio comercial em paralelo e o apoio estratégico de GBB e dos times Microsoft e GitHub para construir a fundação e as melhores práticas.",
   "duration": "Banco BTG Pactual S.A."
 },
 "agenda": {
   "eyebrow": "Agenda",
   "title": "Quatro partes, um plano com datas.",
   "item1": "O momento, três cenários e a janela que fecha em 1 de setembro",
   "item2": "O trabalho até aqui, análise auditada, kit de transição e proposta de ação",
   "item3": "O programa de seis meses, a curva de resgate de US$ 495 mil",
   "item4": "Duas trilhas em paralelo, apoio comercial e apoio estratégico de GBB"
 },
 "p1": {"eyebrow": "Parte 01", "title": "O momento.", "sub": "A adoção cresceu 23% ao mês. A promoção segura a fatura até 1 de setembro de 2026. Depois disso, decide quem se preparou."},
 "moment": {
   "eyebrow": "A janela de setembro",
   "hero": "+US$ 94k",
   "title": "Sem decisão, a fatura salta US$ 94 mil em um único mês.",
   "body": "Hoje o BTG paga US$ 130.948 por mês. Com a promoção ativa, US$ 137.624, apenas 5% acima. Quando a promoção expira, o consumo atual sobre o pool padrão leva a conta a US$ 231.704 por mês.",
   "s1Label": "Hoje (PRU)", "s1": "US$ 130.948/mês",
   "s2Label": "Com promoção (jun-ago)", "s2": "US$ 137.624/mês",
   "s3Label": "Sem ação (set+)", "s3": "US$ 231.704/mês"
 },
 "p2": {"eyebrow": "Parte 02", "title": "O trabalho até aqui.", "sub": "Nada aqui é projeção solta. Três entregas auditadas sustentam cada número desta conversa."},
 "deliver": {
   "eyebrow": "Entregas concluídas",
   "title": "Três peças, um conjunto coerente.",
   "c1Label": "Análise", "c1Title": "Análise de orçamento auditada",
   "c1Body": "Base oficial de billing de abril de 2026, cenários, curva de setembro, mix de modelos e trajetória de consumo. Trilíngue, para o time da conta.",
   "c2Label": "Motor", "c2Title": "Kit de transição dinâmico",
   "c2Body": "Planilha enterprise com motor de cenários, simulador das alavancas R1 a R7, forecast, ROI, plano de ação e KPIs. Tudo recalcula a partir de uma única aba de entrada.",
   "c3Label": "Proposta", "c3Title": "Proposta de ação executiva",
   "c3Body": "Documento editorial enviado ao BTG: os três cenários, as duas trilhas, o plano de seis meses e os próximos passos com datas."
 },
 "p3": {"eyebrow": "Parte 03", "title": "O programa de seis meses.", "sub": "O resgate não depende de desconto. É eficiência na origem, construída em fases, com um checkpoint que decide tudo."},
 "program": {
   "eyebrow": "Roadmap de seis meses",
   "title": "Três fases, uma trava em setembro.",
   "ph1Label": "Meses 1 e 2", "ph1Title": "Fundação e instrumentação",
   "ph1Body": "Baseline validada, allowlist de modelos, orçamentos com alerta no piloto, cache em produção, painel de FinOps no ar, time treinado.",
   "ph2Label": "Mês 3", "ph2Title": "Checkpoint de setembro",
   "ph2Body": "A promoção expira, o overage real aparece. Revisão conjunta: overage real versus projetado, marcos do programa e a decisão comercial com dados na mesa.",
   "ph3Label": "Meses 4 a 6", "ph3Title": "Maturação do resgate",
   "ph3Body": "Primitivos publicados, agentes governados, mix de modelos sob revisão semanal. A curva dobra para baixo mês a mês até o regime maduro."
 },
 "redeem": {
   "eyebrow": "O resgate",
   "hero": "US$ 495k",
   "title": "US$ 495 mil de resgate projetado no ano fiscal.",
   "body": "Aplicada a curva de maturação típica, a configuração enxuta das alavancas R1 a R7 reduz o consumo na origem. Não custa um dólar de desconto e não reduz um assento. Um programa maduro alcança 55 a 70% de redução; trabalhamos com a faixa conservadora.",
   "kLabel": "Composição", "kValue": "eficiência técnica, sem depender de desconto"
 },
 "levers": {
   "eyebrow": "Alavancas de maior impacto",
   "title": "Onde o programa ataca primeiro.",
   "lead1": "As quatro alavancas que pegam as classes de token mais caras. Bandas oficiais do runbook, sempre faixa com fonte.",
   "eyebrow2": "Alavancas estruturais",
   "title2": "O que sustenta o ganho no tempo.",
   "lead2": "Tres alavancas que transformam o corte pontual em padrão permanente e protegem o orçamento.",
   "r1Label": "R1 · 40 a 70% do output", "r1Title": "Controle de output",
   "r1Body": "A saída custa ~4 a 5x o input por token. Blocos de instrução no copilot-instructions.md tornam a resposta direta (código ou diff) o padrão do repositório. Uma resposta típica cai de 400 a 600 tokens para 30 a 50 restrita a diff.",
   "r2Label": "R2 · 40 a 70% da conta", "r2Title": "Roteamento de modelos",
   "r2Body": "O preço por token varia duas ordens de grandeza entre a classe leve e a de fronteira. Modo Auto como padrão (mais 10% de desconto no chat), utility model para tarefas triviais, fronteira reservada para o que precisa. Dois modelos concentram 69% do custo do BTG.",
   "r3Label": "R4 · 40 a 80% do input", "r3Title": "Escopo de contexto",
   "r3Body": "O contexto é frequentemente 60%+ do input por turno. Disciplina de #-mentions, content exclusion e fim das mega-threads cortam o que entra. LLMLingua (Microsoft) comprimiu prompts em até 20x; a banda usada é conservadora.",
   "r4Label": "R5 · 30 a 50% do input", "r4Title": "Cache e memória",
   "r4Body": "83,5% do volume de tokens do BTG é releitura de contexto. Prefixos estáveis em cache não são reprocessados (leitura a 0,1x na Anthropic, 50% na OpenAI). Memória corta a reexplicação entre sessões.",
   "r5Label": "R6 · ganho composto", "r5Title": "Primitivos de repositório",
   "r5Body": "Instruções, agentes, prompts e hooks versionados no repositório, tratados como infraestrutura. Cada arquivo reduz reexplicação em todo pedido futuro: é o que transforma os cortes das outras alavancas em padrão permanente.",
   "r6Label": "R3 · rotina a custo zero", "r6Title": "Modelos locais (BYOK)",
   "r6Body": "Modelo local no VS Code (Ollama ou Foundry Local) roteado para o trabalho de rotina, a custo zero de AI Credits pela mecânica oficial do BYOK. Não se aplica a completions; participação de um dígito a ~15% conforme o mix.",
   "r7Label": "R7 · guard-rail de variância", "r7Title": "Orçamentos e medição",
   "r7Body": "Quatro níveis de budget, do limite individual ao failsafe da empresa, com alerta em 80%. ULB em disponibilidade geral desde 1 de junho. Não corta o regime de trabalho; impede que um loop de agente consuma o pool da unidade sozinho."
 },
 "p4": {"eyebrow": "Parte 04", "title": "Duas trilhas em paralelo.", "sub": "Enquanto a engenharia constrói eficiência, a trilha comercial garante que o contrato acompanhe. Nenhuma espera pela outra."},
 "tracks": {
   "eyebrow": "Comercial e estratégico",
   "title": "O apoio que cerca o programa pelos dois lados.",
   "leftLabel": "Trilha comercial",
   "leftTitle": "Reduzir o impacto do overage",
   "leftBody": "Um leque de opções a explorar, nada definido ainda: estender o crédito promocional ou negociar um desconto adicional nos três meses seguintes para suavizar o degrau de setembro, e, se fizer sentido para o BTG, avaliar um Pre-Purchase Plan ou condições via ACD. O caminho certo sai da conversa, com os números na mesa.",
   "rightLabel": "Trilha estratégica, GBB e times",
   "rightTitle": "Fundação e melhores práticas",
   "rightBody": "Software Global Black Belt com presença quinzenal de junho a dezembro: enablement do time, arquitetura de contexto e agentes, implantação das alavancas R1 a R7, fundação de FinOps com os times Microsoft e GitHub, e o pacote de evidências do checkpoint de setembro."
 },
 "who": {
   "eyebrow": "Papéis",
   "title": "Quem faz o quê, sem zona cinzenta.",
   "c1Label": "BTG Pactual", "c1Title": "Três nomes e uma data",
   "c1Body": "Patrocinador executivo, ponto focal de plataforma e ponto focal de FinOps. Acesso ao painel de billing e o kickoff agendado ainda em junho.",
   "c2Label": "Microsoft", "c2Title": "GBB e time da conta",
   "c2Body": "O programa R1 a R7 com enablement, o kit de transição vivo, a exploração das opções comerciais junto ao BTG e a cadência quinzenal ao longo dos seis meses, até dezembro.",
   "c3Label": "GitHub", "c3Title": "Produto e billing",
   "c3Body": "Telemetria oficial de consumo, a promoção de 90 dias, a tabela de planos e o suporte de produto para budgets, cache e governança."
 },
 "end": {
   "eyebrow": "Próximo passo",
   "title": "Kickoff em junho. Checkpoint em setembro. Parceria até dezembro.",
   "sub": "A janela existe exatamente para decidir com vantagem. Nenhuma decisão precisa ser tomada no escuro.",
   "contactLabel": "Contato", "nextLabel": "Próxima ação",
   "next": "Agendar o kickoff do programa dentro de junho de 2026"
 },
 "notes": {}
}

EN = {
 "meta": {"title": "BTG Pactual, the six-month program"},
 "labels": {"author": "Author", "role": "Role", "duration": "Client", "date": "Date"},
 "cover": {
   "eyebrow": "GitHub Copilot · Usage-Based Billing · Banco BTG Pactual",
   "part1": "The six-month program.",
   "keyword1": "Efficiency, governance and partnership through December.",
   "subtitle": "How we will work together through the usage-based billing transition: the six-month technical redemption, the commercial track in parallel, and the strategic support from GBB and the Microsoft and GitHub teams to build the foundation and best practices.",
   "duration": "Banco BTG Pactual S.A."
 },
 "agenda": {
   "eyebrow": "Agenda",
   "title": "Four parts, one plan with dates.",
   "item1": "The moment, three scenarios and the window that closes on September 1",
   "item2": "The work so far, audited analysis, transition kit and action proposal",
   "item3": "The six-month program, the US$ 495 thousand redemption curve",
   "item4": "Two parallel tracks, commercial support and GBB strategic support"
 },
 "p1": {"eyebrow": "Part 01", "title": "The moment.", "sub": "Adoption grew 23% a month. The promo holds the bill until September 1, 2026. After that, preparation decides."},
 "moment": {
   "eyebrow": "The September window",
   "hero": "+US$ 94k",
   "title": "Without a decision, the bill jumps US$ 94 thousand in a single month.",
   "body": "Today BTG pays US$ 130,948 per month. With the promo active, US$ 137,624, just 5% above. When the promo expires, current consumption over the standard pool takes the bill to US$ 231,704 per month.",
   "s1Label": "Today (PRU)", "s1": "US$ 130,948/mo",
   "s2Label": "With promo (Jun-Aug)", "s2": "US$ 137,624/mo",
   "s3Label": "No action (Sep+)", "s3": "US$ 231,704/mo"
 },
 "p2": {"eyebrow": "Part 02", "title": "The work so far.", "sub": "Nothing here is loose projection. Three audited deliverables back every number in this conversation."},
 "deliver": {
   "eyebrow": "Completed deliverables",
   "title": "Three pieces, one coherent set.",
   "c1Label": "Analysis", "c1Title": "Audited budget analysis",
   "c1Body": "Official April 2026 billing base, scenarios, the September curve, model mix and consumption trajectory. Trilingual, for the account team.",
   "c2Label": "Engine", "c2Title": "Dynamic transition kit",
   "c2Body": "Enterprise workbook with a scenario engine, the R1 to R7 lever simulator, forecast, ROI, action plan and KPIs. Everything recalculates from a single intake tab.",
   "c3Label": "Proposal", "c3Title": "Executive action proposal",
   "c3Body": "Editorial document sent to BTG: the three scenarios, the two tracks, the six-month plan and the next steps with dates."
 },
 "p3": {"eyebrow": "Part 03", "title": "The six-month program.", "sub": "The redemption does not depend on a discount. It is efficiency at the source, built in phases, with one checkpoint that decides everything."},
 "program": {
   "eyebrow": "Six-month roadmap",
   "title": "Three phases, one lock in September.",
   "ph1Label": "Months 1 and 2", "ph1Title": "Foundation and instrumentation",
   "ph1Body": "Validated baseline, model allowlist, budgets with alerts in the pilot, caching in production, FinOps dashboard live, team enabled.",
   "ph2Label": "Month 3", "ph2Title": "The September checkpoint",
   "ph2Body": "The promo expires, real overage shows up. Joint review: actual versus projected overage, program milestones and the commercial decision with data on the table.",
   "ph3Label": "Months 4 to 6", "ph3Title": "Redemption maturation",
   "ph3Body": "Primitives published, agents governed, model mix under weekly review. The curve bends down month by month into the mature regime."
 },
 "redeem": {
   "eyebrow": "The redemption",
   "hero": "US$ 495k",
   "title": "US$ 495 thousand of projected fiscal-year redemption.",
   "body": "Applied to the typical maturation curve, the lean configuration of the R1 to R7 levers reduces consumption at the source. It costs no discount dollars and removes no seats. A mature program reaches 55 to 70% reduction; we work with the conservative band.",
   "kLabel": "Composition", "kValue": "technical efficiency, no discount required"
 },
 "levers": {
   "eyebrow": "Highest-impact levers",
   "title": "Where the program attacks first.",
   "lead1": "The four levers that hit the most expensive token classes. Official bands from the runbook, always a sourced range.",
   "eyebrow2": "Structural levers",
   "title2": "What sustains the gain over time.",
   "lead2": "Three levers that turn a one-off cut into a permanent standard and protect the budget.",
   "r1Label": "R1 · 40 to 70% of output", "r1Title": "Output control",
   "r1Body": "Output costs ~4 to 5x input per token. Instruction blocks in copilot-instructions.md make the direct answer (code or diff) the repository default. A typical response drops from 400 to 600 tokens to 30 to 50 when restricted to a diff.",
   "r2Label": "R2 · 40 to 70% of the bill", "r2Title": "Model routing",
   "r2Body": "Price per token spans two orders of magnitude between the light and frontier class. Auto mode as default (plus 10% chat discount), utility model for trivial tasks, frontier reserved for what needs it. Two models concentrate 69% of BTG's cost.",
   "r3Label": "R4 · 40 to 80% of input", "r3Title": "Context scoping",
   "r3Body": "Context is often 60%+ of input per turn. #-mention discipline, content exclusion and the end of mega-threads cut what enters. LLMLingua (Microsoft) compressed prompts up to 20x; the band used is conservative.",
   "r4Label": "R5 · 30 to 50% of input", "r4Title": "Cache and memory",
   "r4Body": "83.5% of BTG's token volume is context re-reading. Stable cached prefixes are not reprocessed (cache read at 0.1x on Anthropic, 50% on OpenAI). Memory cuts re-explanation across sessions.",
   "r5Label": "R6 · compound gain", "r5Title": "Repository primitives",
   "r5Body": "Instructions, agents, prompts and hooks versioned in the repository, treated as infrastructure. Each file reduces re-explanation on every future request: this is what turns the other levers' cuts into a permanent standard.",
   "r6Label": "R3 · routine at zero cost", "r6Title": "Local models (BYOK)",
   "r6Body": "A local model in VS Code (Ollama or Foundry Local) routed to routine work, at zero AI Credit cost by the official BYOK mechanic. Does not apply to completions; single-digit to ~15% share depending on the mix.",
   "r7Label": "R7 · variance guardrail", "r7Title": "Budgets and measurement",
   "r7Body": "Four budget levels, from the individual cap to the enterprise failsafe, with alerts at 80%. ULB generally available since June 1. It does not cut the working regime; it prevents a single agent loop from consuming the unit's pool."
 },
 "p4": {"eyebrow": "Part 04", "title": "Two parallel tracks.", "sub": "While engineering builds efficiency, the commercial track keeps the contract in step. Neither waits for the other."},
 "tracks": {
   "eyebrow": "Commercial and strategic",
   "title": "Support that surrounds the program on both sides.",
   "leftLabel": "Commercial track",
   "leftTitle": "Soften the overage impact",
   "leftBody": "A set of options to explore, nothing fixed yet: extend the promotional credit or negotiate an additional discount over the next three months to soften the September step, and, if it fits BTG, evaluate a Pre-Purchase Plan or ACD-based terms. The right path comes out of the conversation, with the numbers on the table.",
   "rightLabel": "Strategic track, GBB and teams",
   "rightTitle": "Foundation and best practices",
   "rightBody": "Software Global Black Belt with biweekly presence from June to December: team enablement, context and agent architecture, R1 to R7 lever implementation, the FinOps foundation with the Microsoft and GitHub teams, and the September checkpoint evidence package."
 },
 "who": {
   "eyebrow": "Roles",
   "title": "Who does what, no gray zone.",
   "c1Label": "BTG Pactual", "c1Title": "Three names and a date",
   "c1Body": "Executive sponsor, platform focal point and FinOps focal point. Billing dashboard access and the kickoff scheduled within June.",
   "c2Label": "Microsoft", "c2Title": "GBB and account team",
   "c2Body": "The R1 to R7 program with enablement, the living transition kit, the exploration of commercial options with BTG and the biweekly cadence across the six months, through December.",
   "c3Label": "GitHub", "c3Title": "Product and billing",
   "c3Body": "Official consumption telemetry, the 90-day promo, the plan table and product support for budgets, caching and governance."
 },
 "end": {
   "eyebrow": "Next step",
   "title": "Kickoff in June. Checkpoint in September. Partnership through December.",
   "sub": "The window exists precisely so the decision is made with an advantage. No decision needs to be made in the dark.",
   "contactLabel": "Contact", "nextLabel": "Next action",
   "next": "Schedule the program kickoff within June 2026"
 },
 "notes": {}
}

ES = {
 "meta": {"title": "BTG Pactual, el programa de seis meses"},
 "labels": {"author": "Autora", "role": "Función", "duration": "Cliente", "date": "Fecha"},
 "cover": {
   "eyebrow": "GitHub Copilot · Usage-Based Billing · Banco BTG Pactual",
   "part1": "El programa de seis meses.",
   "keyword1": "Eficiencia, gobernanza y alianza hasta diciembre.",
   "subtitle": "Cómo vamos a trabajar juntos en la transición a la facturación por consumo: el rescate técnico de seis meses, el apoyo comercial en paralelo y el apoyo estratégico de GBB y de los equipos de Microsoft y GitHub para construir la fundación y las mejores prácticas.",
   "duration": "Banco BTG Pactual S.A."
 },
 "agenda": {
   "eyebrow": "Agenda",
   "title": "Cuatro partes, un plan con fechas.",
   "item1": "El momento, tres escenarios y la ventana que cierra el 1 de septiembre",
   "item2": "El trabajo hasta aquí, análisis auditado, kit de transición y propuesta de acción",
   "item3": "El programa de seis meses, la curva de rescate de US$ 495 mil",
   "item4": "Dos pistas en paralelo, apoyo comercial y apoyo estratégico de GBB"
 },
 "p1": {"eyebrow": "Parte 01", "title": "El momento.", "sub": "La adopción creció 23% al mes. La promoción sostiene la factura hasta el 1 de septiembre de 2026. Después, decide quién se preparó."},
 "moment": {
   "eyebrow": "La ventana de septiembre",
   "hero": "+US$ 94k",
   "title": "Sin decisión, la factura salta US$ 94 mil en un solo mes.",
   "body": "Hoy BTG paga US$ 130.948 por mes. Con la promoción activa, US$ 137.624, apenas 5% más. Cuando la promoción expira, el consumo actual sobre el pool estándar lleva la cuenta a US$ 231.704 por mes.",
   "s1Label": "Hoy (PRU)", "s1": "US$ 130.948/mes",
   "s2Label": "Con promoción (jun-ago)", "s2": "US$ 137.624/mes",
   "s3Label": "Sin acción (sep+)", "s3": "US$ 231.704/mes"
 },
 "p2": {"eyebrow": "Parte 02", "title": "El trabajo hasta aquí.", "sub": "Nada aquí es proyección suelta. Tres entregas auditadas sostienen cada número de esta conversación."},
 "deliver": {
   "eyebrow": "Entregas concluidas",
   "title": "Tres piezas, un conjunto coherente.",
   "c1Label": "Análisis", "c1Title": "Análisis de presupuesto auditado",
   "c1Body": "Base oficial de billing de abril de 2026, escenarios, la curva de septiembre, mix de modelos y trayectoria de consumo. Trilingüe, para el equipo de la cuenta.",
   "c2Label": "Motor", "c2Title": "Kit de transición dinámico",
   "c2Body": "Hoja enterprise con motor de escenarios, simulador de las palancas R1 a R7, forecast, ROI, plan de acción y KPIs. Todo recalcula desde una única pestaña de entrada.",
   "c3Label": "Propuesta", "c3Title": "Propuesta de acción ejecutiva",
   "c3Body": "Documento editorial enviado a BTG: los tres escenarios, las dos pistas, el plan de seis meses y los próximos pasos con fechas."
 },
 "p3": {"eyebrow": "Parte 03", "title": "El programa de seis meses.", "sub": "El rescate no depende de descuento. Es eficiencia en el origen, construida por fases, con un checkpoint que lo decide todo."},
 "program": {
   "eyebrow": "Roadmap de seis meses",
   "title": "Tres fases, un candado en septiembre.",
   "ph1Label": "Meses 1 y 2", "ph1Title": "Fundación e instrumentación",
   "ph1Body": "Baseline validada, allowlist de modelos, presupuestos con alerta en el piloto, caché en producción, panel de FinOps activo, equipo entrenado.",
   "ph2Label": "Mes 3", "ph2Title": "El checkpoint de septiembre",
   "ph2Body": "La promoción expira, el overage real aparece. Revisión conjunta: overage real versus proyectado, hitos del programa y la decisión comercial con datos sobre la mesa.",
   "ph3Label": "Meses 4 a 6", "ph3Title": "Maduración del rescate",
   "ph3Body": "Primitivos publicados, agentes gobernados, mix de modelos bajo revisión semanal. La curva se dobla hacia abajo mes a mes hasta el régimen maduro."
 },
 "redeem": {
   "eyebrow": "El rescate",
   "hero": "US$ 495k",
   "title": "US$ 495 mil de rescate proyectado en el año fiscal.",
   "body": "Aplicada la curva de maduración típica, la configuración austera de las palancas R1 a R7 reduce el consumo en el origen. No cuesta un dólar de descuento y no quita un asiento. Un programa maduro alcanza 55 a 70% de reducción; trabajamos con la banda conservadora.",
   "kLabel": "Composición", "kValue": "eficiencia técnica, sin depender de descuento"
 },
 "levers": {
   "eyebrow": "Palancas de mayor impacto",
   "title": "Dónde ataca el programa primero.",
   "lead1": "Las cuatro palancas que toman las clases de token más caras. Bandas oficiales del runbook, siempre rango con fuente.",
   "eyebrow2": "Palancas estructurales",
   "title2": "Lo que sostiene la ganancia en el tiempo.",
   "lead2": "Tres palancas que convierten el corte puntual en estándar permanente y protegen el presupuesto.",
   "r1Label": "R1 · 40 a 70% del output", "r1Title": "Control de output",
   "r1Body": "La salida cuesta ~4 a 5x el input por token. Bloques de instrucción en copilot-instructions.md hacen de la respuesta directa (código o diff) el estándar del repositorio. Una respuesta típica cae de 400 a 600 tokens a 30 a 50 restringida a diff.",
   "r2Label": "R2 · 40 a 70% de la cuenta", "r2Title": "Ruteo de modelos",
   "r2Body": "El precio por token varía dos órdenes de magnitud entre la clase liviana y la de frontera. Modo Auto por defecto (más 10% de descuento en chat), utility model para tareas triviales, frontera reservada para lo que la necesita. Dos modelos concentran 69% del costo de BTG.",
   "r3Label": "R4 · 40 a 80% del input", "r3Title": "Alcance de contexto",
   "r3Body": "El contexto suele ser 60%+ del input por turno. Disciplina de #-mentions, content exclusion y el fin de las mega-threads cortan lo que entra. LLMLingua (Microsoft) comprimió prompts hasta 20x; la banda usada es conservadora.",
   "r4Label": "R5 · 30 a 50% del input", "r4Title": "Caché y memoria",
   "r4Body": "83,5% del volumen de tokens de BTG es relectura de contexto. Prefijos estables en caché no se reprocesan (lectura a 0,1x en Anthropic, 50% en OpenAI). La memoria corta la reexplicación entre sesiones.",
   "r5Label": "R6 · ganancia compuesta", "r5Title": "Primitivos de repositorio",
   "r5Body": "Instrucciones, agentes, prompts y hooks versionados en el repositorio, tratados como infraestructura. Cada archivo reduce la reexplicación en cada pedido futuro: es lo que convierte los cortes de las otras palancas en estándar permanente.",
   "r6Label": "R3 · rutina a costo cero", "r6Title": "Modelos locales (BYOK)",
   "r6Body": "Un modelo local en VS Code (Ollama o Foundry Local) ruteado al trabajo de rutina, a costo cero de AI Credits por la mecánica oficial de BYOK. No aplica a completions; participación de un dígito a ~15% según el mix.",
   "r7Label": "R7 · guard-rail de varianza", "r7Title": "Presupuestos y medición",
   "r7Body": "Cuatro niveles de budget, del tope individual al failsafe de la empresa, con alerta al 80%. ULB en disponibilidad general desde el 1 de junio. No corta el régimen de trabajo; impide que un loop de agente consuma el pool de la unidad solo."
 },
 "p4": {"eyebrow": "Parte 04", "title": "Dos pistas en paralelo.", "sub": "Mientras la ingeniería construye eficiencia, la pista comercial mantiene el contrato al paso. Ninguna espera a la otra."},
 "tracks": {
   "eyebrow": "Comercial y estratégico",
   "title": "El apoyo que rodea al programa por los dos lados.",
   "leftLabel": "Pista comercial",
   "leftTitle": "Suavizar el impacto del overage",
   "leftBody": "Un abanico de opciones a explorar, nada definido aún: extender el crédito promocional o negociar un descuento adicional en los tres meses siguientes para suavizar el escalón de septiembre y, si le sirve a BTG, evaluar un Pre-Purchase Plan o condiciones vía ACD. El camino correcto sale de la conversación, con los números sobre la mesa.",
   "rightLabel": "Pista estratégica, GBB y equipos",
   "rightTitle": "Fundación y mejores prácticas",
   "rightBody": "Software Global Black Belt con presencia quincenal de junio a diciembre: enablement del equipo, arquitectura de contexto y agentes, implantación de las palancas R1 a R7, fundación de FinOps con los equipos de Microsoft y GitHub, y el paquete de evidencias del checkpoint de septiembre."
 },
 "who": {
   "eyebrow": "Roles",
   "title": "Quién hace qué, sin zona gris.",
   "c1Label": "BTG Pactual", "c1Title": "Tres nombres y una fecha",
   "c1Body": "Patrocinador ejecutivo, punto focal de plataforma y punto focal de FinOps. Acceso al panel de billing y el kickoff agendado dentro de junio.",
   "c2Label": "Microsoft", "c2Title": "GBB y equipo de cuenta",
   "c2Body": "El programa R1 a R7 con enablement, el kit de transición vivo, la exploración de las opciones comerciales junto a BTG y la cadencia quincenal a lo largo de los seis meses, hasta diciembre.",
   "c3Label": "GitHub", "c3Title": "Producto y billing",
   "c3Body": "Telemetría oficial de consumo, la promoción de 90 días, la tabla de planes y el soporte de producto para budgets, caché y gobernanza."
 },
 "end": {
   "eyebrow": "Próximo paso",
   "title": "Kickoff en junio. Checkpoint en septiembre. Alianza hasta diciembre.",
   "sub": "La ventana existe exactamente para decidir con ventaja. Ninguna decisión necesita tomarse a oscuras.",
   "contactLabel": "Contacto", "nextLabel": "Próxima acción",
   "next": "Agendar el kickoff del programa dentro de junio de 2026"
 },
 "notes": {}
}
