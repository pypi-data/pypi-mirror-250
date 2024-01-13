# A CMake config file for the library, to be used by external projects


####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was mqt-core-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

check_required_components(mqt-core)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}")

include(CMakeFindDependencyMacro)
find_dependency(GMP)
find_dependency(pybind11_json)

if(TARGET MQT::Core)
  return()
endif()

include("${CMAKE_CURRENT_LIST_DIR}/Cache.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/CompilerOptions.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/CompilerWarnings.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/GetVersion.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/PackageAddTest.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/PreventInSourceBuilds.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/Sanitizers.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/StandardProjectSettings.cmake")
include("${CMAKE_CURRENT_LIST_DIR}/mqt-core-targets.cmake")

if(NOT mqt-core_FIND_QUIETLY)
  message(STATUS "Found mqt-core version ${mqt-core_VERSION}")
endif()
