# Webflow IX3 layer (build-hub child templates only)
Scope: pages = AAB, SQB, LP, Form collection templates. Never site-wide (the use-case component is shared with live CRM pages).
- i-54e50d55  Use-case image reveal: scroll, trigger .section_usecase at "top 85%", image rises 64px, scales 96%→100% and fades in, 1.0s expo.out. Reduced motion: off. Phones: skip to end.
- i-af43ffd6  Use-case image 3D tilt: mouse-move over .build-usecase_image, rotationY -3..3 and rotationX 2.5..-2.5 at 1400px perspective, smoothness 0.8. Reduced motion, tablet, phone: off.
- Tab cross-fade: native Webflow Tabs fade (not IX3), so images are never hidden at rest.
Rollback: delete the two interaction ids above.
