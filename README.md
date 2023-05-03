---
date created: 2023-03-31 19:15
date updated: 2023-05-03 16:56
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

#### 0. 声明工作区

```sh
git clone https://github.com/Zweisamkeiten/transplantation-doc.git work && cd work
mkdir output
export WORKDIR=$(pwd) && echo $WORKDIR
source init.sh
git submodule update --init am-kernels
git submodule update --init abstract-machine
git submodule update --init rt-thread
```

#### 1. 构建 `riscv-gnu-toolchain` 的裸机 `newlib` 交叉编译器

> 如果不想从源码自行编译交叉编译器，可以下载预编译好的编译器 [mutilib](https://github.com/iEDA-Open-Source-Core-Project/riscv64-unknown-elf-mutilib), 并将其解压到 `$WORKDIR/output/riscv` 目录下。

##### 构建依赖

On Ubuntu, executing the following command should suffice:

```
$ sudo apt-get update
$ sudo apt-get install autoconf automake autotools-dev curl python3 libmpc-dev libmpfr-dev libgmp-dev gawk build-essential bison flex texinfo gperf libtool patchutils bc zlib1g-dev libexpat-dev ninja-build
```

On Arch Linux, executing the following command should suffice:

```
$ sudo pacman -Sy autoconf automake curl python3 libmpc mpfr gmp gawk base-devel bison flex texinfo gperf libtool patchutils bc zlib expat
```

##### Getting the source(From official repo)

```sh
git clone https://github.com/riscv/riscv-gnu-toolchain --depth=1
```

##### Getting the source(From mirror)

```sh
bash riscv-gnu-toolchain.sh
```

耐心等待所有 repo 拉取完成

##### 构建 newlib 交叉编译器 (同时支持 32位和64位)

```
cd $WORKDIR/riscv-gnu-toolchain
./configure --prefix=$WORKDIR/output/riscv --enable-multilib
make -j$(nproc)
# 临时生效可执行文件路径, 长期生效请写入 shell 的相关文件中
export PATH=$WORKDIR/output/riscv/bin:$PATH
```

##### 检查

```
$ riscv64-unknown-elf-gcc --version
riscv64-unknown-elf-gcc () x.x.x
$ test $(which riscv64-unknown-elf-gcc) == "$WORKDIR/output/riscv/bin/riscv64-unknown-elf-gcc"
$ echo $?
0
$ which riscv64-unknown-elf-gcc
/path/to/work/output/riscv/bin/riscv64-unknown-elf-gcc
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
$ sudo pacman -Sy make ninja gcc pkgconf glib2 pixman libcap-ng-dev attr
```

##### Getting the source

```
cd $WORKDIR/riscv-gnu-toolchain/qemu
git checkout v7.2.0
```

##### 构建

```
mkdir -p build
cd build
../configure --prefix=$WORKDIR/output/qemu --target-list=riscv32-softmmu,riscv64-softmmu --enable-virtfs --disable-gio --enable-debug
make -j$(nproc)
make install
export PATH=$WORKDIR/output/qemu/bin:$PATH
```

或通过 `--prefix=安装绝对路径` 指定安装的位置, 最终将该路径添加进行 `PATH` 环境变量中

##### 检查

```
$ qemu-system-riscv32 --version
QEMU emulator version 7.2.0 (v7.2.0)
Copyright (c) 2003-2022 Fabrice Bellard and the QEMU Project developers
$ test $(which qemu-system-riscv32) == "$WORKDIR/output/qemu/bin/qemu-system-riscv32"
$ echo $?
0
$ which qemu-system-riscv32
/path/to/work/output/qemu/bin/qemu-system-riscv32
```

### 构建 RT-thread

#### 依赖

```
sudo apt-get install scons g++-riscv64-linux-gnu binutils-riscv64-linux-gnu # 使用源中预编译的包的原因是为第一次直接成功编译在 qemu-system-riscv64 上运行 rt-thread 而无需进行修改
```

#### 构建

```
cd $WORKDIR
git submodule update --init --recursive
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

#### 构建 qemu-riscv-virt32

```
cd $WORKDIR
cd rt-thread/bsp/qemu-riscv-virt32/
scons
```

使用 `gen.sh` 生成相关 image 文件

```sh
$ bash gen.sh
```

## Usage <a name = "usage"></a>

### 自行添加测试程序
* 正确设置`AM_HOME`环境变量。
```sh
source init.sh
```
可以通过 `env | grep AM_HOME` 查看是否正确设置了`AM_HOME`环境变量。
* 将自己的测试程序源码目录放到`./prog/src`下，源码目录下需要有个Makefile，其内容格式可以参考`./prog/src/hello/Makefile`：
    ```Makefile
    SRCS = hello.c # 所有的源码路径
    NAME = hello   # 生成的可执行程序名

    include $(AM_HOME)/Makefile
    ```
* 然后切换到`./prog/src`，修改`run.py`中的`APP_NAME`和`APP_TYPE`, `APP_ARCH`的值。其中`APP_NAME`修改为上一个步骤中Makefile中填写的`NAME`，`APP_TYPE`修改为`flash`或者`mem`，表示生成的程序的加载类型，`flash`表示程序从flash直接执行，`mem`表示程序先从flash加载到mem中， `APP_ARCH`修改为 `riscv64-mycpu` 或 `riscv32-mycpu` 然后再执行。
* 执行`./prog/src/run.py`，编译通过的话就可以在`./prog/bin/$(FLASH_TYPE)`下得到可执行程序和相对应类型的 image。
