# This should work on Linux.  Modify as needed for other platforms.

BOINC_SOURCE_API_DIR = $(BOINC_DIR)/api
BOINC_SOURCE_LIB_DIR = $(BOINC_DIR)/lib
BOINC_SOURCE_ZIP_DIR = $(BOINC_DIR)/zip
FREETYPE_DIR = /usr/include/freetype2

BOINC_API_DIR = $(BOINC_SOURCE_API_DIR)
BOINC_LIB_DIR = $(BOINC_SOURCE_LIB_DIR)
BOINC_ZIP_DIR = $(BOINC_SOURCE_ZIP_DIR)

#MAKEFILE_LDFLAGS = -lpthread libstdc++.a
MAKEFILE_LDFLAGS = -lpthread libstdc++.a -static
MAKEFILE_STDLIB  = libstdc++.a

#    -O3 
CXXFLAGS += -g \
    -Wall -W -Wshadow -Wpointer-arith -Wcast-qual -Wcast-align -Wunused-parameter -Wno-write-strings -fno-common \
    -DAPP_GRAPHICS \
    -I$(BOINC_DIR) \
    -I$(BOINC_SOURCE_API_DIR) \
    -I$(BOINC_SOURCE_LIB_DIR) \
    -I$(BOINC_SOURCE_ZIP_DIR) \
    -I$(FREETYPE_DIR) \
    -L$(BOINC_API_DIR) \
    -L$(BOINC_LIB_DIR) \
    -L/usr/X11R6/lib \
    -L/usr/lib \
    -L.

# to get the graphics app to compile you may need to install some packages
# e.g. ftgl-devel.x86_64
#
# You may have to change the paths for your system.

LIBGLUT = -lglut
LIBGLU = -lGLU
LIBGL= -lGL
LIBUI = -lX11 -lXmu
LIBFTGL = -lftgl
LIBJPEG = -ljpeg

ifdef BUILD_WITH_VCPKG
  BUILD_DIR     = $(BOINC_DIR)/3rdParty/linux
  VCPKG_DIR     ?= $(BUILD_DIR)/vcpkg/installed/x64-linux

  CXXFLAGS += \
    -I$(VCPKG_DIR)/include \
    -L$(VCPKG_DIR)/lib

  LIBUI = -lX11 -lXmu -lXrandr -lXxf86vm -lXi
  LIBFTGL = -lftgl -lfreetype -lpng -lbz2 -lbrotlidec-static -lbrotlienc-static -lbrotlicommon-static -lz
endif

ifdef BUILD_WITH_MINGW
  LIBGLUT = -lfreeglut_static
  LIBGLU = -lglu32
  LIBGL= -lopengl32
  LIBUI = -lgdi32 -lwinmm
  LIBFTGL = -lftgl -lfreetype -lpng -lbz2 -lbrotlidec-static -lbrotlienc-static -lbrotlicommon-static -lz
endif

PROGS = xboinc
# make this optional so compile doesn't break on systems without OpenGL

$(info All PROGS=$(PROGS))

all: $(PROGS)

libstdc++.a:
	ln -s `$(CXX) $(CXXFLAGS) -print-file-name=libstdc++.a`

ttfont.cpp:
	ln -s ../../api/ttfont.cpp .

clean: distclean

distclean:
	/bin/rm -f $(PROGS) $(addsuffix .exe, $(PROGS)) *.o libstdc++.a ttfont.cpp

install: xboinc

# specify library paths explicitly (rather than -l)
# because otherwise you might get a version in /usr/lib etc.

xboinc: xboinc.o $(MAKEFILE_STDLIB) $(BOINC_API_DIR)/libboinc_api.a $(BOINC_LIB_DIR)/libboinc.a
	$(CXX) $(CXXFLAGS) $(CPPFLAGS) $(LDFLAGS) -o xboinc xboinc.o \
	-o xboinc_executable -lm \
	-lboinc_api -lboinc $(MAKEFILE_LDFLAGS) \
	$(STDCPPTC)
