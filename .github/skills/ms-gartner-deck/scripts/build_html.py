#!/usr/bin/env python3
"""
gen_50.py: generates the 50-slide reference deck body and splices it into
the existing mock-reference-deck.html (which already holds all the CSS).

Produces ms-reference-deck.html. Each slide is one <section class="slide">.
"""
import os
import re
import sys

# ----- section -> anchor color map -----
SECTIONS = {
    "front":  "blue",
    "ctx":    "blue",
    "prob":   "green",
    "sol":    "yellow",
    "arch":   "red",
    "plan":   "blue",
    "invest": "green",
    "back":   "red",
}

ACT_LABEL = {
    "front":  "Front matter",
    "ctx":    "Section 1 \u00b7 Context",
    "prob":   "Section 2 \u00b7 The problem",
    "sol":    "Section 3 \u00b7 The solution",
    "arch":   "Section 4 \u00b7 Architecture",
    "plan":   "Section 5 \u00b7 The plan",
    "invest": "Section 6 \u00b7 Investment",
    "back":   "Appendix",
}

MS_MARK = '<span class="ms-mark"><i></i><i></i><i></i><i></i></span>'

# running page counter, total filled in at the end
_TOTAL = 53

def chrome_top(act):
    return f'''    <div class="chrome-top">
      <div class="brand">
        {MS_MARK}
        <b>Microsoft</b><span class="sep">\u00b7</span>{act}
      </div>
      <div class="page-no"><b>PP</b><span class="dot">\u00b7</span>{_TOTAL}</div>
    </div>'''

def title_block(kicker, h, desc):
    return f'''    <div class="title-block">
      <div class="kicker">{kicker}</div>
      <h1>{h}</h1>
      <div class="descriptor">{desc}</div>
    </div>'''

def chrome_bot(src):
    return f'''    <div class="chrome-bot">
      <div class="src">{src}</div>
      <div class="foot-brand">Microsoft \u00b7 Strategic Brief</div>
    </div>'''

def content_slide(sec, kicker, h, desc, body, src, body_class=""):
    """A standard content slide: chrome + title + body + chrome."""
    act = ACT_LABEL[sec]
    color = SECTIONS[sec]
    bc = f" {body_class}" if body_class else ""
    return f'''  <section class="slide act-{color}">
{chrome_top(act)}
{title_block(kicker, h, desc)}
    <div class="body{bc}">
{body}
    </div>
{chrome_bot(src)}
  </section>'''

def bleed_slide(sec, inner):
    """A full-bleed slide (cover, divider, quote, appendix, contact)."""
    color = SECTIONS[sec]
    return f'''  <section class="slide slide--bleed act-{color}">
{inner}
  </section>'''


# ============================================================
# SLIDE BUILDERS: front matter (1-4)
# ============================================================

def s01_cover():
    inner = '''    <div class="cover">
      <div class="cover__left">
        <div class="cover__brand">
          ''' + MS_MARK + '''
          <b>Microsoft</b><span class="sep">\u00b7</span>AI Platform Modernization
        </div>
        <div>
          <div class="cover__title">
            The platform decision behind every <span class="accent">production AI</span> outcome.
          </div>
          <div class="cover__sub">
            A strategic and technical brief on why enterprise AI initiatives
            stall before production, and the reference architecture that
            closes the gap between pilot and scale.
          </div>
          <div class="cover__chips">
            <span>Azure <b>AI Foundry</b></span>
            <span>GitHub <b>Copilot Enterprise</b></span>
            <span>Azure <b>Kubernetes Service</b></span>
            <span>Agentic <b>DevOps</b></span>
          </div>
        </div>
        <div class="cover__byline">
          <div><b>Frontier Cockpit Team</b>Software Global Black Belt</div>
          <div><b>Strategic &amp; Technical Brief</b>Client engagement \u00b7 2026</div>
        </div>
      </div>
      <div class="cover__right">
        <div class="cover__top">
          <span>Confidential \u00b7 Client brief</span>
          <span><b>01 / 50</b></span>
        </div>
        <div class="cover__meeting">
          <div class="label">Session context</div>
          <div class="headline">
            A working session to decide the
            <b>platform scope and the first phase</b>.
          </div>
          <div class="cover__meeting__grid">
            <div>
              <div class="mk">Client</div>
              <div class="mv">Contoso Financial<span>Platform &amp; Engineering leadership</span></div>
            </div>
            <div>
              <div class="mk">Date</div>
              <div class="mv">2026-05-20<span>90-minute briefing</span></div>
            </div>
            <div>
              <div class="mk">Session type</div>
              <div class="mv">Strategic &amp; technical brief<span>Decision-oriented, not a pitch</span></div>
            </div>
            <div>
              <div class="mk">In the room</div>
              <div class="mv">CTO, Head of Platform<span>Security and SRE leads</span></div>
            </div>
          </div>
          <div class="decide">
            <b>Outcome we are after:</b> agreement on a three-week assessment
            window and the two candidate workloads to baseline. Placeholders
            for the reference template.
          </div>
        </div>
      </div>
    </div>'''
    return bleed_slide("front", inner)


def s02_agenda():
    secs = [
        ("01", "Context", "Slides 05\u201312", ["Market adoption signals", "Landscape of approaches", "Where teams sit today", "A client's starting point"]),
        ("02", "The problem", "Slides 13\u201321", ["Cost of delay", "Three root causes", "The broken path", "What compounds it"]),
        ("03", "The solution", "Slides 22\u201330", ["The reference stack", "Operating principles", "The governed path", "Objections answered"]),
        ("04", "Architecture", "Slides 31\u201338", ["Component diagram", "Runtime layer detail", "CI/CD with gates", "Build options"]),
        ("05", "The plan", "Slides 39\u201344", ["Modernization roadmap", "Assessment week by week", "The engagement team", "Ownership and risks"]),
        ("06", "Investment", "Slides 45\u201348", ["Engagement sizes", "The ask", "The recommendation"]),
    ]
    cards = ""
    for no, name, rng, items in secs:
        lis = "".join(f"<li>{it}</li>" for it in items)
        cards += f'''        <div class="agenda__sec">
          <div class="ag-no">{no}</div>
          <h4>{name}</h4>
          <div class="ag-range">{rng}</div>
          <ul>{lis}</ul>
        </div>
'''
    body = f'      <div class="agenda">\n{cards}      </div>'
    return content_slide("front", "Agenda",
        "Six sections, from <b>where the market is</b> to <b>what to do next</b>.",
        "This brief follows a single line: diagnose the gap, reframe the solution as a platform, then lay out the architecture, plan, and investment to get there.",
        body,
        "<b>Navigation \u00b7</b> Section dividers mark each transition. The deck is built to be read in order or sampled by section.",
        body_class="body--center")


def s03_exec_summary():
    body = '''      <div class="exec">
        <div class="exec__col">
          <div class="ec-no">1</div>
          <h3>The blocker is the platform, not the model</h3>
          <p>Pilots reach a working demo and stall. The recurring cause is the absence of a shared foundation: environments, data access, and a route to production.</p>
          <div class="ec-take"><b>So what \u00b7</b> Solve it once at the platform layer, not repeatedly per project.</div>
        </div>
        <div class="exec__col">
          <div class="ec-no">2</div>
          <h3>An opinionated stack closes the gap</h3>
          <p>Four layers, each owned once, remove the friction line-items teams hit today. Teams consume the platform; they do not re-derive it.</p>
          <div class="ec-take"><b>So what \u00b7</b> The reference architecture is the deliverable, not a slideware idea.</div>
        </div>
        <div class="exec__col">
          <div class="ec-no">3</div>
          <h3>Start small, decide on evidence</h3>
          <p>A three-week assessment produces the client's own baseline. Every commitment after that is a decision made with real numbers.</p>
          <div class="ec-take"><b>So what \u00b7</b> Low-commitment first step. The roadmap earns the next phase.</div>
        </div>
      </div>'''
    return content_slide("front", "Executive summary",
        "Three things to take from this brief, <b>before the detail</b>.",
        "If the room reads only one slide, it is this one. Each column is a claim, the evidence behind it, and what it means for the decision ahead.",
        body,
        "<b>Read order \u00b7</b> This slide stands alone. The six sections expand each column with evidence and architecture.",
        body_class="body--center")


def s04_quote():
    inner = '''    <div class="quote-bleed">
      <div class="qb-mark">\u201c</div>
      <blockquote>
        The hard part of enterprise AI was never the model. It is the
        <mark>distance between a notebook and a service</mark> the business
        can actually depend on.
      </blockquote>
      <cite>Framing position \u00b7 <b>reference template</b>, illustrative attribution</cite>
    </div>'''
    return bleed_slide("front", inner)


# ============================================================
# NEW ARCHETYPE BUILDERS (the 14 not in the 16-slide mock)
# Each takes a `sec` so the anchor color is set by section.
# ============================================================

