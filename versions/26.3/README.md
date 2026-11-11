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
