 cmake_minimum_required(VERSION 3.18)

 set(m4l_device ${CMAKE_CURRENT_SOURCE_DIR}/PatchCookbook.amxd)
 file(GLOB m4l_js CONFIGURE_DEPENDS  ${CMAKE_CURRENT_SOURCE_DIR}/*.js)
 message(STATUS "js sources are ${m4l_js}")

 set(m4l_SRC ${m4l_device} ${m4l_js} PARENT_SCOPE)

