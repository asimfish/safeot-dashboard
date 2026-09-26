# Process notes — NIPSStyle R5

Round 1: inspected R4 at 5.5-inch print width and identified the overlap source: a detached kernel equation, old iteration labels, and a repeated PPO label occupying the projection/feedback lanes.

Round 2: removed those stale solver internals; reduced column 3 to the two constraints used by the method; separated column 4 into projection, flow labels, and safety-price output; and placed the three actor-side equations in independent cards.

Round 3: rendered through LibreOffice, checked the 300-dpi print PNG, grayscale/CVD previews, card intersection QA, and anonymous PDF metadata. No manuscript or experimental data were changed.
