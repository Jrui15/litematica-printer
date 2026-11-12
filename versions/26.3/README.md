# Minecraft 26.3

Build with JDK 25: `./gradlew :26.3:build --configure-on-demand`.
The JAR is written to `versions/26.3/build/libs/`.

Install Fabric Loader 0.19.3 or newer, Fabric API for 26.3, Litematica
0.29.1 or newer for 26.3, and MaLiLib 0.30.2 or newer for 26.3.

This target maintains its own sources, based on the 26.2 port. Changes
include tag-based hoe/shovel selection, renamed redstone wire APIs,
explicit swing animations, and the new sign text and update packet APIs.

Before release, test a schematic in a disposable world, including oriented
blocks, inventory switching, digging, hoe/shovel use, redstone, and signs.

## Mixin compatibility validation

Validated against the pinned Litematica 0.29.1 (ZqV316KY), MaLiLib 0.30.2
(JX9bESec), Fabric Loader 0.19.3, and Minecraft 26.3 with Java 25.

- The renderer injection uses the complete `renderBlocksAndOverlay` descriptor.
  Its arguments include `ChunkRenderDispatcherBuffers` after mesh data and before
  block output, with `CallbackInfo` last. No local variables are captured.
  The cancellable HEAD callback retains the existing held-item render filter.
- The passenger rotation redirect targets `LocalPlayer.sendChanges()V`, send
  ordinal 1 (the rotation packet after the input packet). The four sendPosition
  redirects retain their position/rotation/status packet order.
- `:26.3:build` passed. A temporary Fabric preLaunch audit loaded all 14 active
  printer mixin target classes through the runtime classloader with initialization
  disabled and injection counting enabled. All transformed successfully, including
  renderer, verifier, configuration, hotkeys, Easy Place, and packet targets.
  The optional EssentialClient integration was not tested (dependency absent).
- A normal client launch reached graphics initialization, then failed with
  `Unable to initialize SDL: No available video device` in the headless environment.
  This is not a successful title-screen or gameplay test. The gameplay checklist
  above remains necessary. The temporary audit mod is not included in the build.

## Printer activation

Enable Litematica's `easyPlaceMode`, disable `printerOff`, and hold the
Easy Place activation key. For continuous placement enable `easyPlaceHoldEnabled`.
Load and enable a schematic placement, stay within reach, and use a tool mode
other than Rebuild. Both values of `easyPlacePostRewrite` are supported.

Litematica routes legacy Easy Place through `WorldUtils.doEasyPlaceAction` and
rewritten Easy Place through `EasyPlaceUtils.handleEasyPlace`. The printer
intercepts both at HEAD using the same cancellable callback. This preserves
the printer-off fallback, fake-rotation-only mode, and existing placement logic.
Previously only the rewritten path was intercepted, leaving the printer inactive
when the legacy path was selected.

Validation: Java 25 `:26.3:build`; runtime transformation of both Easy Place
classes; `python versions/26.3/tests/check_activation_mixins.py` against the
exported runtime bytecode. The check verifies both paths invoke the printer
callback and honor cancellation. These checks do not establish successful
in-world placement; graphical startup is blocked here by SDL's missing video
device.
