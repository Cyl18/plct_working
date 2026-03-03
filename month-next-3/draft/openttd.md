<!-- markdownlint-disable -->

sudo apt install -y \
    build-essential \
    pkg-config \
    zlib1g-dev \
    liblzma-dev \
    libpng-dev \
    liblzo2-dev \
    libcurl4-openssl-dev \
    libsdl2-dev \
    libfreetype-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libicu-dev cmake ninja-build

   20  ruyi install gnu-plct
   21  ruyi venv -t gnu-plct generic venv
   22  . venv/bin/ruyi-activate
   23  mkdir build\ncd build


cmake .. -DCMAKE_CXX_COMPILER=riscv64-plct-linux-gnu-g++ -DCMAKE_C_COMPILER=riscv64-plct-linux-gnu-gcc -DCMAKE_TOOLCHAIN_FILE=../venv/toolchain.cmake


sudo nano /etc/apt/sources.list.d/riscv.sources

