const fs=require('fs');const {URL}=require('url');global.URL=URL;
const code=fs.readFileSync(process.argv[2]||'page-schema.html','utf8').replace(/^[\s\S]*?<script>/,'').replace(/<\/script>[\s\S]*$/,'');
function el(t,href){return {textContent:t,getAttribute:k=>k==='href'?(href||null):null};}
function page(path,title,desc,crumbs,faq){
  const head=[];global.location={pathname:path};
  const bc={children:crumbs};
  global.document={readyState:'complete',title,getElementById:id=>head.find(e=>e.id===id)||null,
    querySelector:s=>s==='.build_breadcrumbs'?bc:s.startsWith('meta')?{getAttribute:()=>desc}:null,
    createElement:()=>({}),head:{appendChild:e=>head.push(e)},addEventListener:()=>{}};
  global.window={awbFAQ:faq}; eval(code); eval(code);
  if(head.length!==1) throw 'dup'; return JSON.parse(head[0].text);}
// Case 1: SQB child page exactly as Webflow renders it (published href for page links is a relative path)
const j=page('/ai-survey-and-quiz-builder/customer-satisfaction','Customer Satisfaction Survey Template & CSAT | Emergent',
 'Build a customer satisfaction survey with CSAT, NPS, and CES questions. Tie every response to the customer and alert on low scores. Free to start.',
 [el('Home','https://emergent.sh/'),el('/'),el('AI Survey and Quiz Builder','/ai-survey-and-quiz-builder'),el('/'),el('Customer Satisfaction Survey')],
 {items:[{q:'What is a CSAT survey?',a:'A CSAT survey asks customers to rate...'},{q:'How do I create one for free?',a:'Emergent\'s <a href="https://emergent.sh/ai-survey-and-quiz-builder">AI survey builder</a> generates it.'}]});
const bl=j['@graph'].find(n=>n['@type']==='BreadcrumbList').itemListElement;
console.log(bl.map(i=>i.position+'. '+i.name+' -> '+i.item).join('\n'));
const wp=j['@graph'].find(n=>n['@type']==='WebPage'); console.log('WebPage name:',wp.name);
if(bl.length!==3||bl[1].item!=='https://emergent.sh/ai-survey-and-quiz-builder'||bl[2].item!=='https://emergent.sh/ai-survey-and-quiz-builder/customer-satisfaction') throw 'crumbs';
if(!wp.name.includes('&')||wp.name.includes('&amp;')) throw 'amp';
// every @id reference resolves
const ids=new Set(j['@graph'].map(n=>n['@id']));const refs=[...JSON.stringify(j).matchAll(/"@id":"([^"]+)"/g)].map(m=>m[1]);
const bad=refs.filter(r=>!ids.has(r)); if(bad.length) throw 'dangling '+bad;
// Case 2: staging host + trailing slash + no FAQ -> still production ids, no FAQPage node
const j2=page('/ai-form-builder/creator-application/','T','D',[el('Home','https://emergent.sh/'),el('/'),el('AI Form Builder','/ai-form-builder'),el('/'),el('Creator Application')],undefined);
if(j2['@graph'].some(n=>n['@type']==='FAQPage')) throw 'faq';
if(j2['@graph'][2].url!=='https://emergent.sh/ai-form-builder/creator-application') throw 'url';
console.log('Types:',j['@graph'].map(n=>n['@type']).join(', '));
console.log('ALL SCHEMA SCRIPT TESTS PASS');
