import os

c_compiler_command="gcc -o %shortname% %fullname%"
cpp_compiler_command="g++ -o %shortname% %fullname%"
lua_compiler_command="luac -o %shortname% %fullname%"
java_compiler_command="javac -d bin %name%"
directories_to_compile=["Lexer"]