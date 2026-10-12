# /ai-form-builder/employee-information-form: live audit 2026-10-12

Base: https://emergent.sh

## 20261012-employee-information-form-A5-empty-p-1 (P2, A5-empty-p, backlog)
- field: template
- caught by: A5-empty-p (Layer A): empty paragraph (Webflow rich-text zero-width placeholder) in visible text

## 20261012-employee-information-form-B-QCA1stocknam-1 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_content_1
- caught by: B-QCA1stocknam (Layer B): Stock placeholder company name 'Northwind' (QC A1 now blocks it).
- live text: Northwind Freight sends each of its 140 employees their own record, every field filled in from last year.
- cover_image before: Employee information form: a direct message tells payroll lead Grace Holt that Lena Park has shown HR her updated Social Security card, with buttons to update payroll to Lena Ortiz or view her record.
- cover_image after: Employee information form: a direct message tells payroll lead Grace Hensley that Mira Hurst has shown HR her updated Social Security card, with buttons to update payroll to Mira Garvey or view her record.
- share_image before: Build an employee information form that keeps every staff record current, with Emergent
- share_image after: Build an employee information form that keeps every staff record current, with Emergent
- tab_content_1 before: Every record sent, 112 back in ten days January is when the records get checked. Northwind Freight sends each of its 140 employees their own record, every field filled in from last year. Most people confirm without changing a thing, and a driver who moved in the spring fixes his address. After ten days 112 have replied, and the other 28 get an email reminder.
- tab_content_1 after: Every record sent, 112 back in ten days January is when the records get checked. Hartigan Freight sends each of its 140 employees their own record, every field filled in from last year. Most people confirm without changing a thing, and a driver who moved in the spring fixes his address. After ten days 112 have replied, and the other 28 get an email reminder.
- tab_content_2 before: The new surname waits on a Social Security card Marriage changes a surname, and payroll has to time the switch. Lena Park, a supervisor at Northwind Freight, submits her new last name, Ortiz. Her Social Security card does not show it yet, and payroll keeps Park on file until it does. Once she shows HR the new card, payroll gets a direct message to change the name.
- tab_content_2 after: The new surname waits on a Social Security card Marriage changes a surname, and payroll has to time the switch. Mira Hurst, a supervisor at Hartigan Freight, submits her new last name, Garvey. Her Social Security card does not show it yet, and payroll keeps Hurst on file until it does. Once she shows HR the new card, payroll gets a direct message to change the name.
- tab_image_1 before: A January record check at Northwind Freight: all 140 employees got their pre-filled record, 112 have confirmed after ten days, and the 28 who have not replied get an email reminder.
- tab_image_1 after: A January record check at Hartigan Freight: all 140 employees got their pre-filled record, 112 have confirmed after ten days, and the 28 who have not replied get an email reminder.
- tab_image_2 before: Lena Park submits her new last name, Ortiz, but her Social Security card does not show it yet, so payroll keeps Park on file until she shows HR the updated card.
- tab_image_2 after: Mira Hurst submits her new last name, Garvey, but her Social Security card does not show it yet, so payroll keeps Hurst on file until she shows HR the updated card.
- tab_image_3 before: Bayside Dental imports 86 staff records; 17 lack a home address or personal phone, each person gets a link for only the missing field, 11 are filled by Friday and 6 are still open.
- tab_image_3 after: Bayside Dental imports 86 staff records; 17 lack a home address or personal phone, each person gets a link for only the missing field, 11 are filled by Friday and 6 are still open.
- tab_image_4 before: A Juniper Home Goods store manager sees a directory with a work phone beside every name, while home addresses and birth dates stay in the HR view; a request for an address is logged for HR.
- tab_image_4 after: A Juniper Home Goods store manager sees a directory with a work phone beside every name, while home addresses and birth dates stay in the HR view; a request for an address is logged for HR.

## 20261012-employee-information-form-B-QCA1stocknam-2 (P1, B-QCA1stocknam, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1stocknam (Layer B): Stock placeholder company name 'Northwind' in the second tab.
- live text: Lena Park, a supervisor at Northwind Freight, submits her new last name, Ortiz.

## 20261012-employee-information-form-B-QCA1stocknam-3 (P1, B-QCA1stocknam, proposed)
- field: images.tab_image_1.alt
- caught by: B-QCA1stocknam (Layer B): Stock placeholder company name in the tab 1 image alt (same string in image_brief.tabs[0].alt).
- live text: A January record check at Northwind Freight: all 140 employees got their pre-filled record, 112 have confirmed after ten days

## 20261012-employee-information-form-B-QCA1reusedpe-1 (P1, B-QCA1reusedpe, fix-by-writer, fixed)
- field: tab_content_2
- caught by: B-QCA1reusedpe (Layer B): Reused persona names: 'Lena Park' appears in 6 other specs and 'Lena Ortiz' in 13; also in the tab 2 alt, the image brief and the cover (with payroll lead Grace Holt, also on employee-referral-form).
- live text: Lena Park, a supervisor at Northwind Freight, submits her new last name, Ortiz.

## 20261012-employee-information-form-B-QCA1reusedpe-2 (P1, B-QCA1reusedpe, proposed)
- field: image_brief tab 3
- caught by: B-QCA1reusedpe (Layer B): The drawn table reuses persona names from other pages: Ana Ruiz (25 other specs), Priya Nair (22), Tom Becker (13), Mei Chen (2).
- live text: Ana Ruiz | Home address ... Tom Becker | Personal phone ... Priya Nair ... Mei Chen

## 20261012-employee-information-form-B-QCA1reusedpe-3 (P1, B-QCA1reusedpe, proposed)
- field: image_brief tab 4
- caught by: B-QCA1reusedpe (Layer B): The drawn directory reuses persona names: Rosa Diaz (6 other specs), Ben Okafor (2), Luis Romero (1).
- live text: Rosa Diaz | Sales lead | Ext. 214; Ben Okafor | Cashier; Luis Romero | Cashier

## 20261012-employee-information-form-B-HUBRULES8fie-1 (P2, B-HUBRULES8fie, backlog)
- field: tab_content_1
- caught by: B-HUBRULES8fie (Layer B): The example runs the yearly check in January, while step 6 says to pick a quiet month away from year-end payroll (W-2 season).
- live text: January is when the records get checked.

## 20261012-employee-information-form-B-HUBRULES2a-1 (P2, B-HUBRULES2a, backlog)
- field: faq item 10
- caught by: B-HUBRULES2a (Layer B): Advice to keep emergency contact forms at a front desk conflicts with FAQ 8's need-to-know access advice.
- live text: Supervisors who need emergency contacts on site can keep a separate emergency contact form at the front desk.
