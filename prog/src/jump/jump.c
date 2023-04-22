#include <am.h>

int main(){
  char *str = "jump-to-mem\n";
  for (char * p = str; *p != '\0'; p++) {
    putch(*p);
  }
  asm("jr %0" : : "r"(0x80000000));
}
