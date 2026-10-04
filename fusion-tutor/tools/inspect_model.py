# Read-only inspection of the active Fusion model for the tutor.
# Run via fusion_mcp_execute: featureType "script", readOnly: true.
import adsk.core, adsk.fusion


def run(_context: str):
    app = adsk.core.Application.get()
    doc = app.activeDocument
    if not doc:
        print("No document is open in Fusion.")
        return
    design = adsk.fusion.Design.cast(app.activeProduct)
    print(f"Document: {doc.name}  (modified: {doc.isModified})")
    if not design:
        print("The active product is not a Design (not a 3D design).")
        return
    um = design.unitsManager
    print(f"Units: {um.defaultLengthUnits}  |  mode: "
          f"{'parametric' if design.designType == adsk.fusion.DesignTypes.ParametricDesignType else 'direct'}")

    print("\n== User Parameters ==")
    if design.userParameters.count == 0:
        print("(none: every dimension is hard-coded)")
    for p in design.userParameters:
        print(f"  {p.name} = {p.expression}  {('- ' + p.comment) if p.comment else ''}")

    print("\n== Timeline ==")
    tl = design.timeline
    bad = adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState
    for i in range(tl.count):
        it = tl.item(i)
        ent = it.entity
        kind = ent.objectType.split("::")[-1] if ent else "Group/?"
        flag = "" if it.healthState == bad else f"  !! {it.errorOrWarningMessage}"
        sup = " (suppressed)" if it.isSuppressed else ""
        print(f"  {i:>3}. {it.name:<28} {kind}{sup}{flag}")
    print(f"  marker at position {tl.markerPosition} of {tl.count}")

    print("\n== Components, sketches, bodies ==")
    for c in design.allComponents:
        print(f"- {c.name}: bodies {c.bRepBodies.count}, sketches {c.sketches.count}")
        for s in c.sketches:
            state = "fully constrained" if s.isFullyConstrained else "NOT constrained"
            print(f"    sketch '{s.name}': {state}, dimensions {s.sketchDimensions.count}, "
                  f"constraints {s.geometricConstraints.count}, profiles {s.profiles.count}")
        for b in c.bRepBodies:
            print(f"    body '{b.name}': solid={b.isSolid}, volume {b.volume:.3f} cm³")
