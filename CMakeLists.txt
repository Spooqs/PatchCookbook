# OperatorCookBook

cmake_minimum_required(VERSION 3.18)

project(OperatorCookBook VERSION 0.1.0 LANGUAGES NONE)

#find_progam(PYTHON NAMES "python" "python3")
find_file(PYTHON NAMES python python3)

add_custom_command(
    OUTPUT patches.json
    COMMAND ${PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py --out patches.json  ${CMAKE_CURRENT_SOURCE_DIR}/recipes
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    VERBATIM
    )

add_custom_target(patch_file ALL 
    DEPENDS patches.json ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    )

enable_testing()

add_test(NAME PythonTests
    COMMAND ${PYTHON} -m unittest discover ${CMAKE_CURRENT_SOURCE_DIR}/tests
    )

set_property(TEST PythonTests
    PROPERTY ENVIRONMENT PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/src
    )