def a_section_intro(sec):
    return content_slide(sec, "Section intro",
        "Where the market is, in <b>one honest read</b>.",
        "A section intro is lighter than a divider. It sets up the sub-topic and frames what the next few slides will show, without the full act ceremony.",
        '''      <div class="sec-intro">
        <div class="sec-intro__main">
          <div class="sec-intro__eyebrow">What this section covers</div>
          <div class="sec-intro__h">Adoption is wide. <b>Production is narrow.</b></div>
          <div class="sec-intro__lead">
            Most enterprises now run AI pilots. Far fewer run AI in production.
            This section sizes that gap with the client's peers as the reference
            point, so the problem is concrete before we name its causes.
          </div>
        </div>
        <div class="sec-intro__aside">
          <div class="ai-row"><div class="ai-k">In this section</div><div class="ai-v">4 slides, ending on a client snapshot</div></div>
          <div class="ai-row"><div class="ai-k">Key question</div><div class="ai-v">How big is the pilot-to-production gap?</div></div>
          <div class="ai-row"><div class="ai-k">Leaves you with</div><div class="ai-v">A measured starting point, not an opinion</div></div>
        </div>
      </div>''',
        "<b>Pattern note \u00b7</b> Use a section intro after a divider when the section is long enough to need its own framing.",
        body_class="body--fill")


def a_team(sec):
    people = [
        ("PS", "Frontier Cockpit Team", "Engagement lead", "Software Global Black Belt. Owns the technical direction and the client relationship end to end."),
        ("AE", "Account exec", "Commercial owner", "Holds scope, timeline, and the commercial conversation. Single point for contracting."),
        ("PE", "Platform engineer", "Build lead", "Stands up the landing zone and the standard pipeline. Pairs with client engineers."),
        ("CE", "Client engineer", "Embedded", "Two client engineers work inside the engagement, so ownership transfers as the platform is built."),
    ]
    cards = ""
    for initials, name, role, desc in people:
        cards += f'''        <div class="team__card">
          <div class="team__avatar">{initials}</div>
          <h4>{name}</h4>
          <div class="tm-role">{role}</div>
          <p>{desc}</p>
        </div>
'''
    return content_slide(sec, "The engagement team",
        "Four roles, <b>clear ownership</b>, no ambiguity about who decides what.",
        "A small team by design. Each person owns one thing, and two of the four seats are filled by the client so the hand-over starts on day one.",
        f'      <div class="team">\n{cards}      </div>',
        "<b>Staffing note \u00b7</b> Role names are generic for the template. A real deck names individuals and their tenure.",
        body_class="body--center")


def a_case_study(sec):
    return content_slide(sec, "Case study",
        "One client, <b>same shape of problem</b>, measured before and after.",
        "A case study makes the abstract concrete. Problem, approach, result, in three rows, with the headline outcome pulled into the hero panel.",
        '''      <div class="case">
        <div class="case__hero">
          <div>
            <div class="ch-tag">Reference client</div>
            <div class="ch-name">Mid-size financial services firm</div>
            <div class="ch-meta">~600 engineers \u00b7 existing Azure footprint \u00b7 12 AI pilots, 1 in production</div>
          </div>
          <div class="ch-stat">
            <div class="n">9 \u2192 2</div>
            <div class="l">weeks to provision a new AI workload, after the platform</div>
          </div>
        </div>
        <div class="case__steps">
          <div class="case__step">
            <div class="cs-k">Problem</div>
            <div class="cs-v">Every pilot rebuilt its own environment and data access. <b>Eleven of twelve</b> never got a production target.</div>
          </div>
          <div class="case__step">
            <div class="cs-k">Approach</div>
            <div class="cs-v">A six-week foundation phase: AKS landing zone, standard pipeline, and one pilot migrated onto golden paths.</div>
          </div>
          <div class="case__step">
            <div class="cs-k">Result</div>
            <div class="cs-v">Provisioning dropped from <b>nine weeks to two</b>. Three further workloads reached production within the next quarter.</div>
          </div>
        </div>
      </div>''',
        "<b>Anonymization note \u00b7</b> Figures and client descriptor are illustrative. Real case studies use cited, approved data.",
        body_class="body--fill")


def a_architecture_detail(sec):
    return content_slide(sec, "Architecture detail",
        "The reference stack, <b>component by component</b>, with the decisions called out.",
        "Where the layer-stack slide is the overview, this is the annotated version: real components in tiers, with the design decisions pulled out as notes.",
        '''      <div class="arch">
        <div class="arch__canvas">
          <div class="arch__tier">
            <div class="at-lbl">Experience</div>
            <div class="arch__row">
              <div class="arch__node b"><h5>Developer portal</h5><span>Golden-path templates</span></div>
              <div class="arch__node b"><h5>Service catalog</h5><span>Self-service provisioning</span></div>
            </div>
          </div>
          <div class="arch__tier">
            <div class="at-lbl">Delivery</div>
            <div class="arch__row">
              <div class="arch__node g"><h5>Standard CI</h5><span>Build, test, evaluate</span></div>
              <div class="arch__node g"><h5>Policy gates</h5><span>In-pipeline governance</span></div>
              <div class="arch__node g"><h5>Release</h5><span>Promotion with rollback</span></div>
            </div>
          </div>
          <div class="arch__tier">
            <div class="at-lbl">Runtime &amp; Intelligence</div>
            <div class="arch__row">
              <div class="arch__node y"><h5>AKS landing zone</h5><span>Networking, identity, scale</span></div>
              <div class="arch__node r"><h5>Azure AI Foundry</h5><span>Model catalog, evaluation</span></div>
              <div class="arch__node r"><h5>Observability</h5><span>Cost, latency, behavior</span></div>
            </div>
          </div>
        </div>
        <div class="arch__notes">
          <div class="arch__note"><div class="an-k">Decided once</div><div class="an-v">Networking and identity live in the landing zone, not per workload.</div></div>
          <div class="arch__note"><div class="an-k">Shift-left by design</div><div class="an-v">Policy gates run inside CI, so governance is a property of shipping.</div></div>
          <div class="arch__note"><div class="an-k">One pane</div><div class="an-v">Observability is shared, so every team reads the same signal.</div></div>
        </div>
      </div>''',
        "<b>Diagram note \u00b7</b> Component names are generic. A real deck names the client's specific services and versions.",
        body_class="body--fill")


def a_vendor_compare(sec):
    return content_slide(sec, "Build options",
        "Three ways to get a platform. <b>One fits this client</b>.",
        "A vendor-compare slide is an honest feature matrix. The recommended column is highlighted, but every row is filled in for all three options.",
        '''      <table class="vtable">
        <thead>
          <tr>
            <th>Capability</th>
            <th class="opt">Build in-house</th>
            <th class="opt win">Reference platform</th>
            <th class="opt">Off-the-shelf PaaS</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Time to first workload</td><td class="no">Months</td><td class="col-win yes">Weeks</td><td class="partial">Weeks</td></tr>
          <tr><td>Fits existing Azure estate</td><td class="yes">Yes</td><td class="col-win yes">Yes</td><td class="no">Partial</td></tr>
          <tr><td>Governance in the pipeline</td><td class="partial">If built</td><td class="col-win yes">Yes</td><td class="no">No</td></tr>
          <tr><td>Client owns it at the end</td><td class="yes">Yes</td><td class="col-win yes">Yes</td><td class="no">No</td></tr>
          <tr><td>Ongoing vendor lock-in</td><td class="yes">None</td><td class="col-win yes">None</td><td class="no">High</td></tr>
          <tr><td>Internal effort to maintain</td><td class="no">High</td><td class="col-win partial">Moderate</td><td class="yes">Low</td></tr>
        </tbody>
      </table>
      <div class="pull" style="margin-top:16px;">
        <div class="lbl">How to read this</div>
        <p>In-house gives control at a high cost. Off-the-shelf is fast but rents you the platform. The <b>reference platform</b> is the middle path: built with you, owned by you.</p>
        <cite>Synthesis line \u00b7 <b>reference template</b></cite>
      </div>''',
        "<b>Matrix note \u00b7</b> Ratings are qualitative for the template. Real comparisons cite specifics and are reviewed with the account team.",
        body_class="body--center")


def a_raci(sec):
    rows = [
        ("Platform scope &amp; design", "A", "C", "R", "I"),
        ("Landing zone build", "I", "R", "A", "C"),
        ("CI/CD pipeline setup", "I", "R", "A", "C"),
        ("Policy &amp; governance rules", "C", "C", "A", "R"),
        ("Pilot workload migration", "C", "A", "R", "C"),
        ("Platform ownership, ongoing", "A", "I", "C", "R"),
    ]
    body_rows = ""
    for label, *codes in rows:
        cells = "".join(
            f'<td><span class="badge {c}">{c}</span></td>' if c != "-"
            else '<td><span class="badge dash">\u2013</span></td>'
            for c in codes)
        body_rows += f"          <tr><td>{label}</td>{cells}</tr>\n"
    return content_slide(sec, "Ownership matrix",
        "Who is <b>responsible, accountable, consulted, informed</b> for each workstream.",
        "A RACI matrix removes the most common engagement failure: ambiguity about who owns what. Each cell is one letter, and ownership shifts to the client down the rows.",
        f'''      <table class="raci">
        <thead>
          <tr>
            <th>Workstream</th>
            <th>Client lead</th>
            <th>MS engagement</th>
            <th>Platform team</th>
            <th>Client ops</th>
          </tr>
        </thead>
        <tbody>
{body_rows}        </tbody>
      </table>
      <div class="raci-legend">
        <span><span class="badge R">R</span> Responsible</span>
        <span><span class="badge A">A</span> Accountable</span>
        <span><span class="badge C">C</span> Consulted</span>
        <span><span class="badge I">I</span> Informed</span>
      </div>''',
        "<b>RACI note \u00b7</b> One accountable party per row. Calibrate the grid with the client during the assessment.",
        body_class="body--center")


