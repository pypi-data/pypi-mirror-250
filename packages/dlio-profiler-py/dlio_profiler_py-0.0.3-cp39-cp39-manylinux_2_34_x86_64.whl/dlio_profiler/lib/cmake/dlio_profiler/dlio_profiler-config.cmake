set(DLIO_PROFILER_FOUND TRUE)

# Include directories
set(DLIO_PROFILER_INCLUDE_DIRS "/home/runner/work/dlio-profiler/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/include")
if (NOT IS_DIRECTORY "${DLIO_PROFILER_INCLUDE_DIRS}")
    set(DLIO_PROFILER_FOUND FALSE)
endif ()
#message(STATUS "DLIO_PROFILER_INCLUDE_DIRS: " ${DLIO_PROFILER_INCLUDE_DIRS})
get_filename_component(DLIO_PROFILER_ROOT_DIR ${DLIO_PROFILER_INCLUDE_DIRS}/.. ABSOLUTE)
#message(STATUS "DLIO_PROFILER_ROOT_DIR: " ${DLIO_PROFILER_ROOT_DIR})
set(DLIO_PROFILER_LIBRARY_PATH "/home/runner/work/dlio-profiler/dlio-profiler/build/lib.linux-x86_64-3.9/dlio_profiler/lib")
link_directories(${DLIO_PROFILER_LIBRARY_PATH})
set(DLIO_PROFILER_LIBRARIES dlio-profiler)
set(DLIO_PROFILER_DEFINITIONS "")
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(dlio-profiler
            REQUIRED_VARS DLIO_PROFILER_FOUND DLIO_PROFILER_INCLUDE_DIRS DLIO_PROFILER_LIBRARIES)
