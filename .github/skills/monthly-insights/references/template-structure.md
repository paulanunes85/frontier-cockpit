# Monthly Insights - HTML Template Structure Reference

This document contains the full CSS class definitions and HTML patterns used in the Monthly Insights report. Use this as a copy-paste reference when building reports.

## Table of Contents

1. [Full CSS Block](#full-css-block)
2. [Header + Nav Pattern](#header--nav)
3. [Introduction Pattern](#introduction)
4. [Portfolio Overview Table](#portfolio-overview-table)
5. [Account Card Pattern](#account-card)
6. [Additional Accounts Grid](#additional-accounts-grid)
7. [Insight Callout Boxes](#insight-callouts)
8. [KPI Row Pattern](#kpi-row)
9. [Audience Panel Pattern](#audience-panel)
10. [Chart.js Configuration Examples](#chartjs-configs)
11. [Data Table Pattern](#data-table)
12. [Competitive Landscape Table](#competitive-landscape)
13. [Section Dividers](#section-dividers)

---

## Full CSS Block

```css
:root{--blue:#0078D4;--green:#107C10;--red:#D83B01;--yellow:#FFB900;--dark:#1B1A19;--gray:#605E5C;--light:#F3F2F1;--purple:#8957E5;--gh:#24292F;--teal:#008272}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:#f9f9f9;color:var(--dark);line-height:1.55}
.header{background:linear-gradient(135deg,var(--gh),#2d333b);color:#fff;padding:36px 48px;border-bottom:4px solid var(--blue)}
.header h1{font-size:26px;font-weight:600;margin-bottom:4px}
.header p{font-size:13px;opacity:.8}
.nav{background:#fff;border-bottom:1px solid #e1dfdd;padding:10px 48px;display:flex;gap:6px;flex-wrap:wrap;position:sticky;top:0;z-index:10;box-shadow:0 1px 3px rgba(0,0,0,.05)}
.nav a{font-size:11px;padding:5px 12px;border-radius:16px;text-decoration:none;color:var(--gray);background:var(--light);transition:.15s;white-space:nowrap}
.nav a:hover{background:var(--blue);color:#fff}
.c{max-width:1200px;margin:0 auto;padding:28px 24px}
.divider{margin:40px 0 32px;border:none;border-top:2px solid var(--light);position:relative}
.divider-label{position:absolute;top:-10px;left:0;background:#f9f9f9;padding:0 14px 0 0;font-size:12px;font-weight:600;color:var(--blue);text-transform:uppercase;letter-spacing:.5px}
.intro{background:#fff;border-radius:12px;padding:24px 28px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:28px;border-left:5px solid var(--blue);font-size:13px;line-height:1.7}
.intro p{margin-bottom:10px}
.intro p:last-child{margin-bottom:0}
.kpi{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;margin-bottom:28px}
@media(max-width:900px){.kpi{grid-template-columns:repeat(2,1fr)}}
.k{background:#fff;border-radius:10px;padding:20px;text-align:center;box-shadow:0 1px 3px rgba(0,0,0,.07);border-top:4px solid var(--blue)}
.k.r{border-top-color:var(--red)}.k.y{border-top-color:var(--yellow)}.k.g{border-top-color:var(--green)}.k.p{border-top-color:var(--purple)}
.k .v{font-size:32px;font-weight:700;margin:6px 0}
.k .l{font-size:11px;color:var(--gray);text-transform:uppercase;letter-spacing:.5px}
.k .s{font-size:11px;color:var(--gray);margin-top:3px}
.sec{margin-bottom:32px}
.sec-t{font-size:18px;font-weight:600;margin-bottom:14px;padding-bottom:6px;border-bottom:2px solid var(--light);display:flex;align-items:center;gap:8px}
.badge{font-size:10px;padding:2px 8px;border-radius:12px;font-weight:600;text-transform:uppercase}
.badge.sp{background:#DEECF9;color:var(--blue)}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:768px){.g2{grid-template-columns:1fr}}
.card{background:#fff;border-radius:10px;padding:22px;box-shadow:0 1px 3px rgba(0,0,0,.07)}
.card h3{font-size:14px;font-weight:600;margin-bottom:3px}
.card .sub{font-size:11px;color:var(--gray);margin-bottom:14px}
.ch{position:relative;height:260px}
.ins{padding:14px 18px;border-radius:0 8px 8px 0;margin:16px 0;font-size:13px;line-height:1.55}
.ins.warn{background:#FFF4CE;border-left:4px solid var(--yellow)}
.ins.crit{background:#FDE7E9;border-left:4px solid var(--red)}
.ins.info{background:#DEECF9;border-left:4px solid var(--blue)}
.ins.ok{background:#DFF6DD;border-left:4px solid var(--green)}
.ins strong{color:var(--dark)}
.ap{background:#fff;border-radius:12px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.07);border-left:5px solid var(--blue)}
.ap.sp{border-left-color:var(--purple)}
.ap h3{font-size:16px;font-weight:700;margin-bottom:3px}
.ap .meta{font-size:11px;color:var(--gray);margin-bottom:14px}
.sr{display:flex;gap:12px;margin-bottom:14px;flex-wrap:wrap}
.st{flex:1;min-width:80px;background:var(--light);border-radius:8px;padding:10px 12px;text-align:center}
.st .n{font-size:24px;font-weight:700}.st .lb{font-size:10px;color:var(--gray);text-transform:uppercase;margin-top:1px}
.rb{height:7px;border-radius:4px;background:#E1DFDD;margin:6px 0;overflow:hidden}
.rb .f{height:100%;border-radius:4px}
.rl{display:flex;justify-content:space-between;font-size:10px;color:var(--gray)}
.fc{background:var(--light);border-radius:8px;padding:12px 14px;margin-bottom:8px;border-left:4px solid var(--blue);font-size:12px;line-height:1.5}
.fc.r{border-left-color:var(--red)}.fc.g{border-left-color:var(--green)}.fc.y{border-left-color:var(--yellow)}.fc.p{border-left-color:var(--purple)}
.fc strong{font-size:13px;display:block;margin-bottom:2px}
table.dt{width:100%;border-collapse:collapse;font-size:13px}
.dt th{text-align:left;padding:8px 10px;background:var(--gh);color:#fff;font-weight:600;font-size:11px;text-transform:uppercase}
.dt td{padding:8px 10px;border-bottom:1px solid var(--light)}
.dt tr:hover td{background:#f5f5f5}
.bc{display:flex;align-items:center;gap:6px}.bf{height:18px;border-radius:3px;min-width:3px}
.acct{background:#fff;border-radius:12px;padding:24px 28px;box-shadow:0 1px 3px rgba(0,0,0,.07);margin-bottom:18px;border-left:5px solid var(--blue)}
.acct.high{border-left-color:var(--red)}.acct.med{border-left-color:var(--yellow)}.acct.low{border-left-color:var(--green)}
.acct h3{font-size:17px;font-weight:700;margin-bottom:2px}
.acct .ainfo{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;font-size:11px;color:var(--gray);align-items:center}
.acct .ainfo .sep{color:#ccc}
.acct .ameta{font-size:11px;color:var(--gray);margin-bottom:14px;display:flex;gap:8px;flex-wrap:wrap}
.tag{display:inline-block;font-size:9px;padding:2px 7px;border-radius:10px;font-weight:600;text-transform:uppercase;margin-right:2px}
.tag.aws{background:#FF9900;color:#fff}
.tag.gl{background:#FC6D26;color:#fff}
.tag.dr{background:#E1DFDD;color:var(--dark)}
.tag.fp{background:#DEECF9;color:var(--blue)}
.tag.ag{background:#DFF6DD;color:var(--green)}
.tag.mm{background:#EDE0FF;color:var(--purple)}
.tag.ent{background:#0078D4;color:#fff}
.tag.pub{background:#107C10;color:#fff}
.tag.ind{background:var(--gh);color:#fff}
.acct p.desc{font-size:13px;line-height:1.6;margin-bottom:14px;color:#444}
.acct ul{margin:0;padding-left:20px;font-size:13px;line-height:1.7}
.acct ul li{margin-bottom:6px}
.addl{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:14px}
@media(max-width:768px){.addl{grid-template-columns:1fr}}
.addl-item{background:#fff;border-radius:10px;padding:16px 14px;box-shadow:0 1px 3px rgba(0,0,0,.07);font-size:13px;border-top:3px solid var(--blue)}
.addl-item strong{display:block;font-size:14px;margin-bottom:3px}
.addl-item span{font-size:10px;color:var(--gray)}
.footer{text-align:center;padding:28px;color:var(--gray);font-size:11px}
```

---

## Header + Nav

```html
<div class="header">
  <h1>Monthly Insights - Brazil & LATAM Key Accounts</h1>
  <p>Q3 FY26 &nbsp;|&nbsp; March 2026 &nbsp;|&nbsp; Frontier Cockpit Team - Software Global Black Belt</p>
</div>
<div class="nav">
  <a href="#intro">Introduction</a>
  <a href="#petrobras">Petrobras</a>
  <!-- ... more account links ... -->
  <a href="#observations">Observations</a>
  <a href="#workshops">Workshop Data</a>
  <a href="#priorities">Priorities</a>
</div>
```

---

## Introduction

```html
<div id="intro" class="intro">
  <p>This report consolidates field observations... for <strong>Q3 FY26 (January - March 2026)</strong>.</p>
  <p>It covers <strong>7 priority accounts</strong> and <strong>6 additional accounts</strong> spanning Energy, Mining, Government IT...</p>
  <p>All strategic efforts are concentrated on these accounts through...</p>
</div>
```

---

## Portfolio Overview Table

```html
<div class="card">
  <table class="dt">
    <thead><tr><th>Account</th><th>Country</th><th>Industry</th><th>Segment</th><th>Key Themes</th><th>Risk</th></tr></thead>
    <tbody>
      <tr>
        <td><strong>Petrobras</strong></td>
        <td>Brazil</td>
        <td>Energy (Oil & Gas)</td>
        <td><span class="tag pub">Public Sector</span></td>
        <td>Data Residency, AWS, Agentic Platform</td>
        <td style="color:var(--red)"><strong>High</strong></td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## Account Card

```html
<div id="account-id" class="acct high"> <!-- high/med/low for border color -->
  <h3>Account Name</h3>
  <div class="ainfo">
    <span>Country</span><span class="sep">|</span>
    <span>Industry - Sub-vertical</span><span class="sep">|</span>
    <span class="tag pub">Public Sector</span>  <!-- or tag ent for Enterprise -->
    <span class="tag dr">Data Residency</span>
    <span class="tag aws">AWS</span>
    <span class="tag ag">Agentic Platform</span>
  </div>
  <!-- Optional description paragraph for accounts that need context -->
  <p class="desc"><strong>Full name</strong> description of what the company is...</p>
  <ul>
    <li>Full detail bullet point - do NOT summarize</li>
    <li>Another full detail point with <strong>bold</strong> for key terms</li>
  </ul>
</div>
```

---

## Additional Accounts Grid

```html
<div class="addl">
  <div class="addl-item">
    <strong>Account Name</strong>
    <span>Country | Industry | Segment</span>
  </div>
</div>
```

---

## Insight Callouts

```html
<!-- Critical (red) -->
<div class="ins crit">
  <strong>Bold headline.</strong> Supporting text...
</div>

<!-- Warning (yellow) -->
<div class="ins warn">
  <strong>Bold headline.</strong> Supporting text...
</div>

<!-- Info (blue) -->
<div class="ins info">
  <strong>Bold headline.</strong> Supporting text...
</div>

<!-- Success (green) -->
<div class="ins ok">
  <strong>Bold headline.</strong> Supporting text...
</div>
```

---

## KPI Row

```html
<div class="kpi">
  <div class="k"><div class="l">Label</div><div class="v">400</div><div class="s">Subtitle</div></div>
  <div class="k p"><div class="l">Label</div><div class="v">203</div><div class="s">Subtitle</div></div>
  <div class="k r"><div class="l">Label</div><div class="v">~0%</div><div class="s">Subtitle</div></div>
  <div class="k y"><div class="l">Label</div><div class="v">79.2%</div><div class="s">Subtitle</div></div>
  <div class="k g"><div class="l">Label</div><div class="v">Dev 67%</div><div class="s">Subtitle</div></div>
</div>
```

Color variants: default (blue), `.r` (red), `.y` (yellow), `.g` (green), `.p` (purple)

---

## Audience Panel

```html
<div class="ap"> <!-- add .sp for purple variant -->
  <h3>Workshop Name</h3>
  <div class="meta">Date &nbsp;|&nbsp; Description</div>
  <div class="sr">
    <div class="st"><div class="n">150</div><div class="lb">Attendees</div></div>
    <div class="st"><div class="n" style="color:var(--blue)">61</div><div class="lb">Responded</div></div>
    <div class="st"><div class="n">40.7%</div><div class="lb">Response Rate</div></div>
  </div>
  <div class="rb"><div class="f" style="width:40.7%;background:var(--blue)"></div></div>
  <div class="rl"><span>0</span><span>61 of 150</span><span>150</span></div>
  <div style="height:180px;margin:14px 0"><canvas id="chartId"></canvas></div>
  <div class="fc r"><strong>Finding headline</strong>Details...</div>
</div>
```

---

## Chart.js Configs

### Doughnut (Role Distribution)

```javascript
new Chart(document.getElementById('crRole'), {
  type: 'doughnut',
  data: {
    labels: ['Developers 57%', 'Tech Leads 26%', 'DevOps/SRE 12%', 'Managers 5%'],
    datasets: [{
      data: [33, 15, 7, 3],
      backgroundColor: [B, G, Y, R],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    cutout: '55%',
    plugins: { legend: { position: 'bottom', labels: { padding: 8, usePointStyle: true, font: { size: 10 } } } }
  }
});
```

### Stacked Horizontal Bar (GitHub Copilot Experience)

```javascript
new Chart(document.getElementById('copilotAll'), {
  type: 'bar',
  data: {
    labels: ['Workshop 1', 'Workshop 2', 'Combined'],
    datasets: [
      { label: 'Never Used', data: [2, 33, 35], backgroundColor: R },
      { label: 'Autocomplete', data: [15, 17, 32], backgroundColor: Y },
      { label: 'Chat/Ask', data: [26, 31, 57], backgroundColor: B },
      { label: 'Agent Mode', data: [15, 38, 53], backgroundColor: P + '99', borderWidth: 2, borderColor: P }
    ]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { stacked: true, beginAtZero: true },
      y: { stacked: true, grid: { display: false } }
    },
    plugins: { legend: { position: 'bottom', labels: { usePointStyle: true, padding: 10, font: { size: 10 } } } }
  }
});
```

### Horizontal Bar (Agent Knowledge)

```javascript
new Chart(document.getElementById('agentKnow'), {
  type: 'bar',
  data: {
    labels: ['Level 1', 'Level 2', 'Level 3', 'Level 4'],
    datasets: [{
      data: [42, 38, 20, 1],
      backgroundColor: [R, Y, B, G],
      borderRadius: 5,
      barThickness: 24
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    scales: { x: { beginAtZero: true }, y: { grid: { display: false } } },
    plugins: { legend: { display: false } }
  }
});
```

---

## Data Table

```html
<table class="dt">
  <thead><tr><th>Column 1</th><th>Column 2</th><th>Column 3</th></tr></thead>
  <tbody>
    <tr><td>Data</td><td><strong>Bold data</strong></td><td style="color:var(--red)"><strong>~0%</strong></td></tr>
  </tbody>
</table>
```

---

## Competitive Landscape

```html
<table class="dt">
  <thead><tr><th>Threat</th><th>Accounts Affected</th><th>Impact</th></tr></thead>
  <tbody>
    <tr><td><span class="tag aws">AWS</span></td><td>Account 1, Account 2</td><td>Description of impact</td></tr>
    <tr><td><span class="tag gl">GitLab</span></td><td>Account 3</td><td>Description</td></tr>
    <tr><td><span class="tag dr">Data Residency</span></td><td>Account 1, Account 4</td><td>Description</td></tr>
  </tbody>
</table>
```

---

## Section Dividers

```html
<hr class="divider"><div class="divider-label">Section Label Text</div>
```

---

## Footer

```html
<div class="footer">Monthly Insights - Q3 FY26 - Frontier Cockpit Team, Software Global Black Belt &nbsp;|&nbsp; March 2026</div>
```

---

## Chart.js Setup

Use this only when the user explicitly asks for an interactive dashboard with external JavaScript dependencies. For standard reports, prefer self-contained inline SVG charts.

Include at the top of `<head>` only for the interactive variant:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
```

Color constants for JavaScript:

```javascript
const B='#0078D4', G='#107C10', R='#D83B01', Y='#FFB900', P='#8957E5', D='#24292F';
Chart.defaults.font.family = "'Segoe UI',system-ui,sans-serif";
Chart.defaults.font.size = 11;
```