def a_metrics_dashboard(sec):
    return content_slide(sec, "Target-state metrics",
        "Six signals that tell you the platform is <b>actually working</b>.",
        "A metrics dashboard mixes tile sizes so the eye lands on what matters. The featured tile carries the headline; the rest give context around it.",
        '''      <div class="dash">
        <div class="dash__tile feat w2 tall">
          <div class="dk">Headline signal</div>
          <div class="dn">2<sup>wks</sup></div>
          <div class="dd">median time to provision a new AI workload, down from nine</div>
        </div>
        <div class="dash__tile w2"><div class="dk">Time to production</div><div class="dn">\u221270%</div><div class="dd">pilot to live service</div></div>
        <div class="dash__tile w2"><div class="dk">Policy rework</div><div class="dn">\u22121<sup>stage</sup></div><div class="dd">governance shifted left</div></div>
        <div class="dash__tile w2"><div class="dk">Workloads on platform</div><div class="dn">14</div><div class="dd">across six teams</div></div>
        <div class="dash__tile w2"><div class="dk">Shared observability</div><div class="dn">100<sup>%</sup></div><div class="dd">one pane, all teams</div></div>
      </div>''',
        "<b>Dashboard note \u00b7</b> All figures are placeholders. Real dashboards read against the Phase 1 baseline.",
        body_class="body--fill")


def a_faq(sec):
    items = [
        ("Does this replace our existing Azure setup?", "No. The assessment maps the current estate first, and the landing zone is designed <b>around what exists</b>, not on top of a teardown."),
        ("What if our teams resist a shared platform?", "Two pilot teams co-design the golden paths. The platform reflects <b>real workflows</b> because real teams shaped it."),
        ("How long until we see value?", "The Phase 1 assessment delivers a baseline in <b>three weeks</b>. The first workload runs end to end by week nine of the foundation phase."),
        ("Who owns the platform afterwards?", "The client does. Client engineers work inside Phases 2 and 3, so ownership <b>transfers gradually</b>, not in a single hand-off."),
        ("Is this locked to Microsoft tooling?", "The reference stack uses Azure services, but the patterns are portable. There is <b>no proprietary lock-in</b> layer."),
        ("What does it cost to run, ongoing?", "Runtime cost is the AKS and Foundry footprint. The platform itself adds <b>process, not licensing</b>."),
    ]
    cells = ""
    for q, a in items:
        cells += f'''        <div class="faq__item">
          <div class="faq__q"><span class="fq-mark">Q</span><span>{q}</span></div>
          <div class="faq__a">{a}</div>
        </div>
'''
    return content_slide(sec, "Common objections",
        "The questions a careful buyer asks, <b>answered directly</b>.",
        "A FAQ slide pre-empts the room's real concerns. Six pairs, two columns, no evasion. If a question needs a longer answer, it gets its own slide.",
        f'      <div class="faq">\n{cells}      </div>',
        "<b>FAQ note \u00b7</b> These are the recurring objections for this template. Tailor the list to each client's known concerns.",
        body_class="body--center")


def a_org_chart(sec):
    return content_slide(sec, "Governance structure",
        "How decisions flow once the platform is <b>live and owned</b>.",
        "An org chart on a proposal slide answers a quiet question: after hand-over, who runs this? Three tiers, one accountable owner at the top.",
        '''      <div class="org">
        <div class="org__node lead"><h5>Platform owner</h5><span>Client \u00b7 accountable for the platform</span></div>
        <div class="org__connector"></div>
        <div class="org__rail"></div>
        <div class="org__row">
          <div style="display:grid;justify-items:center;">
            <div class="org__node"><h5>Platform engineering</h5><span>Runs the landing zone &amp; pipeline</span></div>
          </div>
          <div style="display:grid;justify-items:center;">
            <div class="org__node"><h5>Governance &amp; security</h5><span>Owns policy in the pipeline</span></div>
          </div>
          <div style="display:grid;justify-items:center;">
            <div class="org__node"><h5>Enablement</h5><span>Onboards teams to golden paths</span></div>
          </div>
        </div>
      </div>''',
        "<b>Org note \u00b7</b> Structure is illustrative. A real deck maps to the client's actual reporting lines.",
        body_class="body--fill")


def a_gantt(sec):
    # bars: (label, color, start_col 1-12, span)
    bars = [
        ("Phase 1 \u00b7 Assess", "b", 1, 3, "Weeks 1\u20133"),
        ("Phase 2 \u00b7 Foundation", "g", 4, 6, "Weeks 4\u20139"),
        ("Phase 3 \u00b7 Golden paths", "y", 7, 4, "Weeks 7\u201310, overlaps"),
        ("Phase 4 \u00b7 Scale", "r", 10, 3, "Weeks 10\u201312+"),
    ]
    head = '<span>Workstream</span>' + "".join(f'<span>W{i}</span>' for i in range(1, 13))
    rows = ""
    for label, color, start, span, note in bars:
        left = (start - 1) / 12 * 100
        width = span / 12 * 100
        rows += f'''        <div class="gantt__row">
          <div class="gr-label">{label}</div>
          <div class="gantt__track">
            <div class="gantt__bar {color}" style="left:{left:.2f}%; width:{width:.2f}%;">{note}</div>
          </div>
        </div>
'''
    return content_slide(sec, "Detailed timeline",
        "Twelve weeks, <b>four phases</b>, with the overlaps shown honestly.",
        "A gantt makes dependencies visible. Phase 3 starts before Phase 2 fully closes, on purpose: golden paths are designed while the foundation settles.",
        f'''      <div class="gantt">
        <div class="gantt__head">{head}</div>
{rows}      </div>''',
        "<b>Timeline note \u00b7</b> Weeks assume a mid-size org with an existing Azure footprint. Re-scope per engagement.",
        body_class="body--fill")


def a_decision_matrix(sec):
    # rows: (option, [scores]), weights row, total
    return content_slide(sec, "Weighted decision",
        "The build-versus-platform call, <b>scored on the criteria that matter</b>.",
        "A decision matrix shows the reasoning, not just the conclusion. Each option is scored against weighted criteria, and the totals are computed in the open.",
        '''      <table class="dmatrix">
        <thead>
          <tr>
            <th>Criterion</th>
            <th class="num">Weight</th>
            <th class="num">Build in-house</th>
            <th class="num">Reference platform</th>
            <th class="num">Off-the-shelf PaaS</th>
          </tr>
        </thead>
        <tbody>
          <tr><td>Speed to production</td><td class="num">30%</td><td class="num">1.2</td><td class="num">2.7</td><td class="num">2.4</td></tr>
          <tr><td>Fit with current estate</td><td class="num">25%</td><td class="num">2.3</td><td class="num">2.5</td><td class="num">1.0</td></tr>
          <tr><td>Long-term ownership</td><td class="num">25%</td><td class="num">2.5</td><td class="num">2.5</td><td class="num">0.8</td></tr>
          <tr><td>Internal effort to sustain</td><td class="num">20%</td><td class="num">0.8</td><td class="num">1.8</td><td class="num">2.4</td></tr>
          <tr class="total"><td>Weighted total</td><td class="num">100%</td><td class="num">1.67</td><td class="num">2.41<span class="scorebar" style="width:60px;"></span></td><td class="num">1.62</td></tr>
        </tbody>
      </table>
      <div class="pull" style="margin-top:16px;">
        <div class="lbl">What the score says</div>
        <p>The reference platform wins not on any single row, but on <b>balance</b>: it is the only option that scores well on speed, fit, and ownership at once.</p>
        <cite>Scoring is illustrative \u00b7 <b>reference template</b></cite>
      </div>''',
        "<b>Scoring note \u00b7</b> Weights and scores are placeholders. Set them with the client so the decision is theirs.",
        body_class="body--center")


def a_stakeholder_map(sec):
    return content_slide(sec, "Stakeholder map",
        "Who to <b>engage closely</b>, and who to keep informed.",
        "A stakeholder map plots influence against interest. The top-right quadrant is where the engagement spends its attention; the rest get the right, lighter touch.",
        '''      <div class="smap-wrap">
        <div class="quad-yaxis">Influence \u2192</div>
        <div class="quad-col">
          <div class="smap">
            <div class="smap__cell">
              <div class="sm-lbl">High influence \u00b7 low interest</div>
              <div class="smap__chips"><span class="smap__chip">CFO</span><span class="smap__chip">Procurement</span></div>
            </div>
            <div class="smap__cell key">
              <div class="sm-lbl">High influence \u00b7 high interest \u00b7 engage closely</div>
              <div class="smap__chips"><span class="smap__chip">CTO</span><span class="smap__chip">Head of platform</span><span class="smap__chip">Security lead</span></div>
            </div>
            <div class="smap__cell">
              <div class="sm-lbl">Low influence \u00b7 low interest \u00b7 monitor</div>
              <div class="smap__chips"><span class="smap__chip">Adjacent BUs</span></div>
            </div>
            <div class="smap__cell">
              <div class="sm-lbl">Low influence \u00b7 high interest \u00b7 keep informed</div>
              <div class="smap__chips"><span class="smap__chip">App teams</span><span class="smap__chip">SRE</span><span class="smap__chip">Data engineering</span></div>
            </div>
          </div>
          <div class="quad-xaxis">Interest \u2192</div>
        </div>
      </div>''',
        "<b>Map note \u00b7</b> Placement is illustrative. Build the real map with the client sponsor early in Phase 1.",
        body_class="body--fill")






