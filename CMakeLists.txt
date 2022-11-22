# OperatorCookBook

cmake_minimum_required(VERSION 3.18)

project(PatchCookbook VERSION 0.0.1 LANGUAGES NONE)

#find_progam(PYTHON NAMES "python" "python3")
find_file(PYTHON NAMES python python3)

find_file(TOUCH NAMES touch)

file(GLOB patches_SRC CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/recipes/*.recipe)

set(m4l_SRC x)
add_subdirectory(src/m4l)

add_custom_command(
    OUTPUT patches.json
    COMMAND ${PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py 
        --out ${CMAKE_CURRENT_BINARY_DIR}/patches.json ${CMAKE_CURRENT_SOURCE_DIR}/recipes
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    VERBATIM
    )

add_custom_target(patch_file ALL 
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/patches.json ${patches_SRC} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    )

set(tempDIR PatchCookbook)

add_custom_command(
    OUTPUT PatchCookbook_v${PatchCookbook_VERSION}.zip
    COMMAND rm -rf ${tempDIR}
    COMMAND mkdir ${tempDIR}
    COMMAND cp patches.json ${tempDIR}
    COMMAND cp ${m4l_SRC} ${tempDIR}
    COMMAND zip -9 -r PatchCookbook_v${PatchCookbook_VERSION}.zip ${tempDIR}
    DEPENDS ${m4l_SRC}
    VERBATIM
    )


add_custom_target(zipfile ALL
    DEPENDS patch_file ${m4l_SRC} ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook_v${PatchCookbook_VERSION}.zip
    )

add_test(NAME PythonTests
    COMMAND ${PYTHON} -m unittest discover ${CMAKE_CURRENT_SOURCE_DIR}/tests
    )

set_property(TEST PythonTests
    PROPERTY ENVIRONMENT PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/src
    )
