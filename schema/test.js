const fs=require('fs');
const html=fs.readFileSync('faq-schema.html','utf8');
const code=html.replace(/^[\s\S]*?<script>/,'').replace(/<\/script>[\s\S]*$/,'');
const head=[]; global.location={pathname:'/ai-automation-builder/approval-workflow/'};
global.document={readyState:'complete',getElementById:id=>head.find(e=>e.id===id)||null,
  createElement:()=>({}),head:{appendChild:e=>head.push(e)},addEventListener:()=>{}};
global.window={awbFAQ:{"heading":"Got Questions? We've Got Answers","items":[
 {"q":"How do I create an approval workflow?","a":"Describe the trigger, the approvers, the routing rules, and where the record should land. Emergent's <a href=\"https://emergent.sh/ai-automation-builder\">AI automation builder</a> generates the request form, the routing, the alerts, and the audit database, and you refine it by prompting."},
 {"q":"Markdown case","a":"See [the builder](https://emergent.sh/x) now."},
 {"q":"","a":"skipped"},{"q":"Quote \"test\" & ampersand","a":"It's <b>fine</b> — em dash"}]}};
eval(code); eval(code); // run twice: must not duplicate
if(head.length!==1) throw 'duplicate/none: '+head.length;
const j=JSON.parse(head[0].text);
console.log(JSON.stringify(j,null,1).slice(0,900));
if(j['@id']!=='https://emergent.sh/ai-automation-builder/approval-workflow#faqpage') throw 'bad id';
if(j.mainEntity.length!==3) throw 'filter failed';
if(!j.mainEntity[1].acceptedAnswer.text.includes('<a href="https://emergent.sh/x">the builder</a>')) throw 'md';
console.log('\nFAQ SCRIPT TESTS PASS');
