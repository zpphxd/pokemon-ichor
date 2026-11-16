# Shared host setup and verdicts. Source from the repository root.

export PATH="${DEVKITARM:-/opt/devkitpro/devkitARM}/bin:$PATH:$HOME/.local/bin:/opt/homebrew/bin"
RUNNER=build/tools/ichor-mgba-headless

harness_require() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "HARNESS FAIL: missing $1 ($2)" >&2
    return 1
  }
}

harness_timeout() {
  TIMEOUT=$(command -v gtimeout || command -v timeout) || {
    echo "HARNESS FAIL: install coreutils for timeout (Homebrew on macOS, apt on Ubuntu)" >&2
    return 1
  }
}

harness_prepare() {
  harness_timeout || return 1
  harness_require cc "install a host C compiler" || return 1
  local prefix="${MGBA_PREFIX:-}" tmp="${RUNNER}.tmp.$$"
  local -a flags
  flags=(-lmgba)
  if [ -z "$prefix" ] && [ "$(uname -s)" = Darwin ]; then
    harness_require brew "install Homebrew and mgba, or set MGBA_PREFIX" || return 1
    prefix=$(brew --prefix mgba) || return 1
  fi
  if [ -n "$prefix" ]; then
    flags=("-I$prefix/include" "-L$prefix/lib" "-Wl,-rpath,$prefix/lib" -lmgba)
  fi
  mkdir -p build/tools || return 1
  # Recompile this small runner to validate current headers, library and Lua API,
  # rather than trusting a cached executable from another toolchain.
  if ! cc -O2 tools/ichor/mgba_headless.c "${flags[@]}" -o "$tmp"; then
    rm -f "$tmp"
    echo "HARNESS FAIL: need Lua-capable mGBA 0.10.5 development headers/library; see design/ENGINEERING.md" >&2
    return 1
  fi
  mv "$tmp" "$RUNNER" || return 1
}

harness_result() {
  local tag="$1" log="$2" code="$3" complete="${4:-$1 done}"
  if [ "$code" -ne 0 ]; then
    echo "$tag FAIL: runner exit $code (including timeout); see $log" >&2
    return 1
  fi
  if [ ! -f "$log" ] || ! grep -Fq "$complete" "$log"; then
    echo "$tag FAIL: missing completion '$complete'; see $log" >&2
    return 1
  fi
  if grep -qiE "(^|[[:space:]])$tag (FAIL|BUG)(:|[[:space:]]|$)|invalid address|illegal opcode|undefined instruction|bad (read|write)|abort|assertion" "$log"; then
    echo "$tag FAIL: failure/bug/crash in $log" >&2
    return 1
  fi
}

harness_assemble() {
  local source="$1" output="$2"
  (set -o pipefail
    tools/preproc/preproc -s "$source" charmap.txt \
      | arm-none-eabi-cpp -iquote include -Wno-trigraphs -DMODERN=1 -DTESTING=0 -DEMERALD -std=gnu17 -I include - \
      | tools/preproc/preproc -ie "$source" charmap.txt \
      | arm-none-eabi-as -mcpu=arm7tdmi -march=armv4t -meabi=5 --defsym MODERN=1 --defsym EMERALD=1 -o "$output"
  )
}
