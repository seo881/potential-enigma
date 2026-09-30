const code=require('fs').readFileSync('faq-customcode.html','utf8').replace(/^[\s\S]*?<script>/,'').replace(/<\/script>[\s\S]*$/,'');
const head=[];global.document={readyState:'complete',getElementById:id=>head.find(e=>e.id===id)||null,createElement:()=>({}),head:{appendChild:e=>head.push(e)},addEventListener:()=>{}};
global.window={awbFAQ:{items:[{q:'What is a thank you page?',a:'A page.'},{q:'Link?',a:'See [x](https://emergent.sh/y) and <a href="https://emergent.sh/z">z</a>.'},{q:'',a:'skip'}]}};
eval(code);eval(code);const j=JSON.parse(head[0].text);
if(head.length!==1||j.mainEntity.length!==2||!j.mainEntity[1].acceptedAnswer.text.includes('<a href="https://emergent.sh/y">x</a>')) throw 'fail';
console.log('FAQ custom-code script tests PASS');
