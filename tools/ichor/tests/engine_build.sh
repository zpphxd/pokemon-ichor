# Shared build steps for the Ichor engine-system checks (source it; don't run it).
#
#   . tools/ichor/tests/engine_build.sh
#   engine_prepare SAVE build/test_ichor_save tools/ichor/tests/ichor_save_consts.c tools/ichor/tests/ichor_save_setup.s
#   engine_run SAVE build/test_ichor_save tools/ichor/tests/ichor_save.lua 200000 900
#
# engine_prepare writes, into OUT:
#   symbols.lua         the slice library's table (slice_symbols.sh)
#   engine_symbols.lua  CONSTS's k_NAME constants plus the engine symbols below
#   setup.bin, .syms    ASM, the test-only event scripts, assembled with the
#                       game's macros and linked at BLOB_ADDR in spare EWRAM
#                       against the ELF's symbols. Never part of the ROM.
# engine_run runs LUA in the Lua headless runner and fails on a FAIL line, a
# crash-like error, or a run that never prints "<TAG> done".
#
# Call from the repo root, with ROM set (default pokeemerald.gba).

ROM="${ROM:-pokeemerald.gba}"
ELF="${ROM%.gba}.elf"
BLOB_ADDR=0x0203F000
export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:/opt/homebrew/bin:$PATH"
TIMEOUT=$(command -v gtimeout || command -v timeout)
RUNNER=build/tools/ichor-mgba-headless

# Engine addresses every check may need, besides slice_symbols.sh's.
ENGINE_SYMS="gSaveBlock3Ptr gSpecialVar_0x8000 gSpecialVar_0x8001 gSpecialVar_0x8002 gSpecialVar_0x8003
gSpecialVar_0x8005 gSpecialVar_0x8006 gSpecialVar_0x8007 gSpecialVar_0x800A gSpecialVar_0x800B gLocalTime
gStringVar1 gStringVar2 gStringVar3 gPlayerPartyCount gFieldEffectArguments gSaveBlock1Ptr
gWeather CB2_FlyMap CB2_Bag Task_ShowStartMenu sFlyMap gSprites SpriteCB_FlyDestIcon sCarriedFlame
gPlttBufferUnfaded gPlttBufferFaded"

engine_prepare() {
  local tag="$1" out="$2" consts="$3" asm="$4"
  [ -f "$ROM" ] && [ -f "$ELF" ] || { echo "$tag FAIL: $ROM or $ELF missing (run make first)"; exit 1; }
  mkdir -p "$out/shots" && rm -f "$out"/shots/*.png "$out"/*.png
  if [ ! -x "$RUNNER" ] || [ tools/ichor/mgba_headless.c -nt "$RUNNER" ]; then
    local prefix
    prefix=$(brew --prefix mgba) || { echo "$tag FAIL: needs Homebrew mgba"; exit 1; }
    mkdir -p build/tools
    cc -O2 -I"$prefix/include" tools/ichor/mgba_headless.c -L"$prefix/lib" -lmgba -o "$RUNNER" || exit 1
  fi
  tools/ichor/tests/slice_symbols.sh "$ELF" "$out/symbols.lua" >/dev/null \
    || { echo "$tag FAIL: slice_symbols.sh"; exit 1; }

  arm-none-eabi-gcc -S -O0 -mthumb -mabi=apcs-gnu -march=armv4t -iquote include -Wno-trigraphs \
    -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -o "$out/consts.s" "$consts" \
    || { echo "$tag FAIL: could not compile $consts"; exit 1; }
  local pattern="^($(echo $ENGINE_SYMS | tr ' ' '|'))$"
  {
    echo "return {"
    # A zero constant is emitted as .space rather than .word.
    awk '/^k_[A-Za-z0-9_]+:/ { n = substr($1, 3, length($1) - 3); next }
         n && /\.word/  { print "  " n " = " $2 ","; n = "" }
         n && /\.short/ { print "  " n " = " $2 ","; n = "" }
         n && /\.space/ { print "  " n " = 0,"; n = "" }' "$out/consts.s"
    arm-none-eabi-nm "$ELF" | awk -v pat="$pattern" '$3 ~ pat && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
    # Ichor's own functions and scripts, by name, for checks that look for them.
    arm-none-eabi-nm "$ELF" | awk '$3 ~ /^(Ichor|EventScript_Ichor)[A-Za-z0-9_]*$|^EventScript_(CutTree|RockSmash|StrengthBoulder|UseSurf|UseWaterfall|UseDive)$/ && !seen[$3]++ { print "  " $3 " = 0x" $1 "," }'
    echo "}"
  } > "$out/engine_symbols.lua"

  [ -n "$asm" ] || return 0
  tools/preproc/preproc -s "$asm" charmap.txt \
    | arm-none-eabi-cpp -iquote include -Wno-trigraphs -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -I include - \
    | tools/preproc/preproc -ie "$asm" charmap.txt \
    | arm-none-eabi-as -mcpu=arm7tdmi -march=armv4t -meabi=5 --defsym MODERN=1 --defsym EMERALD=1 -o "$out/setup.o" \
    || { echo "$tag FAIL: could not assemble $asm"; exit 1; }
  arm-none-eabi-ld -e 0 -Ttext=$BLOB_ADDR --just-symbols="$ELF" -o "$out/setup.elf" "$out/setup.o" \
    && arm-none-eabi-objcopy -O binary -j .text "$out/setup.elf" "$out/setup.bin" \
    || { echo "$tag FAIL: could not link the setup blob"; exit 1; }
  arm-none-eabi-nm "$out/setup.elf" | awk '$3 ~ /(Header|Script)$/ { print $3, $1 }' > "$out/setup.syms"
}

engine_run() {
  local tag="$1" out="$2" lua="$3" frames="$4" secs="$5"
  ENGINE_OUT="$out/" ENGINE_TAG="$tag" ENGINE_BLOB_ADDR=$BLOB_ADDR ${TIMEOUT:+$TIMEOUT $secs} "$RUNNER" \
    --script "$lua" --frames "$frames" --until "$tag done" "$ROM" > "$out/run.log" 2>&1
  local code=$?
  grep -o "$tag \(ok\|FAIL\|NOTE\|BUG\).*" "$out/run.log"
  local crash="invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion"
  if grep -qiE "$crash" "$out/run.log"; then
    echo "$tag FAIL: crash-like errors in $out/run.log"; grep -iE "$crash" "$out/run.log" | head -5; exit 1
  fi
  if grep -q "$tag \(FAIL\|BUG\)" "$out/run.log" || ! grep -q "$tag done" "$out/run.log"; then
    echo "$tag FAIL: see $out/run.log (runner exit $code)"; exit 1
  fi
  echo "$tag PASS: $(grep -c "$tag ok" "$out/run.log") checks, $(ls "$out"/shots/*.png 2>/dev/null | wc -l | tr -d ' ') screenshots in $out/shots/"
}
