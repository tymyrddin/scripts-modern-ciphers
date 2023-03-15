// RootMe: Strange encryption challenge
// gcc -m32 -o crypt crypt.c
// $ ./crypt oDjbNkIoLpaMo.bz2.crypt 1354709136
// mv oDjbNkIoLpaMo.bz2.crypt.crypt oDjbNkIoLpaMo.bz2
// bzip2 --decompress oDjbNkIoLpaMo.bz2

int main(int argc, char **argv) {
  char path[128];
  FILE *in, *out;
  long ts;

  if(argc < 2 || argc > 3) {
    printf("[-] Usage : %s <file> [timestamp]\n", argv[0]);
    return EXIT_FAILURE;
  }

  if (argc == 2) {
    ts = time(NULL);
  } else {
    ts = atol(argv[2]);
  }

  snprintf(path, sizeof(path)-1, "%s.crypt", argv[1]);

  if((in = fopen(argv[1], "r")) == NULL) {
    perror("[-] fopen (in) ");
    return EXIT_FAILURE;
  }

  if((out = fopen(path, "w")) == NULL) {
    perror("[-] fopen (out) ");
    return EXIT_FAILURE;
  }

  Srand(ts);
  crypt_file(in, out);

  printf("[+] File %s crypted !\n", path);
  printf("[+] DONE.\n");
  return EXIT_SUCCESS;
}
