# Conversion Guide

## General

This pipeline uses Blender's builtin glTF exporter.
Please refer to [the documentation for that exporter](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html) as a starting point.
This document will note cases where this pipeline makes additions or modifications to this exporter.

## Materials

Only the Principled BSDF node (or no node with Blender 2.91+) is currently supported.
Also, by default PBR materials (and associated textures) are created for the Blender materials.
While attempts are made to keep these materials roughly compatible with Panda's auto shader, using [simplepbr](https://github.com/Moguri/panda3d-simplepbr/) is recommend for maximum compatibility.

If `legacy` materials are requested (via the `--material-mode` CLI switch), then this pipeline makes a "best effort" of converting PBR materials to legacy materials.
However, this conversion is lossy.
Currently only diffuse color and normal maps are supported for legacy materials.

Note that bi-tangents are not generated for models converted via blend2bam and that tangents are 4 component instead of 3.
This makes normal mapping currently incompatible with Panda's auto shader, but simplepbr can support these tangents (and computes bi-tangents).
See [here](https://github.com/Moguri/panda3d-gltf/issues/69) for more information.

> :warning: Blender materials are double-sided by default.
> It is recommended to disable this on materials for performance and to reduce artifacts (e.g., from shadows)

## Animations

Object animations are not supported by Panda3D.
Therefore, only armature animations will get converted.

By default, the glTF exporter will only export actions added to the NLA editor.
As a convenience, blend2bam will automatically add actions to the NLA editor if it is empty.
In other words, blend2bam will export all actions by default if the NLA editor is empty.
To have more control over which actions are exported, add the actions to export to the NLA editor.

The default for animations is to embed them into the same BAM file as the model.
If separate animation files are desired, `--animations embed` can be be used on the CLI.

## Collision Shapes

The glTF exporter does not support exporting collision shape information.
However, blend2bam will convert Blender rigid body shapes and add them to the glTF data outputted from the exporter.
By default this information gets turned into Panda3D CollisionSolid objects.
To use Bullet shapes instead, use `--physics-engine bullet` on the CLI.

Any rigid bodies marked as Passive will become intangible (a ghost object in Bullet).

> :warning: BulletGhostObjects are not currently supported since they do not serialize to BAM.
> This issue has [been reported upstream](https://github.com/panda3d/panda3d/issues/1099).

## Python Tags

Blender custom properties on objects get converted to tags.
