from conans import ConanFile, CMake, tools
import os

class Urho3dConan(ConanFile):
	name = "Urho3D"
	version = "master"
	license = "MIT"
	url = "https://github.com/urho3d/Urho3D"
	description = "Cross-platform 2D and 3D game engine."
	settings = "os", "compiler", "build_type", "arch"
	#TODO add all of Urho3D's cmake settings
	options = {
		"static_runtime": [True, False],
		"samples": [True, False],
		"opengl": [True, False]
	}
	#TODO Urho3D decides on default options when configured, like Direct3D if on Windows
		# if I dont provide default options, will it just let Urho use whatever it defaults to?
			# all options must be defined: http://docs.conan.io/en/latest/reference/conanfile/attributes.html#options-default-options
				# have a "Default" option in addition to [True, False], which doesn't set the cmake setting
	default_options = "static_runtime=False", "samples=False", "opengl=True"
	generators = "cmake"

	def source(self):
		self.run("git clone --branch master --depth 1 https://github.com/urho3d/Urho3D.git")

	def build(self):
		cmake = CMake(self)
		cmake_settings = {
			"URHO3D_STATIC_RUNTIME": self.options.static_runtime,
			"URHO3D_SAMPLES": self.options.samples,
			"URHO3D_OPENGL": self.options.opengl
		}
		cmake.configure(source_folder="%s/Urho3D" % self.source_folder, defs=cmake_settings)
		cmake.build()

	def package(self):
		self.copy("*.h", dst="include", src="include")
		self.copy("*.hpp", dst="include", src="include")
		self.copy("*Urho3D.lib", dst="lib", keep_path=False)
		self.copy("*Urho3D_d.lib", dst="lib", keep_path=False)
		self.copy("*.dll", dst="bin", keep_path=False)
		self.copy("*.so", dst="lib", keep_path=False)
		self.copy("*.dylib", dst="lib", keep_path=False)
		self.copy("*.a", dst="lib", keep_path=False)

	def package_info(self):
		self.cpp_info.includedirs = [
			'include',
			'include/Urho3D/ThirdParty',
			'include/Urho3D/ThirdParty/Bullet',
			'include/Urho3D/ThirdParty/Lua'
		]
	
		# libs
		if self.settings.build_type == "Debug":
			self.cpp_info.libs.append("Urho3D_d")
		else:
			self.cpp_info.libs.append("Urho3D")
		
		#TODO UrhoCommmon.cmake contains the logic for adding additioanl conditional libraries
		#TODO should be conditional on "opengl" option and windows
		self.cpp_info.libs.append("opengl32") # comes from Windows SDK
		
		#TODO windows specific
		self.cpp_info.libs.extend(["winmm", "imm32", "version"])
