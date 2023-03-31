---
date created: 2023-03-31 19:15
date updated: 2023-03-31 20:10
---

# RT-thread 移植

## Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Usage](#usage)
- [Contributing](../CONTRIBUTING.md)

## About <a name = "about"></a>

该项目服务于移植各种开源处理器核于一生一芯 SOC 上. 移植最终的综合测试为成功启动 [RT-thread](https://github.com/OSCPU/rt-thread) 实时操作系统. 为加速移植进度, 该项目通过在 qemu 中修改增加 ram, flash 起始地址以及空间大小符合将要移植的处理器核参数的机器来验证对 RT-thread 系统相对应修改的正确性, 最终将修改后的 RT-thread 作为开源处理器核移植项目的测试程序.

## Getting Started <a name = "getting_started"></a>

1. `riscv-gnu-toolchain` 交叉编译工具链
2. `qemu` `risc-v` 全系统模拟器

### Prerequisites

#### 1. 构建 `riscv-gnu-toolchain` 的裸机 `newlib` 交叉编译器

##### 构建依赖

On Ubuntu, executing the following command should suffice:

```
$ sudo apt-get update
$ sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build
```

On Arch Linux, executing the following command should suffice:

```
$ sudo pacman -Syyu autoconf automake curl python3 libmpc mpfr gmp gawk base-devel bison flex texinfo gperf libtool patchutils bc zlib expat
```

##### Getting the source

```
git clone https://github.com/riscv/riscv-gnu-toolchain --depth=1
```

##### 构建 newlib 交叉编译器 (同时支持 32位和64位)

```
cd riscv-gnu-toolchain
./configure --prefix=/opt/riscv --enable-multilib
sudo make
# 临时生效可执行文件路径, 长期生效请写入 shell 的相关文件中
export PATH=/opt/riscv/bin:$PATH
```

##### 检查

```
$ riscv64-unknown-elf-gcc --version
riscv64-unknown-elf-gcc () x.x.x
```

#### 2. 构建QEMU 7.2.0

##### 依赖

On Ubuntu, executing the following command should suffice:

```
$ sudo apt-get update
$ sudo apt-get install make ninja-build gcc pkg-config libglib2.0-dev libpixman-1-dev libcap-ng-dev libattr1-dev

```

On Arch Linux, executing the following command should suffice:

```
$ sudo pacman -Syyu make ninja gcc pkgconf glib2 pixman libcap-ng-dev attr
```

##### Getting the source

```
git clone https://github.com/qemu/qemu.git
cd qemu && git checkout v7.2.0
```

##### 构建

```
mkdir -p build
cd build
../configure --target-list=riscv32-softmmu,riscv64-softmmu --enable-virtfs --disable-gio --enable-debug
make $(nproc)
sudo make install
```

或通过 `--prefix=安装绝对路径` 指定安装的位置, 最终将该路径添加进行 `PATH`  环境变量中

##### 检查

```
$ qemu-system-riscv32 --version
QEMU emulator version 7.2.0 (v7.2.0)
Copyright (c) 2003-2022 Fabrice Bellard and the QEMU Project developers
```

### 构建 RT-thread

#### 依赖

```
sudo apt-get install scons g++-riscv64-linux-gnu binutils-riscv64-linux-gnu # 使用源中预编译的包的原因是为第一次直接成功编译在 qemu-system-riscv64 上运行 rt-thread 而无需进行修改
```

#### 构建

```
git clone https://github.com/OSCPU/rt-thread.git
cd rt-thread/bsp/qemu-riscv-virt64/
scons
```

#### 运行

```
$ sh qemu-nographic.sh
heap: [0x80022481 - 0x86422481]

 \ | /
- RT -     Thread Operating System
 / | \     4.0.4 build Mar 31 2023
 2006 - 2021 Copyright by rt-thread team
Hello RISC-V!
msh />
```

使用 `Ctrl-a` 松开后按 `x` 退出

## Usage <a name = "usage"></a>

Add notes about how to use the system.