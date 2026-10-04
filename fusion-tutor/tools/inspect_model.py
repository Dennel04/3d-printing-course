# Read-only осмотр активной модели Fusion для учителя.
# Запускать через fusion_mcp_execute: featureType "script", readOnly: true.
import adsk.core, adsk.fusion


def run(_context: str):
    app = adsk.core.Application.get()
    doc = app.activeDocument
    if not doc:
        print("В Fusion не открыт ни один документ.")
        return
    design = adsk.fusion.Design.cast(app.activeProduct)
    print(f"Документ: {doc.name}  (изменён: {doc.isModified})")
    if not design:
        print("Активный продукт — не Design (открыт не 3D-дизайн).")
        return
    um = design.unitsManager
    print(f"Единицы: {um.defaultLengthUnits}  |  режим: "
          f"{'parametric' if design.designType == adsk.fusion.DesignTypes.ParametricDesignType else 'direct'}")

    print("\n== User Parameters ==")
    if design.userParameters.count == 0:
        print("(нет — все размеры захардкожены)")
    for p in design.userParameters:
        print(f"  {p.name} = {p.expression}  {('— ' + p.comment) if p.comment else ''}")

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
    print(f"  marker на позиции {tl.markerPosition} из {tl.count}")

    print("\n== Компоненты, эскизы, тела ==")
    for c in design.allComponents:
        print(f"- {c.name}: тел {c.bRepBodies.count}, эскизов {c.sketches.count}")
        for s in c.sketches:
            state = "полностью определён" if s.isFullyConstrained else "НЕ определён"
            print(f"    эскиз '{s.name}': {state}, размеров {s.sketchDimensions.count}, "
                  f"ограничений {s.geometricConstraints.count}, профилей {s.profiles.count}")
        for b in c.bRepBodies:
            print(f"    тело '{b.name}': solid={b.isSolid}, объём {b.volume:.3f} cm³")
