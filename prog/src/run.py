#!/bin/python

import os

APP_NAME = 'hello'
APP_TYPE = 'mem'  # flash, mem
APP_ARCH = 'riscv64-mycpu'
APP_ORG_BIN = APP_NAME + '-' + APP_ARCH + '.bin'
APP_ORG_ELF = APP_NAME + '-' + APP_ARCH + '.elf'
APP_JUMP_BIN = 'jump-' + APP_ARCH + '.bin'
APP_JUMP_ELF = 'jump-' + APP_ARCH + '.elf'
APP_STD_BIN = APP_NAME + '-' + APP_TYPE + '.bin'
APP_STD_ELF = APP_NAME + '-' + APP_TYPE + '.elf'

HOME_DIR = os.getcwd()

# clean previous build
os.system("rm ../bin -rf") 
os.system('mkdir -p ../bin/mem')
os.system('mkdir -p ../bin/flash')


def chg_ld_script(app_type):
    os.system("sed -i 's/core_[a-z]\+/core_" + app_type +
              "/' $AM_HOME/scripts/" + APP_ARCH + ".mk")


def chg_ld_addr(addr):
    os.system("sed -i 's/\(pmem_start=\)0x[0-9A-Z]\+/\\1" + addr +
              "/' $AM_HOME/scripts/" + APP_ARCH + ".mk")


def chg_ld_sp(addr):
    os.system("sed -i 's/\(_stack_top = ALIGN\)(0x[0-9A-Z]\+)/\\1(" + addr +
              ")/' $AM_HOME/scripts/platform/core_flash.ld")


def copy_oper(app_type):
    if app_type == 'flash':
        os.system('mv build/' + APP_ORG_BIN + ' build/' + APP_STD_BIN)
        os.system('mv build/' + APP_ORG_ELF + ' build/' + APP_STD_ELF)

    else:
        os.chdir(HOME_DIR + '/' + APP_NAME)
        os.system('mv build/' + APP_ORG_BIN + ' build/' + APP_STD_BIN)
        os.system('mv build/' + APP_ORG_ELF + ' build/' + APP_STD_ELF)
        os.chdir(HOME_DIR + '/jump')
        os.system('mv build/' + APP_JUMP_BIN + ' build/' + 'jump-' + APP_STD_BIN)
        os.system('mv build/' + APP_JUMP_ELF + ' build/' + 'jump-' + APP_STD_ELF)

    os.chdir(HOME_DIR + '/' + APP_NAME)
    os.system('mkdir -p ' + HOME_DIR + '/../bin/' + APP_TYPE + '/' + APP_NAME)
    os.system('cp -r build/*' + ' ' +
              HOME_DIR + '/../bin/' + APP_TYPE + '/' + APP_NAME + '/')

    os.chdir(HOME_DIR + '/jump')
    os.system('mkdir -p ' + HOME_DIR + '/../bin/' + APP_TYPE + '/jump')
    os.system('cp -r build/*' + ' ' +
              HOME_DIR + '/../bin/' + APP_TYPE + '/jump/')


if APP_TYPE == 'flash':
    chg_ld_script(APP_TYPE)
    chg_ld_addr('0x30000000')
    os.chdir(APP_NAME)
    os.system('make ARCH=' + APP_ARCH)

elif APP_TYPE == 'mem':
    chg_ld_script(APP_TYPE)
    chg_ld_addr('0x80000000')
    os.chdir(APP_NAME)
    os.system('make ARCH=' + APP_ARCH)

    chg_ld_script('flash')
    chg_ld_addr('0x30000000')
    os.chdir(HOME_DIR + '/jump')
    os.system('make ARCH=' + APP_ARCH)


if APP_TYPE == 'flash':
    copy_oper(APP_TYPE)
elif APP_TYPE == 'mem':
    copy_oper(APP_TYPE)