# ============================================================
# BASE ARCHETYPE BUILDERS (the 12 from the validated 16-mock,
# rewritten as section-parameterized functions)
# ============================================================

def a_divider(sec, act_no, kicker, title, desc, questions, q_start):
    color = SECTIONS[sec]
    on_yellow = " on-yellow" if color == "yellow" else ""
    mini_color = "rgba(0,0,0,0.55)" if color == "yellow" else "rgba(255,255,255,0.78)"
    qs = ""
    for i, q in enumerate(questions):
        qs += f'          <div><span class="qn">Q{q_start+i}</span>{q}</div>\n'
    inner = f'''    <div class="divider">
      <div class="divider__left">
        <div class="divider__actno">{act_no}</div>
        <div class="divider__kicker">{kicker}</div>
        <div class="divider__title">{title}</div>
        <div class="divider__desc">{desc}</div>
      </div>
      <div class="divider__right{on_yellow}">
        <div class="mini-h" style="color:{mini_color}">Questions this act answers</div>
        <div class="divider__qlist">
{qs}        </div>
      </div>
    </div>'''
    return bleed_slide(sec, inner)


def a_big_number(sec, kicker, h, desc, metric_label, metric_n, metric_unit,
                 metric_desc, cards, src):
    card_html = ""
    for lbl, n, d, klass in cards:
        kc = f" {klass}" if klass else ""
        card_html += f'''          <div class="stat-card{kc}">
            <div class="lbl">{lbl}</div>
            <div class="n" style="font-size:38px;">{n}</div>
            <div class="desc">{d}</div>
          </div>
'''
    body = f'''      <div class="two-col" style="grid-template-columns: 0.9fr 1.1fr; gap:32px;">
        <div class="stat-card dark" style="align-content:center;">
          <div class="lbl">{metric_label}</div>
          <div class="n">{metric_n}<sup>{metric_unit}</sup></div>
          <div class="desc">{metric_desc}</div>
          <div class="src-row">Placeholder figure \u00b7 cite real source in production decks</div>
        </div>
        <div class="col-stack">
{card_html}        </div>
      </div>'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


def a_data_table(sec, kicker, h, desc, headers, rows, pull, src):
    thead = "".join(
        f'<th class="{k}" style="width:{w}">{lbl}</th>' if k
        else f'<th style="width:{w}">{lbl}</th>'
        for lbl, k, w in headers)
    tbody = ""
    for row in rows:
        cells = "".join(
            f'<td class="{k}">{v}</td>' if k else f'<td>{v}</td>'
            for v, k in row)
        tbody += f"          <tr>{cells}</tr>\n"
    pull_html = ""
    if pull:
        pull_html = f'''      <div class="pull" style="margin-top:18px;">
        <div class="lbl">{pull[0]}</div>
        <p>{pull[1]}</p>
        <cite>{pull[2]}</cite>
      </div>'''
    body = f'''      <table class="dtable">
        <thead><tr>{thead}</tr></thead>
        <tbody>
{tbody}        </tbody>
      </table>
{pull_html}'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


def a_quadrant(sec, kicker, h, desc, yaxis, xaxis, cells, dots, legend, src):
    cell_html = ""
    for lbl, title, p, hot in cells:
        hc = " hot" if hot else ""
        cell_html += f'''            <div class="quad__cell{hc}">
              <div class="qc-lbl">{lbl}</div>
              <h4>{title}</h4>
              <p>{p}</p>
            </div>
'''
    dot_html = "".join(
        f'            <div class="quad__dot {k}" style="left:{l}; top:{t};"></div>\n'
        for k, l, t in dots)
    leg_html = "".join(
        f'        <span><i style="background:{c};"></i> {t}</span>\n'
        for c, t in legend)
    body = f'''      <div class="quad-wrap">
        <div class="quad-yaxis">{yaxis}</div>
        <div class="quad-col">
          <div class="quad">
{cell_html}{dot_html}          </div>
          <div class="quad-xaxis">{xaxis}</div>
        </div>
      </div>
      <div class="quad-legend">
{leg_html}      </div>'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--fill")


def a_layer_stack(sec, kicker, h, desc, layers, src):
    rows = ""
    for tag, title, d in layers:
        rows += f'''        <div class="layer">
          <div class="layer__tag">{tag}</div>
          <div class="layer__body">
            <h4>{title}</h4>
            <p>{d}</p>
          </div>
        </div>
'''
    body = f'      <div class="stack">\n{rows}      </div>'
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--fill")


def a_pillar_grid(sec, kicker, h, desc, pillars, src):
    cols = ""
    for no, title, d in pillars:
        cols += f'''        <div class="pillar">
          <div class="p-no">{no}</div>
          <h4>{title}</h4>
          <p>{d}</p>
        </div>
'''
    body = f'      <div class="pillars">\n{cols}      </div>'
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


def a_before_after(sec, kicker, h, desc, before_lbl, before_items,
                   after_lbl, after_items, stats, src):
    bi = "".join(f"            <li>{x}</li>\n" for x in before_items)
    ai = "".join(f"            <li>{x}</li>\n" for x in after_items)
    stat_html = ""
    for st in stats:
        lbl, n, d = st[0], st[1], st[2]
        feat = st[3] if len(st) > 3 else False
        fc = " accent" if feat else ""
        stat_html += f'''        <div class="stat-card{fc}"><div class="lbl">{lbl}</div><div class="n" style="font-size:34px;">{n}</div><div class="desc">{d}</div></div>
'''
    body = f'''      <div class="compare">
        <div class="compare__col compare__col--before">
          <div class="lbl">{before_lbl}</div>
          <ul>
{bi}          </ul>
        </div>
        <div class="compare__arrow">&rarr;</div>
        <div class="compare__col compare__col--after">
          <div class="lbl">{after_lbl}</div>
          <ul>
{ai}          </ul>
        </div>
      </div>
      <div class="two-col" style="margin-top:18px; grid-template-columns:repeat(3,1fr); gap:14px;">
{stat_html}      </div>'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


def a_flow(sec, kicker, h, desc, nodes, src):
    parts = []
    for i, (icon, title, d) in enumerate(nodes):
        parts.append(f'''        <div class="flow__node">
          <div class="fn-ico">{icon}</div>
          <h4>{title}</h4>
          <p>{d}</p>
        </div>''')
        if i < len(nodes) - 1:
            parts.append('        <div class="flow__arrow">&rarr;</div>')
    body = '      <div class="flow">\n' + "\n".join(parts) + '\n      </div>'
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


def a_roadmap(sec, kicker, h, desc, phases, src):
    cols = ""
    for no, name, when, items, ex_lbl, ex_text in phases:
        lis = "".join(f"              <li>{it}</li>\n" for it in items)
        cols += f'''        <div class="phase">
          <div class="phase__hd">
            <div class="ph-no">{no}</div>
            <h4>{name}</h4>
          </div>
          <div class="phase__body">
            <div class="when">{when}</div>
            <ul>
{lis}            </ul>
            <div class="phase__exit"><span class="ex-lbl">{ex_lbl}</span><p>{ex_text}</p></div>
          </div>
        </div>
'''
    body = f'      <div class="roadmap">\n{cols}      </div>'
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--fill")


def a_pricing(sec, kicker, h, desc, tiers, src):
    cols = ""
    for name, price, unit, sub, items, foot, featured, badge in tiers:
        fc = " featured" if featured else ""
        badge_html = f'<span class="tier__badge">{badge}</span>' if badge else ""
        lis = "".join(f"            <li>{it}</li>\n" for it in items)
        cols += f'''        <div class="tier{fc}">
          <div class="tier__hd">
            {badge_html}
            <div class="t-name">{name}</div>
            <div class="t-price">{price}<span class="unit"> {unit}</span></div>
            <div class="t-sub">{sub}</div>
          </div>
          <ul class="tier__body">
{lis}          </ul>
          <div class="tier__foot">{foot}</div>
        </div>
'''
    body = f'      <div class="tiers">\n{cols}      </div>'
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--fill")


def a_recommendation(sec, kicker, h, desc, pillars, ask_label, ask_n,
                     ask_desc, next_label, next_text, contact, src):
    pcols = ""
    for no, title, d in pillars:
        pcols += f'''          <div class="pillar">
            <div class="p-no">{no}</div>
            <h4>{title}</h4>
            <p>{d}</p>
          </div>
'''
    body = f'''      <div class="two-col" style="grid-template-columns:1.2fr 0.8fr; gap:32px;">
        <div class="pillars" style="grid-template-columns:1fr; gap:12px; align-content:start;">
{pcols}        </div>
        <div class="col-stack">
          <div class="stat-card dark" style="align-content:center;">
            <div class="lbl">{ask_label}</div>
            <div class="n" style="font-size:44px;">{ask_n}</div>
            <div class="desc">{ask_desc}</div>
          </div>
          <div class="pull">
            <div class="lbl">{next_label}</div>
            <p>{next_text}</p>
            <cite>{contact}</cite>
          </div>
        </div>
      </div>'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


# ============================================================
# PARAMETERIZED VARIANTS: quote / exec-summary / risks-table
# (override the single-purpose versions above; last def wins)
# ============================================================

def a_quote(sec, quote_html, cite_html):
    inner = f'''    <div class="quote-bleed">
      <div class="qb-mark">\u201c</div>
      <blockquote>{quote_html}</blockquote>
      <cite>{cite_html}</cite>
    </div>'''
    return bleed_slide(sec, inner)


def a_exec_summary(sec, kicker, h, desc, cols, src):
    col_html = ""
    for n, title, body, take in cols:
        col_html += f'''        <div class="exec__col">
          <div class="ec-no">{n}</div>
          <h3>{title}</h3>
          <p>{body}</p>
          <div class="ec-take">{take}</div>
        </div>
