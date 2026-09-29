# Webflow IX3 layer (build-hub child templates only)
Scope: pages = AAB, SQB, LP, Form collection templates. Never site-wide (the use-case component is shared with live CRM pages).
- i-54e50d55  Use-case image reveal: scroll, trigger .section_usecase at "top 85%", image rises 64px, scales 96%→100% and fades in, 1.0s expo.out. Reduced motion: off. Phones: skip to end.
- i-af43ffd6  Use-case image 3D tilt: mouse-move over .build-usecase_image, rotationY -3..3 and rotationX 2.5..-2.5 at 1400px perspective, smoothness 0.8. Reduced motion, tablet, phone: off.
- Tab cross-fade: native Webflow Tabs fade (not IX3), so images are never hidden at rest.
Rollback: delete the two interaction ids above.

## Added (all scoped to the 8 build-hub pages: 4 hubs + 4 child templates; reduced motion = off)
- i-680a5d1a  Hero entrance (load): H1 (.heading-style-h1.is-product) rises word by word, 45ms stagger; prompt box (.build_input-block) settles in at +0.45s.
- i-dcb777ac  How-to steps (scroll scrub 0.6, "top 85%" to "top 50%"): each .sticky_list_wrapper goes from 35% to 100% opacity and 24px to 0. Phones: skip to end.
- i-4fd60c05  Carousel card hover: hovered card lifts 4px, its .build_cover zooms to 103%, its .build-arrow_wrapper nudges 4px (targets within the hovered card).
- i-a9d6f7ac  Integration chip hover: .integration_chip lifts 2px, border deepens.
Rollback for any of them: delete the interaction id (one call each). Nothing else on the site references these ids.
