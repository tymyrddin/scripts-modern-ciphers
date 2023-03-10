# RSA: An asymmetric key exchange

RSA is perhaps the most widely known asymmetric algorithm. RSA is a public key method developed in 1977 by three mathematicians, Ron Rivest, Adi Shamir, and Len Adleman. In 1973, Clifford Cocks had developed a similar system.

The RSA algorithm is based on prime numbers and the difficulty of factoring a large number into its prime factors.

Implementing our own RSA encryption/decryption, rather than using a library, is not a good idea at all. Which is exactly why I am doing it, to replicate the failures of others, and to abuse such vulnerabilities. **Do not under any circumstances use this code for real communication**. It is unsafe and insecure!