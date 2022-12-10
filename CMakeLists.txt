# PatchCookBook

cmake_minimum_required(VERSION 3.18)

project(PatchCookbook VERSION 0.1.1 LANGUAGES NONE)

set(VERSION_STRING "PatchCookbook_v${PatchCookbook_VERSION}")

find_file(PYTHON NAMES python python3)

if(PYTHON STREQUAL "PYTHON-NOTFOUND")
	if (WIN32)
		# Hardcode and hope
		set(PYTHON python)
	else()
		message(SEND_ERROR "Could not find a python executable")
	endif()
endif()

if (WIN32)
	set(ZIP "tar" "-acvf")
else()
	set(ZIP "zip" "-9" "-r")
endif()

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
 		--out ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd 
 		--in ${CMAKE_CURRENT_SOURCE_DIR}/src/m4l/PatchCookbook.amxd.in
 		"VERSION_STRING=${VERSION_STRING}"
     DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
     VERBATIM
     )

#add_custom_command(
#    OUTPUT PatchCookbook.amxd
#    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/src/m4l/PatchCookbook.amxd.in 
#                ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd
#    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
#    VERBATIM
#    )

add_custom_target(device_file ALL 
    DEPENDS 
        ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd 
        ${patches_SRC} 
        ${CMAKE_CURRENT_SOURCE_DIR}/src/configure/configure.py
    )

#----------------------------#
# Generate the patch file

set(patchfileNAME "patches.json")
set(patchfilePATH "${CMAKE_CURRENT_BINARY_DIR}/${patchfileNAME}")
set(consolidateSCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/src/consolidate/consolidate.py")

add_custom_command(
    OUTPUT ${patchfileNAME}
    COMMAND ${PYTHON} ${consolidateSCRIPT} 
        --out ${patchfilePATH} ${CMAKE_CURRENT_SOURCE_DIR}/recipes
    DEPENDS ${consolidateSCRIPT}
    VERBATIM
    )

add_custom_target(patch_file ALL 
    DEPENDS 
        ${patchfilePATH} 
		${patches_SRC} 
		${consolidateSCRIPT}
    )

#---------------------------#
# Generate the zip file

set(tempDIR PatchCookbook)
set(zipfileNAME "${VERSION_STRING}.zip")


add_custom_command(
    OUTPUT ${zipfileNAME}
    COMMAND ${CMAKE_COMMAND} -E  rm -rf ${tempDIR}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${tempDIR}
    COMMAND ${CMAKE_COMMAND} -E copy patches.json ${tempDIR}
    COMMAND ${CMAKE_COMMAND} -E copy ${m4l_SRC} 
		${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd 
		${tempDIR}
    COMMAND ${ZIP} ${zipfileNAME} ${tempDIR}
    COMMAND ${CMAKE_COMMAND} -E rm -rf ${tempDIR}
    DEPENDS ${m4l_SRC} ${CMAKE_CURRENT_BINARY_DIR}/PatchCookbook.amxd
    VERBATIM
    )
	
add_custom_target(zipfile ALL
    DEPENDS patch_file device_file ${m4l_SRC} ${zipfileNAME}
    )

#---------------------------#
# Add testing

add_test(NAME PythonTests
    COMMAND ${PYTHON} -m unittest discover ${CMAKE_CURRENT_SOURCE_DIR}/tests
    )

set_property(TEST PythonTests
    PROPERTY ENVIRONMENT PYTHONPATH=${CMAKE_CURRENT_SOURCE_DIR}/src
    )
