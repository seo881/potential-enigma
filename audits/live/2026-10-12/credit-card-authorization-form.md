# /ai-form-builder/credit-card-authorization-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-credit-card-authorization-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-credit-card-authorization-form-B-HUBRULES5FAQ-1 (P1, B-HUBRULES5FAQ, fix-by-writer, fixed)
- field: faq#7
- caught by: B-HUBRULES5FAQ (Layer B): The question asks how long to keep the form; the answer gives no period ('hold on to it after the final charge'). A period tied to card-network dispute windows needs a domain source first, so the wording is Divit's call.
- live text: Keep each signed cc authorization form for as long as you charge the card, and hold on to it after the final charge.
- faq before: window.awbFAQ = {"heading": "Card Authorization Questions, Answered", "items": [{"q": "What is a credit card authorization form?", "a": "A credit card authorization form is a signed permission that lets a business charge a customer's card, once or on a schedule. It names the card and the amount or terms, and the cardholder signs it. The business keeps it as proof the charge was approved."}, {"q": "How do I create a credit card authorization form online?", "a": "Describe the charge to Emergent's 
- faq after: window.awbFAQ = {"heading": "Card Authorization Questions, Answered", "items": [{"q": "What is a credit card authorization form?", "a": "A credit card authorization form is a signed permission that lets a business charge a customer's card, once or on a schedule. It names the card and the amount or terms, and the cardholder signs it. The business keeps it as proof the charge was approved."}, {"q": "How do I create a credit card authorization form online?", "a": "Describe the charge to Emergent's 

## 20261012-credit-card-authorization-form-B-HUBRULES8-1 (P2, B-HUBRULES8, backlog)
- field: faq#5
- caught by: B-HUBRULES8 (Layer B): US-only facts stated without a jurisdiction: ACH (faq#5) and the written-permission rule for employer credit checks, which is the US FCRA (faq#9). Both are sourced.
- live text: Bank debits run on the ACH network, where each debit must be authorized by the account holder.

## 20261012-credit-card-authorization-form-B-CONTENTDEFEC-1 (P2, B-CONTENTDEFEC, backlog)
- field: why_description
- caught by: B-CONTENTDEFEC (Layer B): Generalization about every PDF template (earlier review note); not every template asks for the security code.
- live text: A PDF template puts the full card number and security code in an email.

## 20261012-credit-card-authorization-form-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: feature_1
- caught by: B-HUBRULES2a (Layer B): Run-on list of five items in one sentence with Emergent, not the form, as the one asking, and a stray comma before 'and the signing date'.
- live text: Emergent asks for the cardholder's name and billing address, the card brand and expiration date, what the charge covers and the amount, then a signature, and

## 20261012-credit-card-authorization-form-B-HUBRULES2a-2 (P2, B-HUBRULES2a, backlog)
- field: faq#6
- caught by: B-HUBRULES2a (Layer B): 'Usually' twice in the first two sentences.
- live text: Usually not. A credit card form usually charges the card the moment the customer submits it

## 20261012-credit-card-authorization-form-B-HUBRULES1Num-1 (P2, B-HUBRULES1Num, backlog)
- field: tab_content_1
- caught by: B-HUBRULES1Num (Layer B): Duration spelled out (also in tab_image_1 alt).
- live text: room and tax for two nights, capped at $640.

## 20261012-credit-card-authorization-form-B-layout390px-1 (P2, B-layout390px, backlog)
- field: template
- caught by: B-layout390px (Layer B): UNVERIFIED: in the 390 px capture no use-case tab pill shows the active state (desktop shows Hotel Stays active; other pages' mobile captures do). Probably capture timing; check on a phone.
- live text: Hotel Stays | Monthly Retainers | No-Show Fees | Phone Orders
