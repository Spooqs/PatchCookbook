# OperatorCookBook

cmake_minimum_required(VERSION 3.18)

project(OperatorCookBook VERSION 0.1.0 LANGUAGES NONE)

#find_progam(PYTHON NAMES "python" "python3")
find_file(PYTHON NAMES python python3)

add_custom_command(
    OUTPUT patches.json
    COMMAND ${PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate.py --out patches.json  ${CMAKE_CURRENT_SOURCE_DIR}/recipes
    VERBATIM
    )

add_custom_target(patch_file ALL DEPENDS patches.json)
