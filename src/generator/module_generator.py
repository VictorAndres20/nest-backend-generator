class ModuleGenerator:

    def __init__(self, name):
        self.name = name
        self.main_imports = ["import { Module } from '@nestjs/common';"]
        self.imports = []
        self.controllers = []
        self.providers = []
        self.exports = []
        self.content = ""

    def clean(self):
        self.main_imports = ["import { Module } from '@nestjs/common';"]
        self.imports = []
        self.controllers = []
        self.providers = []
        self.exports = []
        self.content = ""

    def build_class(self):
        self.build_main_imports()
        self.build_init()
        self.build_imports()
        self.build_controllers()
        self.build_providers()
        self.build_exports()
        self.build_close()

    def build_main_imports(self):
        for i in self.main_imports:
            self.content += str(i) + "\n"
        self.content += "\n"

    def build_init(self):
        self.content += "@Module({\n"

    def build_imports(self):
        self.content += "  imports: [\n"
        for i in self.imports:
            self.content += "    " + str(i) + ",\n"
        self.content += "  ],\n"

    def build_controllers(self):
        self.content += "  controllers: [\n"
        for i in self.controllers:
            self.content += "    " + str(i) + ",\n"
        self.content += "  ],\n"

    def build_providers(self):
        self.content += "  providers: [\n"
        for i in self.providers:
            self.content += "    " + str(i) + ",\n"
        self.content += "  ],\n"

    def build_exports(self):
        self.content += "  exports: [\n"
        for i in self.exports:
            self.content += "    " + str(i) + ",\n"
        self.content += "  ],\n"

    def build_close(self):
        self.content += "})\nexport class " + self.name + "Module{}"
