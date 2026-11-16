// Headless mGBA runner with Lua scripting, used by Ichor's automated tests.
//
// The bundled tools/mgba/mgba-rom-test-mac is built without a Lua engine, so
// its --script flag fails, and mGBA 0.10's own frontends have no --script
// flag. This links a Lua-capable libmgba (Homebrew, Linux, or MGBA_PREFIX).
//
// Usage: ichor-mgba-headless [--script FILE]... [--frames N] [--until TEXT] ROM
// It runs until a log line contains TEXT (default "SMOKE done"), or for N frames
// (default 36000). Script console:log output and ROM mgba printf go to stdout.
// Exit code: 0 when TEXT was seen, 2 when the frame limit was hit, 1 on load errors.
#include <mgba/flags.h>
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba/core/scripting.h>
#include <mgba/script/context.h>
#include <mgba/internal/script/lua.h>
#include <mgba-util/vfs.h>

#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char* untilText = "SMOKE done";
static bool finished = false;

static void logLine(struct mLogger* logger, int category, enum mLogLevel level, const char* format, va_list args) {
	(void) logger;
	const char* name = mLogCategoryName(category);
	// Keep errors, script output and the ROM's own mgba printf; drop the
	// per-DMA and per-register chatter mGBA logs at INFO.
	bool wanted = (level & (mLOG_FATAL | mLOG_ERROR | mLOG_GAME_ERROR))
		|| (name && (!strcmp(name, "Scripting") || !strcmp(name, "GBA Debug")));
	if (!wanted) {
		return;
	}
	char line[1024];
	vsnprintf(line, sizeof(line), format, args);
	printf("[%s] %s\n", name ? name : "?", line);
	if (strstr(line, untilText)) {
		finished = true;
	}
}

int main(int argc, char** argv) {
	const char* rom = NULL;
	const char* scripts[16];
	int nScripts = 0;
	long maxFrames = 36000;
	for (int i = 1; i < argc; ++i) {
		if (!strcmp(argv[i], "--script") && i + 1 < argc && nScripts < 16) {
			scripts[nScripts++] = argv[++i];
		} else if (!strcmp(argv[i], "--frames") && i + 1 < argc) {
			maxFrames = strtol(argv[++i], NULL, 10);
		} else if (!strcmp(argv[i], "--until") && i + 1 < argc) {
			untilText = argv[++i];
		} else {
			rom = argv[i];
		}
	}
	if (!rom) {
		fprintf(stderr, "usage: %s [--script FILE]... [--frames N] [--until TEXT] ROM\n", argv[0]);
		return 1;
	}
	setvbuf(stdout, NULL, _IOLBF, 0);

	struct mLogger logger = { .log = logLine, .filter = NULL };
	mLogSetDefaultLogger(&logger);

	struct mCore* core = mCoreFind(rom);
	if (!core || !core->init(core)) {
		fprintf(stderr, "cannot open %s\n", rom);
		return 1;
	}
	mCoreInitConfig(core, NULL);
	unsigned width, height;
	core->desiredVideoDimensions(core, &width, &height);
	color_t* video = calloc((size_t) width * height, sizeof(color_t));
	core->setVideoBuffer(core, video, width);
	if (!mCoreLoadFile(core, rom)) {
		fprintf(stderr, "cannot load %s\n", rom);
		return 1;
	}
	core->reset(core);

	struct mScriptContext context;
	mScriptContextInit(&context);
	mScriptContextAttachStdlib(&context);
	struct mScriptEngineContext* lua = mScriptContextRegisterEngine(&context, mSCRIPT_ENGINE_LUA);
	if (!lua) {
		fprintf(stderr, "mGBA has no Lua engine; rebuild with scripting and Lua enabled\n");
		mScriptContextDeinit(&context);
		core->deinit(core);
		free(video);
		return 1;
	}
	mScriptContextAttachCore(&context, core);
	mScriptContextAttachLogger(&context, &logger);
	// In 0.10, mScriptContextLoadFile only loads a chunk; it has to be run too.
	for (int i = 0; i < nScripts; ++i) {
		struct VFile* vf = VFileOpen(scripts[i], O_RDONLY);
		if (!vf || !lua->load(lua, scripts[i], vf) || !lua->run(lua)) {
			fprintf(stderr, "cannot run script %s: %s\n", scripts[i], lua->getError(lua) ? lua->getError(lua) : "not found");
			return 1;
		}
	}

	long frame = 0;
	for (; frame < maxFrames && !finished; ++frame) {
		core->runFrame(core);
		mScriptContextTriggerCallback(&context, "frame");
	}
	printf("[runner] stopped after %ld frames (%s)\n", frame, finished ? "done" : "frame limit");

	mScriptContextDeinit(&context);
	core->deinit(core);
	free(video);
	return finished ? 0 : 2;
}
