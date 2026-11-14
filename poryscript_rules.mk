# Poryscript (Pokemon Ichor addition)
# Any data/maps/<Map>/scripts.pory or data/scripts/*.pory is compiled to the
# .inc file next to it. When converting a map to Poryscript, delete its tracked
# scripts.inc and list that path in .gitignore, because it becomes generated.
PORYSCRIPT ?= poryscript
PORYSCRIPT_ARGS := -fc tools/poryscript/font_config.json -cc tools/poryscript/command_config.json

PORY_SOURCES := $(wildcard $(DATA_ASM_SUBDIR)/maps/*/scripts.pory) $(wildcard $(DATA_ASM_SUBDIR)/scripts/*.pory)
PORY_OUTPUTS := $(PORY_SOURCES:%.pory=%.inc)
AUTO_GEN_TARGETS += $(PORY_OUTPUTS)

$(PORY_OUTPUTS): %.inc: %.pory tools/poryscript/font_config.json tools/poryscript/command_config.json
	$(PORYSCRIPT) -i $< -o $@ $(PORYSCRIPT_ARGS)
