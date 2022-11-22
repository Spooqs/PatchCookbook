# PatchCookBook

cmake_minimum_required(VERSION 3.18)

project(PatchCookbook VERSION 0.0.1 LANGUAGES NONE)

set(VERSION_STRING "PatchCookbook_v${PatchCookbook_VERSION}")

find_file(PYTHON NAMES python python3)

# Find all the recipe files. This will be used later to make sure
# the patch file gets updated if any of the recipe cards change.
file(GLOB patches_SRC CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/recipes/*.recipe)

# Add precessing for the actual device.
set(m4l_SRC x)
add_subdirectory(src/m4l)

#----------------------------#
# Generate the device file

add_custom_command(
    OUTPUT PatchCookbook.amxd
    COMMAND ${PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
    --out ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd --in ${CMAKE_CURRENT_SOURCE_DIR}/src/m4l/PatchCookbook.amxd.in
    "VERSION_STRING=${VERSION_STRING}"
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
    VERBATIM
    )

add_custom_target(device_file ALL 
    DEPENDS 
        ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd 
        ${patches_SRC} 
        ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
    )

#----------------------------#
# Generate the patch file

add_custom_command(
    OUTPUT patches.json
    COMMAND ${PYTHON} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py 
        --out ${CMAKE_CURRENT_BINARY_DIR}/patches.json ${CMAKE_CURRENT_SOURCE_DIR}/recipes
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    VERBATIM
    )

add_custom_target(patch_file ALL 
    DEPENDS 
        ${CMAKE_CURRENT_BINARY_DIR}/patches.json ${patches_SRC} ${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py
    )

#---------------------------#
# Generate the zip file

set(tempDIR PatchCookbook)

add_custom_command(
    OUTPUT ${VERSION_STRING}.zip
    COMMAND rm -rf ${tempDIR}
    COMMAND mkdir ${tempDIR}
    COMMAND cp patches.json ${tempDIR}
    COMMAND cp ${m4l_SRC} ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd ${tempDIR}
    COMMAND zip -9 -r ${VERSION_STRING}.zip ${tempDIR}
    COMMAND rm -rf ${tempDIR}
    DEPENDS ${m4l_SRC}  ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd
    VERBATIM
    )


add_custom_target(zipfile ALL
    DEPENDS patch_file device_file ${m4l_SRC} ${VERSION_STRING}.zip
    )

#---------------------------#
# Add testing

add_test(NAME PythonTests
    COMMAND ${PYTHON} -m unittest discover ${CMAKE_CURRENT_SOURCE_DIR}/tests
    )

set_property(TEST PythonTests
    PROPERTY ENVIRONMENT PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/src
    )
