#!/usr/bin/env bash
mkdir -p riscv-gnu-toolchain
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain.git riscv-gnu-toolchain
pushd riscv-gnu-toolchain || exit
cat >>.git/config <<EOF
[submodule "binutils"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/binutils.git
EOF
mkdir -p binutils
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/binutils.git binutils
git submodule init binutils
git submodule update binutils
pushd binutils || exit
popd || exit
cat >>.git/config <<EOF
[submodule "gcc"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/gcc.git
EOF
mkdir -p gcc
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/gcc.git gcc
git submodule init gcc
git submodule update gcc
pushd gcc || exit
popd || exit
cat >>.git/config <<EOF
[submodule "glibc"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/glibc.git
EOF
mkdir -p glibc
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/glibc.git glibc
git submodule init glibc
git submodule update glibc
pushd glibc || exit
popd || exit
cat >>.git/config <<EOF
[submodule "newlib"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/newlib.git
EOF
mkdir -p newlib
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/newlib.git newlib
git submodule init newlib
git submodule update newlib
pushd newlib || exit
popd || exit
cat >>.git/config <<EOF
[submodule "gdb"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/gdb.git
EOF
mkdir -p gdb
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/gdb.git gdb
git submodule init gdb
git submodule update gdb
pushd gdb || exit
popd || exit
cat >>.git/config <<EOF
[submodule "qemu"]
        active = true
        url = https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/qemu.git
EOF
mkdir -p qemu
git clone https://mirror.iscas.ac.cn/riscv-toolchains/git/riscv-collab/riscv-gnu-toolchain/qemu.git qemu
git submodule init qemu
git submodule update qemu
pushd qemu || exit
git submodule absorbgitdirs
popd || exit