'''
    body_html = f'      <div class="exec">\n{col_html}      </div>'
    return content_slide(sec, kicker, h, desc, body_html, src, body_class="body--center")


def a_risks_table(sec, kicker, h, desc, rows, pull, src):
    tbody = ""
    for risk, lk, im, mit in rows:
        tbody += f'''          <tr class="risk-row">
            <td><b>{risk}</b></td>
            <td>{lk}</td>
            <td>{im}</td>
            <td>{mit}</td>
          </tr>
'''
    pull_html = ""
    if pull:
        pull_html = f'''      <div class="pull" style="margin-top:16px;">
        <div class="lbl">{pull[0]}</div>
        <p>{pull[1]}</p>
        <cite>{pull[2]}</cite>
      </div>'''
    body = f'''      <table class="dtable">
        <thead>
          <tr>
            <th style="width:24%">Risk</th>
            <th style="width:14%">Likelihood</th>
            <th style="width:14%">Impact</th>
            <th style="width:48%">Mitigation</th>
          </tr>
        </thead>
        <tbody>
{tbody}        </tbody>
      </table>
{pull_html}'''
    return content_slide(sec, kicker, h, desc, body, src, body_class="body--center")


TAG = {
    "high":   '<span class="tag tag--red">High</span>',
    "medium": '<span class="tag tag--yellow">Medium</span>',
    "watch":  '<span class="tag tag--blue">Watch</span>',
    "low":    '<span class="tag tag--green">Low</span>',
}


# ============================================================
# COVER VARIANTS: left panel fixed, right panel swaps
# ============================================================

COVER_LEFT = '''      <div class="cover__left">
        <div class="cover__brand">
          ''' + MS_MARK + '''
          <b>Microsoft</b><span class="sep">\u00b7</span>AI Platform Modernization
        </div>
        <div>
          <div class="cover__title">
            The platform decision behind every <span class="accent">production AI</span> outcome.
          </div>
          <div class="cover__sub">
            A strategic and technical brief on why enterprise AI initiatives
            stall before production, and the reference architecture that
            closes the gap between pilot and scale.
          </div>
          <div class="cover__chips">
            <span>Azure <b>AI Foundry</b></span>
            <span>GitHub <b>Copilot Enterprise</b></span>
            <span>Azure <b>Kubernetes Service</b></span>
            <span>Agentic <b>DevOps</b></span>
          </div>
        </div>
        <div class="cover__byline">
          <div><b>Frontier Cockpit Team</b>Software Global Black Belt</div>
          <div><b>Strategic &amp; Technical Brief</b>Client engagement \u00b7 2026</div>
        </div>
      </div>'''


def _cover(page, right_inner, top_label="Confidential \u00b7 Client brief"):
    inner = f'''    <div class="cover">
{COVER_LEFT}
      <div class="cover__right">
        <div class="cover__top">
          <span>{top_label}</span>
          <span><b>{page:02d} / {_TOTAL}</b></span>
        </div>
{right_inner}
      </div>
    </div>'''
    return bleed_slide("front", inner)


def cover_meeting(page):
    right = '''        <div class="cover__meeting">
          <div class="label">Session context</div>
          <div class="headline">
            A working session to decide the
            <b>platform scope and the first phase</b>.
          </div>
          <div class="cover__meeting__grid">
            <div><div class="mk">Client</div><div class="mv">Contoso Financial<span>Platform &amp; Engineering leadership</span></div></div>
            <div><div class="mk">Date</div><div class="mv">2026-05-20<span>90-minute briefing</span></div></div>
            <div><div class="mk">Session type</div><div class="mv">Strategic &amp; technical brief<span>Decision-oriented, not a pitch</span></div></div>
            <div><div class="mk">In the room</div><div class="mv">CTO, Head of Platform<span>Security and SRE leads</span></div></div>
          </div>
          <div class="decide">
            <b>Outcome we are after:</b> agreement on a three-week assessment
            window and the two candidate workloads to baseline. Placeholders
            for the reference template.
          </div>
        </div>'''
    return _cover(page, right)


def cover_stat(page):
    right = '''        <div class="cover__stat">
          <div class="label">The opening number</div>
          <div class="number">3<sup>\u00d7</sup></div>
          <div class="claim">
            longer time-to-production for AI workloads built on
            <b>ad hoc infrastructure</b> versus an opinionated platform baseline.
          </div>
          <div class="source">
            Illustrative figure for the reference template. Replace with
            <b>cited industry data</b> in real decks.
          </div>
        </div>
        <div class="cover__agenda">
          <div><b><span class="num">I.</span>Context</b>Where the market is</div>
          <div><b><span class="num">II.</span>Solution</b>Platform as the unit of delivery</div>
          <div><b><span class="num">III.</span>Execute</b>Roadmap and investment</div>
        </div>'''
    return _cover(page, right)


def cover_thesis(page):
    right = '''        <div class="cover__thesis">
          <div class="label">The thesis</div>
          <div class="statement">
            The model is not the bottleneck. The <b>platform underneath it</b>
            is what decides whether a pilot ever becomes a
            <mark>service the business can depend on</mark>.
          </div>
          <div class="support">
            This brief makes the case for treating the platform as the unit of
            delivery, then lays out the architecture, roadmap, and investment
            to build one. <b>Content is illustrative</b> for the reference template.
          </div>
        </div>'''
    return _cover(page, right)


def cover_pillars(page):
    right = '''        <div class="cover__pillars">
          <div class="label">Three horizons</div>
          <div class="lead">The brief is built on three moves, each earning the next.</div>
          <div class="cover__pillars__list">
            <div class="cover__pillars__item">
              <div class="pi-no">I</div>
              <div class="pi-body"><h4>Diagnose the gap</h4><p>Why pilots stall before production, sized with the client's own data.</p></div>
            </div>
            <div class="cover__pillars__item">
              <div class="pi-no">II</div>
              <div class="pi-body"><h4>Reframe the solution</h4><p>Platform as the unit of delivery, with an opinionated reference stack.</p></div>
            </div>
            <div class="cover__pillars__item">
              <div class="pi-no">III</div>
              <div class="pi-body"><h4>Execute the plan</h4><p>A staged roadmap, a clear investment, and an honest view of the risks.</p></div>
            </div>
          </div>
        </div>'''
    return _cover(page, right)


# ============================================================
# BACK-MATTER BLEED SLIDES
# ============================================================

def a_appendix_divider(page):
    inner = '''    <div class="appx">
      <div class="appx__eyebrow">Appendix</div>
      <div class="appx__h">Reference material</div>
      <div class="appx__desc">
        Supporting detail for the brief: the full assessment checklist,
        the service inventory, and the data behind each illustrative figure.
        Everything past this point is reference, not narrative.
      </div>
      <div class="appx__list">
        <span>Assessment checklist</span>
        <span>Service inventory</span>
        <span>Figure sources</span>
        <span>Glossary</span>
      </div>
    </div>'''
    return bleed_slide("back", inner)


def a_contact(page):
    inner = '''    <div class="contact">
      <div class="contact__left">
        <div class="cl-eyebrow">Next step</div>
        <h2>Confirm an assessment window, and we begin.</h2>
        <p>
          The three-week assessment is low-commitment and produces the client's
          own baseline. Everything after it is a decision made with real numbers.
        </p>
      </div>
      <div class="contact__right">
        <div class="contact__step">
          <div class="cs-k">What we need from you</div>
          <div class="cs-v">A <b>three-week window</b> and the two candidate workloads to baseline.</div>
        </div>
        <div class="contact__step">
          <div class="cs-k">What you get back</div>
          <div class="cs-v">A measured baseline and a prioritized platform scope.</div>
        </div>
        <div class="contact__sig">
          <div class="sg-name">Frontier Cockpit Team</div>
          <div class="sg-role">Software Global Black Belt</div>
          <div class="sg-mail">frontier-cockpit@example.com</div>
        </div>
      </div>
    </div>'''
    return bleed_slide("back", inner)

# ============================================================
# FULL 50-SLIDE ASSEMBLY
# ============================================================

def build_50():
    S = []

    # ===== FRONT MATTER (1-4), all 4 cover variants represented =====
    S.append(cover_meeting(1))           # 1  · cover (meeting context)
    S.append(s02_agenda())               # 2  · agenda
    S.append(s03_exec_summary())         # 3  · exec summary
    S.append(s04_quote())                # 4  · quote

    # ===== SECTION 1 · CONTEXT (5-13) · blue =====
    S.append(a_divider("ctx", "I", "Section 1 \u00b7 Context",
        "Where the market is on production AI",
        "Adoption is wide and shallow. Pilots are everywhere; production is rare. This section sizes that gap before naming its causes.",
        ["How wide is AI adoption, really?", "How narrow is production?",
         "Where does the typical team sit?"], 1))                       # 5
    S.append(a_section_intro("ctx"))                                    # 6
    S.append(a_big_number("ctx", "Adoption signal",
        "Almost everyone is <b>piloting</b>. Almost no one is <mark>shipping</mark>.",
        "The headline gap is not interest in AI. It is the distance between a team that runs experiments and a team that runs services.",
        "The core metric", "9", "/10",
        "enterprises in this scenario run at least one AI pilot. Illustrative figure.",
        [("Reach a demo", "~80%", "of pilots produce a working demonstration of value.", ""),
         ("Reach production", "~12%", "of those demos become a governed, monitored service.", ""),
         ("The drop", "1", "platform layer separates the two numbers above.", "accent")],
        "<b>Note \u00b7</b> All figures are placeholders. Real client decks must cite named, dated sources."))  # 7
    S.append(a_metrics_dashboard("ctx"))                                # 8
    S.append(a_data_table("ctx", "The landscape",
        "Four ways teams approach AI infrastructure today, and <b>what each costs</b>.",
        "A side-by-side of the common patterns. Most teams are somewhere in the first two rows, and that is the problem.",
        [("Approach", None, "24%"), ("Who does it", None, "16%"),
         ("What it optimizes for", None, "32%"), ("Recurs", "num", "14%"),
         ("Maturity", None, "14%")],
        [[("<b>Per-project setup</b>", None), ("Each app team", None),
          ("Speed of the first demo", None), ("Per project", "num"),
          ('<span class="tag tag--red">Low</span>', None)],
         [("<b>Shared scripts</b>", None), ("A platform champion", None),
          ("Reuse, informally", None), ("Per team", "num"),
          ('<span class="tag tag--yellow">Partial</span>', None)],
         [("<b>Cloud-managed PaaS</b>", None), ("Vendor", None),
          ("Time to first deploy", None), ("Per workload", "num"),
          ('<span class="tag tag--blue">Medium</span>', None)],
         [("<b>Reference platform</b>", None), ("Owned once, consumed by all", None),
          ("Repeatable path to production", None), ("Once", "num"),
          ('<span class="tag tag--green">High</span>', None)]],
        ("Read this as", "Maturity rises only when the platform is <b>owned once</b> instead of rebuilt per project.",
         "Synthesis line \u00b7 <b>reference template</b>"),
        "<b>Maturity banding</b> is qualitative. Replace with the client's own assessment."))  # 9
    S.append(a_quadrant("ctx", "Where teams sit today",
        "Most AI work clusters in the <b>wrong quadrant</b>: high ambition, low readiness.",
        "A simple read of the field. Vertical axis is platform maturity; horizontal is AI ambition. The gap is the distance teams must close.",
        "Platform maturity &rarr;", "AI ambition &rarr;",
        [("Top left", "Over-built", "Strong platform, little AI demand on it yet.", False),
         ("Top right \u00b7 target", "Production-ready", "Platform maturity matches AI ambition.", True),
         ("Bottom left", "Early days", "Low on both axes. Honest starting point.", False),
         ("Bottom right \u00b7 where most sit", "Ambition outruns foundation", "High AI ambition, thin platform.", False)],
        [("them", "31%", "34%"), ("us", "74%", "71%")],
        [("var(--ms-red)", "Typical client today"), ("var(--silver)", "Peer benchmark")],
        "<b>Axis note \u00b7</b> Replace dot positions with the client's own self-assessment scores."))  # 10
    S.append(a_before_after("ctx", "Expectation vs reality",
        "What teams <b>expect</b> from an AI pilot, and what they <b>get</b>.",
        "The gap between the two columns is not failure. It is the predictable result of building without a platform.",
        "Expectation \u00b7 going in",
        ["A pilot proves value in weeks.", "A successful demo ships to production.",
         "The next pilot reuses the first one's work.", "Governance is a final checkbox.",
         "Cost and behavior are visible by default."],
        "Reality \u00b7 without a platform",
        ["The demo works; the path to production does not.",
         "The demo stalls waiting for infrastructure.",
         "The next pilot starts from zero again.",
         "Governance is a late, expensive surprise.",
         "Cost and behavior live in scattered places."],
        [("Demos that ship", "~12%", "reach production"),
         ("Setup, repeated", "Per pilot", "not once"),
         ("Gap", "Predictable", "and fixable", True)],
        "<b>Outcome figures</b> are directional placeholders. Validate against a client baseline."))  # 11
    S.append(a_case_study("ctx"))                                       # 12
    S.append(a_stakeholder_map("ctx"))                                  # 13

    # ===== SECTION 2 · THE PROBLEM (14-22) · green =====
    S.append(a_divider("prob", "II", "Section 2 \u00b7 The problem",
        "Why pilots stall before production",
        "The blocker is rarely the model. It is everything underneath: environments, data access, governance, and the route to a running service.",
        ["Where exactly do pilots break down?", "What does the delay cost?",
         "Is this a tooling problem or a platform problem?"], 4))        # 14
    S.append(a_big_number("prob", "The gap",
        "Most teams reach a <b>working demo</b>. Far fewer reach a <mark>governed service</mark>.",
        "The distance between those two states is the platform gap. It shows up as repeated setup, inconsistent data access, and no standard route to production.",
        "The core metric", "68", "%",
        "of AI pilots in this scenario never get a production deployment target assigned.",
        [("Symptom 1 \u00b7 Environments", "~40h", "spent per team, per quarter, re-creating environments by hand.", ""),
         ("Symptom 2 \u00b7 Governance", "0", "consistent policy gates between an experiment and an endpoint.", ""),
         ("Root cause", "1", "missing platform layer. Every symptom traces back to it.", "accent")],
        "<b>Note \u00b7</b> All figures are placeholders for the reference template."))  # 15
    S.append(a_data_table("prob", "Cost of delay",
        "The platform gap has a <b>line-item cost</b>. Here is where it accrues.",
        "Five recurring friction points, the team they tax, and the effect on delivery.",
        [("Friction point", None, "22%"), ("Primary owner", None, "16%"),
         ("Effect on delivery", None, "30%"), ("Recurs", "num", "14%"),
         ("Severity", None, "18%")],
        [[("<b>Manual environment setup</b>", None), ("Platform team", None),
          ("Each new workload restarts from zero infrastructure.", None),
          ("Per project", "num"), ('<span class="tag tag--red">High</span>', None)],
         [("<b>Inconsistent data access</b>", None), ("Data engineering", None),
          ("Credentials and patterns differ across every team.", None),
          ("Per team", "num"), ('<span class="tag tag--red">High</span>', None)],
         [("<b>No standard CI path</b>", None), ("App teams", None),
          ("Each repo invents its own build and release flow.", None),
          ("Per repo", "num"), ('<span class="tag tag--yellow">Medium</span>', None)],
         [("<b>Governance applied late</b>", None), ("Security", None),
          ("Policy checks happen after build, forcing rework.", None),
          ("Per release", "num"), ('<span class="tag tag--yellow">Medium</span>', None)],
         [("<b>Fragmented observability</b>", None), ("SRE", None),
          ("No shared view of cost, latency, or model behavior.", None),
          ("Continuous", "num"), ('<span class="tag tag--blue">Watch</span>', None)]],
        ("Read this as", "Every row is <b>solvable once</b> at the platform layer instead of <b>repeatedly</b> at the project layer.",
         "Synthesis line \u00b7 <b>reference template</b>"),
        "<b>Severity banding</b> is illustrative. Replace with the client's own incident data."))  # 16
    S.append(a_pillar_grid("prob", "Root causes",
        "Five symptoms, <b>three root causes</b>.",
        "The cost-of-delay table lists what teams feel. These are the three underlying causes that produce all of it.",
        [("01", "No shared foundation", "Every workload re-derives networking, identity, and a release path because nothing provides them by default."),
         ("02", "Governance bolted on", "Policy lives outside the delivery path, so it is discovered late and applied as rework rather than as a property of shipping."),
         ("03", "No common signal", "Cost, latency, and model behavior live in team-local dashboards, so problems surface in weeks instead of hours.")],
        "<b>Cause note \u00b7</b> Three is deliberate. A long list of causes is a list nobody acts on."))  # 17
    S.append(a_flow("prob", "The broken path",
        "Without a platform, the path to production <b>breaks at every hand-off</b>.",
        "Four stages, four points of friction. Each arrow is where a workload waits or stalls.",
        [("1", "Scaffold", "Starts from an empty repo. Infrastructure negotiated by hand."),
         ("2", "Build", "Each team invents its own CI. No shared evaluation or policy."),
         ("3", "Deploy", "No standard runtime target. Networking and scaling re-decided."),
         ("4", "Operate", "Observability is team-local. Problems surface late.")],
        "<b>Flow note \u00b7</b> Compare this to the governed path in the next section, stage for stage."))  # 18
    S.append(a_risks_table("prob", "What compounds it",
        "The problem does not sit still. <b>Four things make it worse</b> over time.",
        "Left alone, the platform gap compounds. Each row is a force that widens it.",
        [("Each new pilot adds debt", TAG["high"], TAG["high"],
          "Every project built the old way is one more thing to migrate later."),
         ("Teams diverge further", TAG["high"], TAG["medium"],
          "Without a shared path, each team's setup drifts further from every other."),
         ("Governance debt accrues", TAG["medium"], TAG["high"],
          "Late policy means rework piles up release after release."),
         ("Knowledge stays siloed", TAG["medium"], TAG["medium"],
          "What one team learns the hard way, the next team learns again.")],
        ("Why this matters now", "The gap is cheapest to close <b>today</b>. Every quarter of delay adds workloads to migrate and divergence to undo.",
         "Synthesis line \u00b7 <b>reference template</b>"),
        "<b>Banding note \u00b7</b> Likelihood and impact are qualitative. Calibrate with the client."))  # 19
    S.append(a_quote("prob",
        "We did not have an AI problem. We had <mark>twelve different definitions</mark> of what it meant to put a model in production.",
        "Practitioner voice \u00b7 <b>reference template</b>, illustrative attribution"))  # 20
    S.append(a_exec_summary("prob", "Problem recap",
        "The problem in <b>three lines</b>, before we turn to the solution.",
        "A mid-deck recap. If the room lost the thread, this is where it picks back up.",
        [("1", "It is a platform problem", "Not a model problem, not a talent problem. The blocker is the absence of a shared foundation.", "<b>So what \u00b7</b> The fix is structural, not another pilot."),
         ("2", "It has a real cost", "Repeated setup, late governance, fragmented signal. Measurable, and paid every quarter.", "<b>So what \u00b7</b> Inaction is not free; it compounds."),
         ("3", "It compounds", "Every quarter of delay adds workloads to migrate and divergence to undo.", "<b>So what \u00b7</b> The cheapest time to act is now.")],
        "<b>Recap note \u00b7</b> This mirrors the front-matter exec summary, refocused on the problem."))  # 21
    S.append(a_section_intro("prob"))                                   # 22

    # ===== SECTION 3 · THE SOLUTION (23-31) · yellow =====
    S.append(a_divider("sol", "III", "Section 3 \u00b7 The solution",
        "Platform as the unit of delivery",
        "Stop shipping AI projects. Start shipping a platform that makes the next AI project boring, fast, and governed by default.",
        ["What does the reference stack look like?",
         "What changes for the teams using it?",
         "What about the obvious objections?"], 8))                     # 23
    S.append(a_section_intro("sol"))                                    # 24
    S.append(a_layer_stack("sol", "Reference stack",
        "Four layers, <b>each owned once</b>, each removing a row from the cost-of-delay table.",
        "The stack is opinionated on purpose. Teams consume it; they do not re-derive it. Layer colors map to the Microsoft palette.",
        [("Experience", "Developer portal &amp; golden paths",
          "Self-service templates so a new AI workload starts from a governed baseline, not a blank repo."),
         ("Delivery", "Standard CI/CD with policy gates",
          "One build-and-release path. Governance runs inside the pipeline, not after it."),
         ("Runtime", "Azure Kubernetes Service landing zone",
          "A consistent place to run workloads, with networking, identity, and scaling decided once."),
         ("Intelligence", "Azure AI Foundry &amp; model governance",
          "Shared model catalog, evaluation, and observability so every team sees cost and behavior the same way.")],
        "<b>Architecture note \u00b7</b> Layer names are generic. Real decks name the client's specific services and versions."))  # 25
    S.append(a_pillar_grid("sol", "Operating principles",
        "The stack works because <b>three principles</b> hold it together.",
        "Architecture describes the what. These principles describe the how, and they keep the platform from drifting back into per-project chaos.",
        [("01", "Opinionated by default", "The platform makes the common choices so teams do not. A new workload inherits networking, identity, and a release path."),
         ("02", "Governed in the path", "Policy runs inside the pipeline, not as a gate discovered late. Compliance becomes a property of shipping."),
         ("03", "Observable end to end", "One shared view of cost, latency, and model behavior. Every team reads the same dashboard.")],
        "<b>Principle note \u00b7</b> These are deliberately few. A long list of principles is a list nobody follows."))  # 26
    S.append(a_before_after("sol", "Before / after",
        "What changes for the teams <b>consuming the platform</b>.",
        "The platform layer is invisible when it works. The visible result is a different day-to-day for app teams, security, and SRE.",
        "Before \u00b7 project-by-project",
        ["New workload starts from an empty repository and a wiki page.",
         "Each team negotiates its own data access and secrets.",
         "Security review is a gate discovered late, near release.",
         "Cost and latency live in scattered, team-local dashboards.",
         "Production readiness is argued case by case."],
        "After \u00b7 platform-as-default",
        ["New workload starts from a golden-path template.",
         "Data access patterns are inherited, not re-negotiated.",
         "Policy gates run inside the standard pipeline.",
         "One shared view of cost, latency, and model behavior.",
         "Production readiness is a checklist the platform enforces."],
        [("Setup time", "&minus;70%", "environment provisioning"),
         ("Policy rework", "&minus;1 stage", "governance shifts left"),
         ("Time to prod", "Weeks &rarr; days", "directional outcome", True)],
        "<b>Outcome figures</b> are directional placeholders. Validate against a client baseline."))  # 27
    S.append(a_flow("sol", "The governed path",
        "With the platform in place, a workload moves through <b>four governed stages</b>.",
        "Each stage has a clear owner and a clear hand-off. Nothing is improvised, and nothing waits on a meeting.",
        [("1", "Scaffold", "Start from a golden-path template with identity and networking pre-wired."),
         ("2", "Build", "Standard CI runs tests, evaluations, and policy checks in one pass."),
         ("3", "Deploy", "Release to the AKS landing zone with scaling and rollback already defined."),
         ("4", "Operate", "Shared observability tracks cost, latency, and model behavior from day one.")],
        "<b>Flow note \u00b7</b> This is the broken-path slide from Section 2, fixed stage for stage."))  # 28
    S.append(a_metrics_dashboard("sol"))                                # 29
    S.append(a_case_study("sol"))                                       # 30
    S.append(a_faq("sol"))                                              # 31

    # ===== SECTION 4 · ARCHITECTURE (32-39) · red =====
    S.append(a_divider("arch", "IV", "Section 4 \u00b7 Architecture",
        "How it fits together",
        "The diagnosis and the reframe are settled. This section is the annotated architecture: real components, real decisions, called out in the open.",
        ["What are the components, concretely?",
         "How does the pipeline enforce governance?",
         "Build, buy, or reference platform?"], 11))                    # 32
    S.append(a_section_intro("arch"))                                   # 33
    S.append(a_architecture_detail("arch"))                             # 34
    S.append(a_layer_stack("arch", "Runtime layer, expanded",
        "The runtime layer is where <b>most decisions get made once</b>.",
        "Zooming into the AKS landing zone: four concerns that every workload would otherwise re-decide, settled at the platform level.",
        [("Networking", "Virtual network &amp; ingress",
          "One network topology, one ingress pattern. Workloads attach; they do not design."),
         ("Identity", "Workload identity &amp; secrets",
          "Managed identity and a single secrets pattern. No per-team credential negotiation."),
         ("Scaling", "Autoscaling &amp; resource policy",
          "Scaling rules and resource quotas defined once, inherited by every namespace."),
         ("Isolation", "Namespace &amp; policy boundaries",
          "Each team gets a bounded space with guardrails, not a blank cluster.")],
        "<b>Architecture note \u00b7</b> Component names are generic. Real decks name the client's specific services."))  # 35
    S.append(a_flow("arch", "CI/CD with policy gates",
        "The pipeline is where <b>governance becomes automatic</b>.",
        "Four stages, with policy embedded in stages two and three. Nothing reaches production without passing through them.",
        [("1", "Commit", "Code and config land in a standard repo structure."),
         ("2", "Build &amp; check", "Tests, model evaluation, and policy gates run in one pass."),
         ("3", "Promote", "Signed artifacts move through environments with rollback defined."),
         ("4", "Observe", "Cost, latency, and behavior stream to the shared dashboard.")],
        "<b>Flow note \u00b7</b> Policy lives in stage 2. That single placement is what shifts governance left."))  # 36
    S.append(a_data_table("arch", "Service inventory",
        "Every component, <b>by layer</b>, with its role and owner.",
        "The architecture diagram, written out as a table. This is the reference list a platform team works from.",
        [("Service", None, "24%"), ("Layer", None, "16%"),
         ("Role", None, "38%"), ("Owner", None, "22%")],
        [[("<b>Developer portal</b>", None), ('<span class="tag tag--blue">Experience</span>', None),
          ("Golden-path templates and self-service provisioning.", None), ("Platform team", None)],
         [("<b>Standard CI/CD</b>", None), ('<span class="tag tag--green">Delivery</span>', None),
          ("Build, evaluate, gate, and promote in one path.", None), ("Platform team", None)],
         [("<b>Policy engine</b>", None), ('<span class="tag tag--green">Delivery</span>', None),
          ("In-pipeline governance rules and enforcement.", None), ("Security", None)],
         [("<b>AKS landing zone</b>", None), ('<span class="tag tag--yellow">Runtime</span>', None),
          ("Networking, identity, scaling, isolation.", None), ("Platform team", None)],
         [("<b>Azure AI Foundry</b>", None), ('<span class="tag tag--red">Intelligence</span>', None),
          ("Model catalog, evaluation, and versioning.", None), ("Platform team", None)],
         [("<b>Observability stack</b>", None), ('<span class="tag tag--red">Intelligence</span>', None),
          ("Shared cost, latency, and model-behavior signal.", None), ("SRE", None)]],
        ("How to use this", "This table is the <b>build checklist</b>. Phase 2 of the roadmap stands up rows one through four; rows five and six follow in Phase 3.",
         "Synthesis line \u00b7 <b>reference template</b>"),
        "<b>Inventory note \u00b7</b> Services are generic. Real decks name specific SKUs and versions."))  # 37
    S.append(a_vendor_compare("arch"))                                  # 38
    S.append(a_decision_matrix("arch"))                                 # 39

    # ===== SECTION 5 · THE PLAN (40-45) · blue =====
    S.append(a_divider("plan", "V", "Section 5 \u00b7 The plan",
        "From decision to a platform teams build on",
        "The architecture is settled. What remains is a staged path, a clear team, and an honest view of who owns what.",
        ["What is the staged path and timeline?",
         "Who runs the engagement?",
         "Who owns the platform afterward?"], 14))                      # 40
    S.append(a_roadmap("plan", "Modernization roadmap",
        "A <b>staged path</b> from assessment to a platform other teams build on.",
        "Each phase ends with something usable. No phase depends on the next one being perfect. Timeframes are indicative.",
        [("Phase 1", "Assess", "Weeks 1&ndash;3",
          ["Map current AI workloads and blockers", "Baseline delivery and cost metrics", "Agree target platform scope"],
          "Exit criteria", "Signed-off <b>scope document</b> and a measured delivery baseline."),
         ("Phase 2", "Foundation", "Weeks 4&ndash;9",
          ["Stand up the AKS landing zone", "Establish identity and networking", "Wire the standard CI/CD path"],
          "Exit criteria", "One workload running through the <b>standard pipeline</b> end to end."),
         ("Phase 3", "Golden paths", "Weeks 10&ndash;16",
          ["Publish self-service templates", "Onboard two pilot teams", "Embed policy gates and observability"],
          "Exit criteria", "Two pilot teams shipping from <b>golden-path templates</b>."),
         ("Phase 4", "Scale", "Weeks 17+",
          ["Roll out to remaining teams", "Hand platform ownership to client", "Establish continuous improvement loop"],
          "Exit criteria", "Platform <b>owned by the client</b>, with an active improvement loop.")],
        "<b>Timeframes</b> assume a mid-size org with an existing Azure footprint. Re-scope per engagement."))  # 41
    S.append(a_gantt("plan"))                                           # 42
    S.append(a_team("plan"))                                            # 43
    S.append(a_raci("plan"))                                            # 44
    S.append(a_risks_table("plan", "Engagement risks",
        "The honest version: <b>what could go wrong</b>, and how each is handled.",
        "A proposal without a risk slide is a sales pitch. Each row pairs a real risk with a concrete mitigation already in the plan.",
        [("Teams resist a shared platform", TAG["medium"], TAG["high"],
          "Two pilot teams co-design the golden paths in Phase 3, so the platform reflects real workflows."),
         ("Scope expands mid-engagement", TAG["high"], TAG["medium"],
          "Phase 1 ends with a signed scope document. Changes are explicit re-scopes, not silent creep."),
         ("Existing Azure footprint conflicts", TAG["medium"], TAG["medium"],
          "The assessment maps the current estate first. The landing zone is designed around what exists."),
         ("Hand-over leaves a knowledge gap", TAG["medium"], TAG["high"],
          "Client engineers work inside Phases 2 and 3, not just at the end. Ownership transfers gradually."),
         ("Platform value is hard to prove", TAG["watch"], TAG["medium"],
          "The Phase 1 baseline is the comparison point. Later metrics read against the client's own start line.")],
        ("Why this slide exists", "Naming risks early is what makes the rest of the proposal <b>credible</b>. Every mitigation here is already a line in the roadmap.",
         "Synthesis line \u00b7 <b>reference template</b>"),
        "<b>Banding note \u00b7</b> Likelihood and impact are qualitative. Calibrate with the client during the assessment."))  # 45

    # ===== SECTION 6 · INVESTMENT (46-48) · green =====
    S.append(a_divider("invest", "VI", "Section 6 \u00b7 Investment",
        "What it takes, and what it returns",
        "The plan is set. This section is the investment shape: three engagement sizes, the specific ask, and the recommendation.",
        ["What does each engagement size include?",
         "What is the specific first ask?"], 16))                       # 46
    S.append(a_pricing("invest", "Investment shape",
        "Three engagement sizes. <b>Each ends with something usable</b>, none locks in the next.",
        "Figures are placeholders. The point is the shape: a small committed first step, a foundation phase, and a full rollout chosen on evidence.",
        [("Tier 1 \u00b7 Assess", "3 wks", "\u00b7 fixed", "Low commitment, high clarity",
          ["Workload and blocker inventory", "Delivery and cost baseline",
           "Prioritized platform scope", "Go or no-go recommendation"],
          "Ends with <b>the client's own data</b> and a clear decision point.", False, ""),
         ("Tier 2 \u00b7 Foundation", "6 wks", "\u00b7 scoped", "The platform baseline, stood up",
          ["AKS landing zone live", "Identity and networking established",
           "Standard CI/CD path wired", "One workload running end to end"],
          "Ends with a <b>working platform</b> and one production workload on it.", True, "Most common start"),
         ("Tier 3 \u00b7 Scale", "Ongoing", "\u00b7 phased", "Rollout and hand-over",
          ["Golden-path templates published", "Remaining teams onboarded",
           "Ownership transferred to client", "Continuous improvement loop"],
          "Ends with the platform <b>owned and run by the client</b> team.", False, "")],
        "<b>Pricing note \u00b7</b> Durations are illustrative. Real proposals carry costed figures reviewed with the account team."))  # 47
    S.append(a_recommendation("invest", "Recommendation",
        "Start with a <b>three-week assessment</b>. Decide the platform scope on evidence, not on this deck.",
        "The assessment is low-commitment and produces the client's own baseline. Everything after it is a decision the client makes with real numbers.",
        [("01", "Immediate \u00b7 the assessment", "Three weeks, fixed scope. Produces a baseline of delivery metrics and a prioritized blocker list."),
         ("02", "Near-term \u00b7 the foundation", "Stand up the landing zone and standard pipeline. First pilot team onboarded by week nine."),
         ("03", "Sustained \u00b7 the handover", "Platform ownership transfers to the client team with golden paths and an improvement loop in place.")],
        "The ask", "3 wks", "to a decision backed by <b>the client's own data</b>, not assumptions.",
        "Next step", "Confirm an assessment window and the two candidate workloads to baseline.",
        "Contact \u00b7 <b>frontier-cockpit@example.com</b>",
        "<b>This is a reference template.</b> Structure, palette, and component set are the deliverable; the content is illustrative."))  # 48

    # ===== BACK MATTER (49-53) · neutral / red =====
    # 48 content slides, then the appendix opens with the cover-variant
    # reference (the other 3 cover layouts), then the contact close.
    S.append(a_appendix_divider(49))                                    # 49
    S.append(cover_stat(50))                                            # 50
    S.append(cover_thesis(51))                                          # 51
    S.append(cover_pillars(52))                                         # 52
    S.append(a_contact(53))                                             # 53

    return S


# ============================================================
# SPLICE + MAIN
# ============================================================

def splice(template_path, slides, total, out_path, deck_title):
    try:
        src = open(template_path, encoding="utf-8").read()
    except OSError as exc:
        sys.exit(f"ERROR: cannot read template {template_path}: {exc}")
    head_end = src.index('<section class="slide')
    head = src[:head_end]
    tail_start = src.rindex('</section>') + len('</section>')
    tail = src[tail_start:]

    toc = "\n".join(f'      <a href="#x{i+1}">{i+1:02d}</a>' for i in range(total))
    head = re.sub(r'<nav class="deck-toc">.*?</nav>',
                  f'<nav class="deck-toc">\n{toc}\n    </nav>', head, flags=re.S)
    head = re.sub(r'<div class="deck-hdr__title">.*?</div>',
                  f'<div class="deck-hdr__title">{deck_title}</div>', head, flags=re.S)
    head = re.sub(r'\d+ slides \u00b7 16:9', f'{total} slides \u00b7 16:9', head)
    head = re.sub(r'(Mock reference|Archetype showcase) <b>v[\d.]+</b>',
                  'Reference template <b>v1.0</b>', head)

    body = ""
    for i, s in enumerate(slides, 1):
        s = s.replace('<section class="slide', f'<section id="x{i}" class="slide', 1)
        s = s.replace("<b>PP</b>", f"<b>{i:02d}</b>")
        body += s + "\n\n"
    html = head + body + tail
    if html.count('<section') < total:
        sys.exit(f"ERROR: generated HTML has fewer than {total} slide sections")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    if not os.path.isfile(out_path) or os.path.getsize(out_path) == 0:
        sys.exit(f"ERROR: output HTML is missing or empty: {out_path}")
    return out_path


if __name__ == "__main__":
    import argparse, os
    SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE = os.path.join(SKILL_DIR, "assets", "deck-template.html")
    ap = argparse.ArgumentParser(
        description="Build the 53-slide Gartner-style HTML deck.")
    ap.add_argument("--out", default="ms-reference-deck.html",
                    help="output HTML path")
    ap.add_argument("--template", default=TEMPLATE,
                    help="CSS source-of-truth template (assets/deck-template.html)")
    ap.add_argument("--title",
                    default="AI Platform Modernization \u00b7 53-Slide Reference Template",
                    help="deck title shown in the header")
    args = ap.parse_args()
    slides = build_50()
    total = len(slides)
    out = splice(args.template, slides, total, args.out, args.title)
    print(f"wrote {out} with {total} slides")
