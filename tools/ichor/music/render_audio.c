// Render a ROM's audio output to a 16-bit stereo WAV, headlessly, with libmgba.
//
// Used by tools/ichor/music/preview.py, which patches a copy of the ROM so the
// title screen plays the song under test, then calls this to record it. The
// audio is the real GBA mix (m4a driver, voicegroups, PSG channels), so it is
// the closest thing to listening on hardware we can do without a speaker.
//
// Usage: ichor-render-audio ROM OUT.wav FRAMES [PRESS_START_FRAME]
// Records FRAMES frames from power-on. If PRESS_START_FRAME is given, START is
// held for 6 frames there (to skip the intro and reach the title screen).
#include <mgba/core/core.h>
#include <mgba/core/log.h>

#include <stdarg.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// blip_buf is exported by libmgba but its header is not installed.
struct blip_t;
int blip_samples_avail(const struct blip_t*);
int blip_read_samples(struct blip_t*, short out[], int count, int stereo);
void blip_set_rates(struct blip_t*, double clockRate, double sampleRate);

#define SAMPLE_RATE 32768
#define KEY_START (1 << 3)

static void quietLog(struct mLogger* logger, int category, enum mLogLevel level, const char* format, va_list args) {
	(void) logger;
	(void) category;
	if (level & (mLOG_FATAL | mLOG_ERROR)) {
		vfprintf(stderr, format, args);
		fputc('\n', stderr);
	}
}

static void put32(FILE* f, uint32_t v) {
	uint8_t b[4] = { v, v >> 8, v >> 16, v >> 24 };
	fwrite(b, 1, 4, f);
}

static void put16(FILE* f, uint16_t v) {
	uint8_t b[2] = { v, v >> 8 };
	fwrite(b, 1, 2, f);
}

static void writeHeader(FILE* f, uint32_t frames) {
	uint32_t dataBytes = frames * 4;
	fseek(f, 0, SEEK_SET);
	fwrite("RIFF", 1, 4, f);
	put32(f, 36 + dataBytes);
	fwrite("WAVEfmt ", 1, 8, f);
	put32(f, 16);
	put16(f, 1); // PCM
	put16(f, 2); // stereo
	put32(f, SAMPLE_RATE);
	put32(f, SAMPLE_RATE * 4);
	put16(f, 4);
	put16(f, 16);
	fwrite("data", 1, 4, f);
	put32(f, dataBytes);
}

int main(int argc, char** argv) {
	if (argc < 4) {
		fprintf(stderr, "usage: %s ROM OUT.wav FRAMES [PRESS_START_FRAME]\n", argv[0]);
		return 1;
	}
	const char* rom = argv[1];
	long frames = strtol(argv[3], NULL, 10);
	long pressAt = argc > 4 ? strtol(argv[4], NULL, 10) : -1;

	struct mLogger logger = { .log = quietLog, .filter = NULL };
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
	core->setAudioBufferSize(core, 4096);
	struct blip_t* left = core->getAudioChannel(core, 0);
	struct blip_t* right = core->getAudioChannel(core, 1);
	blip_set_rates(left, core->frequency(core), SAMPLE_RATE);
	blip_set_rates(right, core->frequency(core), SAMPLE_RATE);
	core->reset(core);

	FILE* out = fopen(argv[2], "wb");
	if (!out) {
		fprintf(stderr, "cannot write %s\n", argv[2]);
		return 1;
	}
	writeHeader(out, 0);

	short buffer[8192];
	uint32_t written = 0;
	for (long frame = 0; frame < frames; ++frame) {
		core->setKeys(core, (pressAt >= 0 && frame >= pressAt && frame < pressAt + 6) ? KEY_START : 0);
		core->runFrame(core);
		int avail = blip_samples_avail(left);
		while (avail > 0) {
			int n = avail > 4096 ? 4096 : avail;
			blip_read_samples(left, buffer, n, 1);
			blip_read_samples(right, buffer + 1, n, 1);
			fwrite(buffer, sizeof(short), (size_t) n * 2, out);
			written += n;
			avail -= n;
		}
	}
	writeHeader(out, written);
	fclose(out);
	core->deinit(core);
	free(video);
	printf("wrote %s: %u samples (%.1f s)\n", argv[2], written, written / (double) SAMPLE_RATE);
	return 0;
}
