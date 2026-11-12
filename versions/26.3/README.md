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

## Config screen integration

Printer settings appear in Generic and All; printer keybinds appear in Hotkeys
and All. Both `getConfigs()` and `getAllConfigs()` must redirect the generic
options and hotkey lists. Litematica's All tab constructs its own list, so
hooking only `getConfigs()` leaves printer entries out of All-tab searches.

After a client launch with Mixin export enabled, run
`python versions/26.3/tests/check_config_mixins.py` with Java 25 on PATH or
JAVA_HOME. This checks the actual transformed GUI bytecode for both redirects
in both methods, exactly once each. This regression check and the 14-target
runtime transformation audit passed against the pinned dependencies. Visual
verification remains blocked here by SDL reporting no available video device.
