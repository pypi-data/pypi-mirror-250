from ogre.docker_management.imports import GetImports

find_imports = GetImports("/home/wilder/dev/3rd-party/OpenGA")

#print(find_imports.get_py_files())

find_imports.get_imported_modules()

print(find_imports.modules)

requirements_file = open("requirements.txt", "w")

for mod in find_imports.modules:
    native = find_imports.is_native_module(mod)
    print("{} = {}".format(native, mod))
    if not native:
        print("{}".format(mod))
        requirements_file.write("%s\n" % mod)

requirements_file.close()
