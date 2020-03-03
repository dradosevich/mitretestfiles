//Danny Radosevich
#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
void sha(char *tosha)
{
  if (!tosha)
  {
        mp_printf("Invalid entry\r\n");
        print_help();
        return;
  }
  unsigned char *d = SHA256(tosha, strlen(s),0)// make d the sha of tosha

}
int main()
{
   // printf() displays the string inside quotation
   printf("Hello, World!");
   return 0;
}
